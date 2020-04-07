from itertools import permutations
from math import *


class Node:
    def __init__(self, state, ticketFlag, transport=None, parent=None):
        self.state = state
        self.transport = transport
        self.parent = parent
        if parent is None:
            if ticketFlag:
                self.tickets = [0, 0, 0]
        else:
            if ticketFlag:
                self.tickets = parent.tickets[:]
                self.tickets[transport] += 1


class Agent:
    def __init__(self, sP, init):
        self.sP = sP
        self.queue = {init: [Node(init, self.sP.ticketFlag)]}
        self.goals = None
        self.paths = None

    def setGoals(self, goals):
        self.goals = goals
        self.paths = tuple([] for _ in range(len(goals)))

    def validateTickets(self, pNL, pNR):

        for ti in range(len(self.sP.tickets)):
            if pNL.tickets[ti] + pNR.tickets[ti] > self.sP.tickets[ti]:
                return False

        return True

    def addPaths(self, genNode, interNodes, index):

        for interNode in interNodes:

            if self.sP.ticketFlag and \
                    not self.validateTickets(genNode, interNode):
                continue

            self.paths[index].append((genNode, interNode))
            if self.sP.nAgents == 1: return

    def search(self):
        queue = {}
        for paths in self.paths:
            del paths[:]

        for srcState in self.queue:
            for source in self.queue[srcState]:
                # Expand Source
                for transport, state in self.sP.model[srcState]:
                    if self.sP.ticketFlag and \
                            source.tickets[transport] == self.sP.tickets[transport]:
                        continue
                    # Create Node
                    genNode = Node(state, self.sP.ticketFlag, transport, source)
                    if state in queue:
                        queue[state].append(genNode)
                    else:
                        queue[state] = [genNode]

                    for index, goal in enumerate(self.goals):
                        if state in goal.queue:
                            # New Path Found
                            self.addPaths(genNode, goal.queue[state], index)
                            if self.sP.nAgents == 1 and self.paths[0]:
                                return self.paths

                self.sP.limitexp -= 1

        self.queue = queue
        return self.paths


class Path:
    def __init__(self):
        self.paths = [[[], []], [[], []]]
        self.index = 0
        self.depth = 1

    def switch(self):
        if self.index:
            self.depth += 1
        self.index = self.index ^ 1

    def expand(self):
        self.paths.append([[], []])

    def get(self): return self.paths

    def add(self, pN):

        iNode = pN[self.index]
        for i in range(self.depth, 0, -1):
            if iNode.state in self.paths[i][1]: return False
            iNode = iNode.parent

        if iNode.state in self.paths[0][1]: return False

        iNode = pN[self.index ^ 1]
        for i in range(self.depth + 1, len(self.paths)):
            iNode = iNode.parent
            if iNode.state in self.paths[i][1]: return False

        iNode = pN[self.index]
        for i in range(self.depth, 0, -1):
            self.paths[i][0].append(iNode.transport)
            self.paths[i][1].append(iNode.state)
            iNode = iNode.parent

        self.paths[0][1].append(iNode.state)

        iNode = pN[self.index ^ 1]
        for i in range(self.depth + 1, len(self.paths)):
            self.paths[i][0].append(iNode.transport)
            iNode = iNode.parent
            self.paths[i][1].append(iNode.state)

        return True

    def pop(self):
        self.paths[0][1].pop()
        for i in range(1, len(self.paths)):
            self.paths[i][0].pop()
            self.paths[i][1].pop()


class SearchProblem:

    def __init__(self, goal, model, auxheur=[]):
        self.goals = goal
        self.model = model
        self.points = auxheur
        self.nAgents = len(self.goals)
        self.agents = None
        self.limitexp = None
        self.limitdepth = None
        self.tickets = None
        self.ticketFlag = None
        self.paths = None

    def validateTickets(self, pNs):

        if self.ticketFlag:
            for ti in range(len(self.tickets)):
                sumT = pNs[0][0].tickets[ti] + pNs[0][1].tickets[ti]
                if len(pNs) > 1: sumT += pNs[1][0].tickets[ti] + pNs[1][1].tickets[ti]
                if len(pNs) > 2: sumT += pNs[2][0].tickets[ti] + pNs[2][1].tickets[ti]
                if sumT > self.tickets[ti]:
                    return False

        return True

    def validatePaths(self, pNs, index):

        return self.validateTickets(pNs) and self.paths.add(pNs[index])

    def pathFilter(self, pathNodes):

        if not all(pathNodes):
            return False

        if len(self.goals) == 1:
            return self.paths.add(pathNodes[0][0])

        for pN0 in pathNodes[0]:
            self.paths.add(pN0)
            for pN1 in pathNodes[1]:
                if not self.validatePaths((pN0, pN1), 1):
                    continue
                for pN2 in pathNodes[2]:
                    if not self.validatePaths((pN0, pN1, pN2), 2):
                        continue
                    return True
                self.paths.pop()
            self.paths.pop()
        return False

    def searchOrd(self):

        for agents in zip(self.agents[0], self.agents[1]):
            agents[0].setGoals((agents[1],))
            agents[1].setGoals((agents[0],))

        index = 0
        while self.limitexp and self.limitdepth:
            pathNodes = tuple(agent.search()[0] for agent in self.agents[index])
            if self.pathFilter(pathNodes):
                return self.paths.get()
            self.paths.switch()
            self.paths.expand()
            self.limitdepth -= 1
            index = index ^ 1

        return []

    def searchAny(self):

        for i in range(2):
            for agent in self.agents[i]:
                agent.setGoals(self.agents[i ^ 1])

        i = 0
        while self.limitexp and self.limitdepth:
            pathNodes = tuple(agent.search() for agent in self.agents[i])
            for indexes in permutations(range(len(self.goals))):
                if i: pNs = tuple(pathNodes[k][n] for n, k in enumerate(indexes))
                else: pNs = tuple(pathNodes[n][k] for n, k in enumerate(indexes))
                if self.pathFilter(pNs):
                    return self.paths.get()
            self.paths.switch()
            self.paths.expand()
            self.limitdepth -= 1
            i = i ^ 1

        return []

    def search(self, init, limitexp=2000, limitdepth=10, tickets=[inf, inf, inf],
               anyorder=False):

        if init == self.goals:
            return [[[], init]]

        self.tickets = tickets
        self.ticketFlag = not all(ticket is inf for ticket in tickets)

        self.limitexp = limitexp
        self.limitdepth = min(limitdepth, sum(tickets) // len(self.goals))

        self.agents = (
            tuple(Agent(self, start) for start in init),
            tuple(Agent(self, target) for target in self.goals)
        )
        self.paths = Path()
        return self.searchAny() if anyorder else self.searchOrd()
