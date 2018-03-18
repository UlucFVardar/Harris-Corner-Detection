class Data():
    def __init__(self):
        self.list = []
        self.dumi=False;
        self.R = -1

    def append(self, v):
        self.list.append(v)

    def get(self, i):
        if i > len(self.list) and i < 0:
            print ("Data class ERROR: get(i) index is something stupid")
            return
        return self.list[i]

    def det(self):
        if len(self.list) != 3:
            print ("Data class ERROR: det() is not allowed for this data. N =", len(self.list))
            return
        return self.list[0] * self.list[2] - self.list[1] * self.list[1]
    def trace(self):
        if len(self.list) != 3:
            print ("Data class ERROR: trace() is not allowed for this data. N =", len(self.list))
            return
        return self.list[0] + self.list[2]

    def getHmatrix(self):
        if len(self.list) != 3:
            print ("Data class ERROR: getHmatrix() is not allowed for this data. N =", len(self.list))
            return
        Hmatrix = [[self.list[0], self.list[1]], [self.list[1], self.list[2]]]
        return Hmatrix

    def getR(self, k):
        if len(self.list) != 3:
            print ("Data class ERROR: getR() is not allowed for this data. N =", len(self.list))
            return
        self.R = self.det() - (k * self.trace() * self.trace())
        return self.R
