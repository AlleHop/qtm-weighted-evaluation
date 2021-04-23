import networkit as nk
import pandas as pd


def contractMover (G, init, sortPath, random, subtreeMove, subtreeSortPath, maxPlateau, maxIterations,bucketQueue, insertEditCost, removeEditCost, weightMatrix):
    handled = [False for i in range(G.numberOfNodes())]
    inSimplePath = [[0 for i in range(G.numberOfNodes())] for j in range(G.numberOfNodes())]
    nk.setSeed(0, False)
    if(weightMatrix == None):
        mover = nk.community.QuasiThresholdEditingLocalMover(G, init, maxIterations, sortPath, random, subtreeMove, subtreeSortPath, maxPlateau, True, insertEditCost, removeEditCost)
    else:
        mover = nk.community.QuasiThresholdEditingLocalMover(G, init, maxIterations, sortPath, random, subtreeMove, subtreeSortPath, maxPlateau, True, 1, 1, weightMatrix)
    mover.run()
    Tree = mover.getDynamicForestGraph()
    for u in Tree.iterNodes(): 
        if  not handled[u]:
            handled[u] = True
            v = u
            w = u
            while G.degreeOut(v) == 1:
                for x in G.iterNeighbors(v):
                    v = x
                handled[v] = True
                inSimplePath[u][v] +=1
                inSimplePath[v][u] +=1
            ##while G.degreeIn(w) == 1:
            #    for y in G.iterInNeighbors(w):
            #        w = y
            #    handled[w] = True
            #    inSimplePath[u][w] +=1
            #    inSimplePath[w][u] +=1
    print(inSimplePath)
    return mover

def contractNodes(G, weightMatrix, nodesToContract):
    print(weightMatrix)
    contractedNode = nodesToContract.pop(0)
    nodesToContract.sort(reverse=True)
    for v in nodesToContract:
        G.removeNode(v)
        weightMatrix[contractedNode] = list(map(sum, zip(weightMatrix[contractedNode],weightMatrix[v])))
    for u in G.iterNodes():
        weightMatrix[u][contractedNode] = weightMatrix[contractedNode][u]
    print(weightMatrix)
    print(G.numberOfNodes())