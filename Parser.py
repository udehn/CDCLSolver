import string


class Parser:
    def __init__(self):
        self.cnf = []

    def parse(self, filename: string):
        self.cnf = []
        with open(filename) as f:
            data = f.readline()
            while data:
                line = data.split()
                if line[0] == 'c':
                    data = f.readline()
                    continue
                elif line[0] == 'p':
                    data = f.readline()
                    continue
                else:
                    Line = []
                    for i in range(0, len(line)):
                        if line[i] == '0':
                            break
                        Line.append(line[i])
                    self.cnf.append(Line)
                data = f.readline()
        return self.cnf
