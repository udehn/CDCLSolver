import queue
from Parser import Parser


class Node:
    def __init__(self, dl, lit, rs):
        self.decisionLevel = dl
        self.literal = lit
        self.reason = rs

    def __repr__(self):
        return f'<({self.decisionLevel}) {self.literal} {self.reason}>'


class Clause:
    def __init__(self, literals: list, i: int):
        self.clause = literals
        self.assignment = {}  # assignment for each literal
        self.index = i
        self.value = None
        for lit in self.clause:
            self.assignment[lit] = None

    def __repr__(self):
        return f'<({self.clause}) {self.value} >'


class CDCLSolver:
    def __init__(self, cnf_clause):
        self.cnf = []
        i = 0
        for clause in cnf_clause:
            self.cnf.append(Clause(clause, i))
            i += 1
        self.assignment = {}  # assignment for each clause
        for clause in self.cnf:
            for literal in clause.clause:
                if literal[0] == '-':
                    lit2 = literal[1:]
                else:
                    lit2 = '-'+literal
                if literal not in self.assignment and lit2 not in self.assignment:
                    self.assignment[literal] = None
        # i = 0
        # for clause in cnf_clause:
        #     self.cnf.append(Clause(clause, i))
        #     self.assignment[self.cnf[i]] = None
        #     i = i + 1
        self.decisions = []
        self.decisionLevel = 0

    def __repr__(self):
        return f'<({self.cnf}) >'

    def find_unit_clause(self):
        for clause in self.cnf:
            if clause.value is not None:
                continue
            # print("try2")
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

    # def add_next_node(self, lit, cls):

    def update_cnf_value(self, unit_clause_literal):
        lit_value = None
        lit_value_not = None
        lit11 = None
        lit22 = None
        # print(unit_clause_literal)

        # print(unit_clause_literal[1:])
        # if unit_clause_literal[0] == '-':
        #     if len(unit_clause_literal) > 2:
        #         print(unit_clause_literal[1:])
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
                # print(unit_clause_literal[1:])
                clause.assignment[lit11] = lit_value
                # print(lit_value)
            elif lit22 in clause.clause:
                clause.assignment[lit22] = lit_value_not

        # print(self.decisions)
        for clause in self.cnf:
            # print(clause)
            if clause.value is None:
                # possible_node_literal = None
                have_none = 0
                # flag_False = 0
                for literal in clause.clause:
                    if clause.assignment[literal] is None:
                        have_none = have_none + 1
                        # possible_node_literal = literal
                        # break
                    if clause.assignment[literal] is True:
                        clause.value = True
                        # self.assignment[clause] = True
                        # self.decisions.append(Node(self.decisionLevel, ))
                        break
                # if clause.value is not True and have_none == 1:
                #     self.decisions.append(Node(self.decisionLevel, possible_node_literal, clause.clause))
                #     clause.value = True
                #     self.assignment[clause] = True
                if clause.value is not True and have_none == 0:
                    clause.value = False
                    # flag_False = 1
                    # self.assignment[clause] = False
                    print(self.decisionLevel)
                    self.decisions.append(Node(self.decisionLevel, None, clause.clause))
                    print(Node(self.decisionLevel, None, clause.clause))
                    print("111111")
                    break
                # if flag_False == 1:
                #     break

        print(len(self.cnf))
        print(self.cnf[-1])
        print(self.decisionLevel)
        print("2222222")

    def BCP(self):
        # for clause in self.cnf:
        #     if clause.value is False:
        #         print("no need to BCP")
        #         return True
        while True:
            unit_clause_literal, unit_clause = self.find_unit_clause()
            print(unit_clause_literal)
            print(unit_clause)
            if unit_clause_literal is None:
                break
            # print("find_unit")
            # print(unit_clause_literal)

            print("before")
            print(self.assignment)
            print(self.decisions)
            self.decisions.append(Node(self.decisionLevel, unit_clause_literal, unit_clause))
            print(self.decisions)

            if unit_clause_literal[0] == '-':
                unit_clause_literal2 = unit_clause_literal[1:]
            else:
                unit_clause_literal2 = '-'+unit_clause_literal
            if unit_clause_literal in self.assignment.keys():
                self.assignment[unit_clause_literal] = True
            else:
                self.assignment[unit_clause_literal2] = False

            print(self.assignment)
            print(len(self.assignment))
            self.update_cnf_value(unit_clause_literal)

            # print("1111111")
            # node = self.decisions[-1]
            # node
            #
            # print(temp.decisionLevel)
        # print("111111111111")
        return True  # unit не найдено

    # def get_all_ways(self, nodes_can_reach_the_conflict, way_now, node_to_be_check):
    #     for node, value in nodes_can_reach_the_conflict:
    #         if value is False:
    #             continue
    #     return all_ways

    # def check_in_all_ways(self, nodes_can_reach_the_conflict, node_to_check, way_now):
    #     for

    def analyze_conflict(self):
        backtrack_level = 0
        # if self.decisions == []:
        #     return self.decisionLevel

        flag = True
        # for v in self.assignment.values():
        for clause in self.cnf:
            if clause.value is False:
                flag = False
                # print("flag: ", flag)
                # print(m)
                break

        if flag is not False:
            print("no conflict")
            return self.decisionLevel

        if self.decisionLevel == 0:
            return -1
        # прстроить list of ways по обратной порядке,
        # начинается с Node conflict, окончается при встрече Node decision
        # list_of_ways_in_the_newest_level = list()
        # latest_decision_node = None
        # for node in self.decisions:
        #     if node.decisionLevel == self.decisionLevel and node.reason is None:
        #         latest_decision_node = node
        #         break
        nodes_in_the_newest_level = []
        for node in self.decisions:
            if node.decisionLevel == self.decisionLevel:
                nodes_in_the_newest_level.append(node)

        nodes_can_reach_conflict_and_in_the_newest_level = {}
        for node in nodes_in_the_newest_level:
            nodes_can_reach_conflict_and_in_the_newest_level[node] = False
        # print(nodes_can_reach_conflict_and_in_the_newest_level.items())

        queue_nodes = queue.Queue()
        # temp = self.decisions[-1]
        # queue_nodes.put(temp)

        for node in nodes_in_the_newest_level:
            if node.literal is None:
                queue_nodes.put(node)
                break
        # print(self.decisions[0])

        while queue_nodes.empty() is False:
            # print(queue_nodes.qsize())
            temp = queue_nodes.get()
            # print(queue_nodes.qsize())

            # print(temp)
            if temp.decisionLevel < self.decisionLevel:
                continue
            if temp.reason is None:
                nodes_can_reach_conflict_and_in_the_newest_level[temp] = True
                continue
            if len(temp.reason) == 1 and temp.reason[0] == temp.literal:
                nodes_can_reach_conflict_and_in_the_newest_level[temp] = True
                continue
            # if temp.literal is not None:
            nodes_can_reach_conflict_and_in_the_newest_level[temp] = True
            for lit in temp.reason:
                if lit == temp.literal:
                    continue
                lit2 = lit
                if lit[0] == '-':
                    lit2 = lit[1:]
                else:
                    lit2 = '-'+lit
                # print(lit)
                # print(lit2)
                for node in nodes_in_the_newest_level:
                    if lit == node.literal or lit2 == node.literal:
                        queue_nodes.put(node)
                        # print(node)

        # print(nodes_can_reach_conflict_and_in_the_newest_level)
        # without decision-node and conflict-node

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
                # lit11 = lit
                lit22 = lit
                if lit[0] == '-':
                    # lit11 = lit[1:]
                    lit22 = lit[1:]
                else:
                    # lit11 = lit
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
                # if lit in literal_nodes_in_the_newest_level and lit not in learned_clause
                # if lit in literal_nodes_in_the_newest_level or lit22 in literal_nodes_in_the_newest_level:
                #     continue
                # if lit in learned_clause or lit22 in learned_clause:
                #     continue
                # else:
                #     learned_clause.append(lit22)

                    # if lit[0] == '-':
                    #     learned_clause.append(lit11)
                    # else:
                    #     learned_clause.append(lit22)

        # print(learned_clause)
        # self.decisionLevel = self.decisionLevel - 1
        # return backtrack_level

        # else:
        print("R and learned_clause")
        print(R)
        print(learned_clause)
        temp = Clause(learned_clause, len(self.cnf))

        # for lit in self.cnf[-1].clause:
        #     if lit[0] == '-':
        #         lit2 = lit[1:]
        #     else:
        #         lit2 = '-'+lit
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
        # self.assignment[temp] = None

        R_levels = sorted(list(set([node.decisionLevel for node in R])))

        backtrack_level = 0
        if len(R_levels) > 1:
            backtrack_level = R_levels[-2]
        print(backtrack_level)
        return backtrack_level

    def find_unassigned_literal(self):
        # for clause in self.cnf:
        #     if clause.value is None:
        #         for lit in clause.clause:
        #             if clause.assignment[lit] is None:
        #                 return lit
        for literal, value in self.assignment.items():
            if value is None:
                return literal
        return None

    # def remake_value(self, remake_literal):
    #     lit2 = remake_literal
    #     if len(remake_literal) == 1:
    #         lit2 = '-'+remake_literal
    #     else:
    #         lit2 = remake_literal[1]
    #     for clause in self.cnf:
    #         for literal in clause.clause:
    #

    def back_track(self, backtrack_level):
        print("in back_track")
        print(self.decisions)

        flag = True
        for clause in self.cnf:
            if clause.value is False:
                flag = False
                break

        if flag is not False:
            return self.decisionLevel

        remake_literal = []
        while self.decisions:
            node = self.decisions[-1]
            # if backtrack_level == 0:
            #     break
            if node.decisionLevel <= backtrack_level:
                break
            if node.literal is not None:
                remake_literal.append(node.literal)
            self.decisions.pop()

        print(remake_literal)


        for lit_to_remake in remake_literal:
            if lit_to_remake[0] == '-':
                lit_to_remake2 = lit_to_remake[1:]
            else:
                lit_to_remake2 = '-' + lit_to_remake
            if lit_to_remake in self.assignment.keys():
                self.assignment[lit_to_remake] = None
            elif lit_to_remake2 in self.assignment.keys():
                self.assignment[lit_to_remake2] = None

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

                # have_none = 0
                # for lit in cluase_to_remake.clause:
                #     if cluase_to_remake.assignment[lit] is True:  # or cluase_to_remake.assignment[lit2] == False:
                #         cluase_to_remake.value = True
                #         # self.assignment[cluase_to_remake] = True
                #         break
                #     if cluase_to_remake.assignment[lit] is None:  # or cluase_to_remake.assignment[lit2] == None:
                #         have_none = have_none + 1
                #         continue
                # if have_none > 0 and cluase_to_remake.value is not True:
                #     # self.assignment[cluase_to_remake] = None
                #     cluase_to_remake.value = None

        print("whyyy")
        print(self.decisions)
        print(self.decisionLevel)
        self.decisionLevel = backtrack_level
        print(self.decisionLevel)

        self.BCP()
        print("after BCP")
        print(self.assignment)
        for clause in self.cnf:
            if clause.value is True:
                print(clause.clause)
        print(self.decisionLevel)

        print(self.decisions)

    def decide(self):
        print("in decision")
        print(self.decisions)

        for node in self.decisions:
            if node.literal is None:
                print("no need to decide")
                return True

        unassigned_literal = self.find_unassigned_literal()
        # print("unassigned_literal")
        print(unassigned_literal)
        print("unassigned_literal")

        if unassigned_literal is None:
            # print(self.assignment)
            return False
        # print(self.decisions)
        self.decisions.append(Node(self.decisionLevel + 1, unassigned_literal, None))

        unassigned_literal2 = unassigned_literal

        if unassigned_literal[0] == '-':
            unassigned_literal2 = unassigned_literal[1:]
        else:
            unassigned_literal2 = '-' + unassigned_literal

        if unassigned_literal in self.assignment.keys():
            self.assignment[unassigned_literal] = True
        elif unassigned_literal2 in self.assignment.keys():
            self.assignment[unassigned_literal2] = False

        self.update_cnf_value(unassigned_literal)
        # print(self.decisions)
        self.decisionLevel = self.decisionLevel + 1
        # print("decide")
        print(self.decisions)
        return True

    def CDCL(self):
        while True:
            while self.BCP():
                print(self.decisions)
                backtrack_level = self.analyze_conflict()
                if backtrack_level < 0:
                    return False
                self.back_track(backtrack_level)
                if self.decide() is not True:
                    print(self.assignment)
                    return True
