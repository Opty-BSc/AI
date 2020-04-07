import random


class LearningAgent:

    def __init__(self, nS, nA):
        if nS <= 0: raise ValueError("State Number")
        if nA <= 0: raise ValueError("Action Number")
        self.nS = nS
        self.nA = nA
        self.discFact = 0.8
        self.epsiRate = 0.8 / nA
        self.epsi = [0 for _ in range(nS)]
        self.Q = [[] for _ in range(nS)]
        self.QCounter = [[] for _ in range(nS)]
        self.R = [0 for _ in range(nS)]
        self.nst = [{} for _ in range(nS)]

    def update(self, st, lenAct):

        if 0 > st > self.nS: raise ValueError("State Number")
        if 0 > lenAct > self.nA: raise ValueError("Action Number")

        if lenAct > len(self.Q[st]):
            newAct = lenAct - len(self.Q[st])
            self.Q[st].extend(0 for _ in range(newAct))
            self.QCounter[st].extend(0 for _ in range(newAct))

    def learnUpdate(self, ost, nst, a):

        if 0 > nst > self.nS: raise ValueError("State Number")
        self.update(ost, a)

        try:
            self.nst[ost][a][nst] += 1
        except KeyError:
            if a in self.nst[ost]: pass
            else: self.nst[ost][a] = {}
            self.nst[ost][a][nst] = 1

    def selectactiontolearn(self, st, aa):

        self.update(st, len(aa))
        
        if random.random() < self.epsi[st]:
            maxQ = max(self.Q[st][:len(aa)])
            return random.choice(
                [a for a in range(len(aa)) if self.Q[st][a] == maxQ])
        else:
            minC = min(self.QCounter[st][:len(aa)])
            return random.choice(
                [a for a in range(len(aa)) if self.QCounter[st][a] == minC])

    def selectactiontoexecute(self, st, aa):

        self.update(st, len(aa))

        return max(range(len(aa)), key=self.Q[st].__getitem__)

    def V(self, ost, a):

        V = 0
        sumEP = 0
        for nst in self.nst[ost][a]:
            EP = self.nst[ost][a][nst]
            if self.Q[nst]:
                V += max(self.Q[nst]) * EP
            sumEP += EP

        return V / sumEP

    def learn(self, ost, nst, a, r):

        self.learnUpdate(ost, nst, a)

        EP = sum(self.QCounter[ost])
        self.QCounter[ost][a] += 1
        
        if EP < self.nA:
            self.epsi[ost] += self.epsiRate

        self.R[ost] = (self.R[ost] * EP + r) / (EP + 1)
        self.Q[ost][a] = self.R[ost] + self.discFact * self.V(ost, a)
