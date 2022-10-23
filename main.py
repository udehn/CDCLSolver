from Parser import Parser
from CDCLSolver import CDCLSolver

if __name__ == '__main__':
    P = Parser()
    for i in range(1, 5):
        filename = "./TestFiles/TestFileSAT"+str(i)+".cnf"
        cnf = P.parse(filename)
        Solver = CDCLSolver(cnf)
        if Solver.CDCL():
            print(filename+": SAT")
            print("assignment: ", Solver.assignment, "\n")
        else:
            print(filename+": UNSAT\n")

        filename = "./TestFiles/TestFileUNSAT"+str(i)+".cnf"
        cnf = P.parse(filename)
        Solver = CDCLSolver(cnf)
        if Solver.CDCL():
            print(filename+": SAT")
            print("assignment: ", Solver.assignment, "\n")
        else:
            print(filename+": UNSAT\n")
