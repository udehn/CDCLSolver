import queue


class Node:
    def __init__(self, dl, lit, rs):
        self.decisionLevel = dl
        self.literal = lit
        self.reason = rs


class Clause:
    def __init__(self, literals: list, i: int):
        self.clause = literals
        self.assignment = {}
        self.index = i
        self.value = None
        for lit in self.clause:
            self.assignment[lit] = None


class CDCLSolver:
    def __init__(self, cnf_clause):
        self.cnf = []
        i = 0
        for clause in cnf_clause:
            self.cnf.append(Clause(clause, i))
            i += 1
        self.assignment = {}
        for clause in self.cnf:
            for literal in clause.clause:
                if literal[0] == '-':
                    lit2 = literal[1:]
                else:
                    lit2 = '-'+literal
                if literal not in self.assignment and lit2 not in self.assignment:
                    self.assignment[literal] = None

        self.decisions = []
        self.decisionLevel = 0

    def find_unit_clause(self):
        for clause in self.cnf:
            if clause.value is not None:
                continue
            num_of_none = 0
            unit_clause_literal = None
            unit_clause = None
            for lit in clause.clause:
                if clause.assignment[lit] is None:
                    num_of_none = num_of_none + 1
                    unit_clause_literal = lit
                    unit_clause = clause.clause
            if num_of_none == 1:
                return unit_clause_literal, unit_clause
        return None, None

    # обновить значение cnf
    # update the cnf value
    def update_cnf_value(self, unit_clause_literal):
        if unit_clause_literal[0] == '-':
            lit_value = False
            lit_value_not = True
            lit11 = unit_clause_literal[1:]
            lit22 = unit_clause_literal
        else:
            lit_value = True
            lit_value_not = False
            lit11 = unit_clause_literal
            lit22 = '-'+unit_clause_literal

        for clause in self.cnf:
            if lit11 in clause.clause:
                clause.assignment[lit11] = lit_value
            elif lit22 in clause.clause:
                clause.assignment[lit22] = lit_value_not

        for clause in self.cnf:
            if clause.value is None:
                have_none = 0
                for literal in clause.clause:
                    if clause.assignment[literal] is None:
                        have_none = have_none + 1
                    if clause.assignment[literal] is True:
                        clause.value = True
                        break
                if clause.value is not True and have_none == 0:
                    clause.value = False
                    self.decisions.append(Node(self.decisionLevel, None, clause.clause))
                    break

    def BCP(self):
        while True:
            unit_clause_literal, unit_clause = self.find_unit_clause()
            if unit_clause_literal is None:
                break
            self.decisions.append(Node(self.decisionLevel, unit_clause_literal, unit_clause))

            if unit_clause_literal[0] == '-':
                unit_clause_literal2 = unit_clause_literal[1:]
            else:
                unit_clause_literal2 = '-'+unit_clause_literal
            if unit_clause_literal in self.assignment.keys():
                self.assignment[unit_clause_literal] = True
            else:
                self.assignment[unit_clause_literal2] = False

            self.update_cnf_value(unit_clause_literal)

        return True  # unit не найдено

    # Analysis back to which level
    # Анализ до какого уровня
    def analyze_conflict(self):
        # Determining if a conflict exists
        flag = True
        for clause in self.cnf:
            if clause.value is False:
                flag = False
                break
        if flag is not False:
            return self.decisionLevel

        # Conflict occurs at ground zero
        if self.decisionLevel == 0:
            return -1

        nodes_in_the_newest_level = []
        for node in self.decisions:
            if node.decisionLevel == self.decisionLevel:
                nodes_in_the_newest_level.append(node)

        nodes_can_reach_conflict_and_in_the_newest_level = {}
        for node in nodes_in_the_newest_level:
            nodes_can_reach_conflict_and_in_the_newest_level[node] = False

        queue_nodes = queue.Queue()

        for node in nodes_in_the_newest_level:
            if node.literal is None:
                queue_nodes.put(node)
                break

        while queue_nodes.empty() is False:
            temp = queue_nodes.get()

            if temp.decisionLevel < self.decisionLevel:
                continue
            if temp.reason is None:
                nodes_can_reach_conflict_and_in_the_newest_level[temp] = True
                continue
            if len(temp.reason) == 1 and temp.reason[0] == temp.literal:
                nodes_can_reach_conflict_and_in_the_newest_level[temp] = True
                continue

            nodes_can_reach_conflict_and_in_the_newest_level[temp] = True
            for lit in temp.reason:
                if lit == temp.literal:
                    continue
                lit2 = lit
                if lit[0] == '-':
                    lit2 = lit[1:]
                else:
                    lit2 = '-'+lit
                for node in nodes_in_the_newest_level:
                    if lit == node.literal or lit2 == node.literal:
                        queue_nodes.put(node)

        literal_nodes_in_the_newest_level = []
        for node in nodes_in_the_newest_level:
            literal_nodes_in_the_newest_level.append(node.literal)

        R = []
        learned_clause = []

        for node, val in nodes_can_reach_conflict_and_in_the_newest_level.items():
            if val is False:
                continue
            if node.reason is None:
                if node.literal[0] == '-':
                    learned_clause.append(node.literal[1:])
                    R.append(node)
                else:
                    learned_clause.append('-'+node.literal)
                    R.append(node)
                continue
            for lit in node.reason:
                lit22 = lit
                if lit[0] == '-':
                    lit22 = lit[1:]
                else:
                    lit22 = '-'+lit
                for node2 in self.decisions:
                    if lit == node2.literal and \
                            lit22 not in learned_clause and \
                            lit not in literal_nodes_in_the_newest_level and \
                            lit22 not in literal_nodes_in_the_newest_level:
                        learned_clause.append(lit22)
                        R.append(node2)
                    elif lit22 == node2.literal and \
                            lit not in learned_clause and \
                            lit not in literal_nodes_in_the_newest_level and \
                            lit22 not in literal_nodes_in_the_newest_level:
                        learned_clause.append(lit)
                        R.append(node2)
        temp = Clause(learned_clause, len(self.cnf))

        for node in self.decisions:
            for lit in temp.clause:
                lit2 = lit
                if lit[0] == '-':
                    lit2 = lit[1:]
                else:
                    lit2 = '-'+lit
                if node.literal == lit:
                    temp.assignment[lit] = True
                if node.literal == lit2:
                    temp.assignment[lit] = False

        self.cnf.append(temp)

        R_levels = sorted(list(set([node.decisionLevel for node in R])))

        backtrack_level = 0
        if len(R_levels) > 1:
            backtrack_level = R_levels[-2]
        return backtrack_level

    # Найти неназначенный элемент
    # Find unassigned element
    def find_unassigned_literal(self):
        for literal, value in self.assignment.items():
            if value is None:
                return literal
        return None

    # Back to the backtrack_level
    # Вернуться на уровень backtrack_level
    def back_track(self, backtrack_level):
        # Determining if a conflict exists
        flag = True
        for clause in self.cnf:
            if clause.value is False:
                flag = False
                break

        if flag is not False:
            return self.decisionLevel

        # Find the literal that needs to be reset
        remake_literal = []
        while self.decisions:
            node = self.decisions[-1]
            if node.decisionLevel <= backtrack_level:
                break
            if node.literal is not None:
                remake_literal.append(node.literal)
            self.decisions.pop()

        # Reset value inside self.assgiment
        for lit_to_remake in remake_literal:
            if lit_to_remake[0] == '-':
                lit_to_remake2 = lit_to_remake[1:]
            else:
                lit_to_remake2 = '-' + lit_to_remake
            if lit_to_remake in self.assignment.keys():
                self.assignment[lit_to_remake] = None
            elif lit_to_remake2 in self.assignment.keys():
                self.assignment[lit_to_remake2] = None

        # Reset the value of each clause
        for lit_to_remake in remake_literal:
            for cluase_to_remake in self.cnf:
                if lit_to_remake[0] != '-':
                    lit_to_remake2 = '-' + lit_to_remake
                else:
                    lit_to_remake2 = lit_to_remake[1:]

                if lit_to_remake in cluase_to_remake.clause:
                    cluase_to_remake.assignment[lit_to_remake] = None
                elif lit_to_remake2 in cluase_to_remake.clause:
                    cluase_to_remake.assignment[lit_to_remake2] = None

                for lit in cluase_to_remake.clause:
                    if cluase_to_remake.assignment[lit] is True:
                        cluase_to_remake.value = True
                        break
                    cluase_to_remake.value = None

        self.decisionLevel = backtrack_level
        self.BCP()

    # decide whether to assign an unassigned literal
    # решить, нужно ли присваивать неназначенный литерал
    def decide(self):
        # Conflicts arise, no need to assign
        for node in self.decisions:
            if node.literal is None:
                return True

        # Find unassigned literal
        unassigned_literal = self.find_unassigned_literal()
        if unassigned_literal is None:
            return False

        # Add assignment decision
        self.decisions.append(Node(self.decisionLevel + 1, unassigned_literal, None))

        if unassigned_literal[0] == '-':
            unassigned_literal2 = unassigned_literal[1:]
        else:
            unassigned_literal2 = '-' + unassigned_literal

        if unassigned_literal in self.assignment.keys():
            self.assignment[unassigned_literal] = True
        elif unassigned_literal2 in self.assignment.keys():
            self.assignment[unassigned_literal2] = False

        self.update_cnf_value(unassigned_literal)
        self.decisionLevel = self.decisionLevel + 1
        return True

    def CDCL(self):
        while True:
            while self.BCP():
                backtrack_level = self.analyze_conflict()
                if backtrack_level < 0:
                    return False
                self.back_track(backtrack_level)
                if self.decide() is not True:
                    return True
