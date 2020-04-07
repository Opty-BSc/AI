import pickle
import copy
import matplotlib.pyplot as plt
import time
import imp

with open("coords.pickle", "rb") as fp:   # Unpickling
    coords = pickle.load(fp)
    
with open("mapasgraph.pickle", "rb") as fp:   #Unpickling
    AA = pickle.load(fp)
U = AA[1]

def plotpath(P,coords):   
        img = plt.imread('maps.png')
        plt.imshow(img)
        colors = ['r.-','g+-','b^-']
        I = P[0][1]
        for agind in range(len(P[0][1])):
                st = I[agind]-1
                for tt in P:                        
                        nst = tt[1][agind]-1
                        plt.plot([coords[st][0],coords[nst][0]],[coords[st][1],coords[nst][1]],colors[agind])
                        st = nst
        plt.axis('off')
        fig = plt.gcf()
        fig.set_size_inches(1.*18.5, 1.*10.5)
        #fig.savefig('test2png.png', dpi=100)   
        plt.show()
        
def validatepath(oP,oI,U,ogoal,tickets=[25,25,25],anyorder = False):
        print(oI," > ",ogoal," with ",tickets)
        print(oP)
        if not oP:
                return False
        P = copy.deepcopy(oP)
        I = copy.copy(oI)
        mtickets = copy.copy(tickets)

        if I!=P[0][1]:
                print('path does not start in the initial state')
                return False
        del P[0]
        
        for tt in P:
                for agind,ag in enumerate(tt[1]):
                        #print(ag)
                        st = I[agind]
                        if mtickets[tt[0][agind]]==0:
                                print('no more tickets')
                                return False
                        else:
                                mtickets[tt[0][agind]] -= 1
                                
                                if [tt[0][agind],ag] in U[st]:
                                        I[agind] = ag
                                        #pass
                                else:
                                        print('invalid action')
                                        return False
                if(len(set(I))<3) and len(I)==3:
                        print('there is more than one police in the same location')
                        return False
        if anyorder:
                if (set(oP[-1][1])==set(ogoal)):
                        return True
        else:
                if (oP[-1][1]==ogoal):
                        return True
        print('error final position')
        return False

def markproj(F):
        M = []
        tinittotal = time.process_time()

        try:
                #print("\n(2 val) Exercise 1 - One agent, No limits")
                SP = F.SearchProblem(goal = [56], model = U, auxheur=coords)
                tinit = time.process_time()
                I = [30]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[56]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:
                SP = F.SearchProblem(goal = [110], model = U, auxheur=coords)
                tinit = time.process_time()
                I = [59]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[110]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:
                SP = F.SearchProblem(goal = [59], model = U, auxheur=coords)
                tinit = time.process_time()
                I = [110]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[59]):
                        M.append(len(nn))
                else:
                        M.append(-1)
                
        except:
                M.append(-1)
              
        try:
                #print("\n(4 val) Exercise 2 - One agent, Limits")
                SP = F.SearchProblem(goal = [56], model = U, auxheur=coords)
                I = [30]
                nn = SP.search(I, limitdepth = 10, tickets = [5,5,2])
                if validatepath(nn,I,U,[56], tickets = [5,5,2]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:
                SP = F.SearchProblem(goal = [72], model = U, auxheur=coords)
                I = [8]
                nn = SP.search(I, limitdepth = 10, tickets = [5,5,2])
                if validatepath(nn,I,U,[72], tickets = [5,5,2]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                SP = F.SearchProblem(goal = [72], model = U, auxheur=coords)
                I = [8]
                nn = SP.search(I, limitdepth = 10, tickets = [5,5,0])
                if validatepath(nn,I,U,[72], tickets = [5,5,0]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:
                        
                #print("\n(6 val) Exercise 3 - Three agents, No limits (test 1)")
                SP = F.SearchProblem(goal = [2,21,9], model = U, auxheur=coords)
                I = [1,3,7]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[2,21,9]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                SP = F.SearchProblem(goal = [1,3,7], model = U, auxheur=coords)
                I = [2,21,9]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[1,3,7]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                SP = F.SearchProblem(goal = [63,99,84], model = U, auxheur=coords)
                I = [84,62,63]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[63,99,84]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:
                        
                SP = F.SearchProblem(goal = [61,60,71], model = U, auxheur=coords)
                I = [30,40,109]
                nn = SP.search(I, limitdepth = 10)
                if validatepath(nn,I,U,[61,60,71]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                #print("\n(4 val) Exercise 4 - Three agents, Limits")
                SP = F.SearchProblem(goal = [63,61,70], model = U, auxheur=coords)
                tinit = time.process_time()
                I = [30,40,109]
                nn = SP.search(I, limitdepth = 10, tickets = [10,10,2])
                if validatepath(nn,I,U,[63,61,70], tickets = [10,10,2]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                SP = F.SearchProblem(goal = [63,99,84], model = U, auxheur=coords)
                I = [84,62,63]
                nn = SP.search(I, limitdepth = 10, tickets = [10,10,2])
                if validatepath(nn,I,U,[63,99,84], tickets = [10,10,2]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                SP = F.SearchProblem(goal = [63,99,84], model = U, auxheur=coords)
                I = [84,62,63]
                nn = SP.search(I, limitdepth = 10, tickets = [20,0,5])
                if validatepath(nn,I,U,[63,99,84], tickets = [20,0,5]):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:
                        
                #print("\n(4 val) Exercise 5 - Three agents, Limits, Any-Order")
                SP = F.SearchProblem(goal = [63,61,70], model = U, auxheur=coords)
                I = [30,40,109]
                nn = SP.search(I, limitdepth = 10, tickets = [5,20,2], anyorder = True)
                if validatepath(nn,I,U,[63,61,70], tickets = [5,20,2], anyorder = True):
                        M.append(len(nn))
                else:
                        M.append(-1)
        except:
                M.append(-1)
              
        try:

                SP = F.SearchProblem(goal = [86,96,70], model = U, auxheur=coords)
                I = [80,70,109]
                nn = SP.search(I, limitdepth = 10, tickets = [10,10,2], anyorder = True)
                if validatepath(nn,I,U,[86,96,70], tickets = [10,10,2], anyorder = True):
                        M.append(len(nn))
                else:
                        M.append(-1)

        except:
                M.append(-1)
              
        try:
                SP = F.SearchProblem(goal = [63,61,70], model = U, auxheur=coords)
                I = [30,40,109]
                nn = SP.search(I, limitdepth = 10, tickets = [10,10,2], anyorder = True)
                if validatepath(nn,I,U,[63,61,70], tickets = [10,10,2], anyorder = True):
                        M.append(len(nn))
                else:
                        M.append(-1)                
                tendtotal = time.process_time()

                M.append((tendtotal-tinittotal)*1000)
        except:
                M.append(-1)

        return M

# to test uncomment and put here you file name
file = "../ScotlandYard.py"
M = imp.load_source(file,".//"+file)
print(markproj(M))
