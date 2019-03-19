#from . import block
import math


class Block:
    def __init__(self, cellLocations=[], type=0, name="block"):
        """

        :param cellLocations: gives (x,y) locations of cells in the block
        :param type: gives the type of the block of cells. { Default : data }
                    { data : 0, column heading: 1, row heading: 2, metadata: 3 }
        """
        cellLocations.sort()
        self.cellLocations = cellLocations
        self.type = type
        self.name = name #"block" + str(type) + "_" + str(len(cellLocations))
    def setType(self, type):
        self.type = type
    def getType(self):
        return self.type
    def setCellLocations(self, cellLocations):
        cellLocations.sort()
        self.cellLocations = cellLocations
    def getCellLocations(self):
        return self.cellLocations
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name



def detectRelationLinks(blockList):
    """
    A data block gets relation with nearest column heading block and row heading block.
    A column heading block and row heading block gets a relation with nearest metadata block.
    :param blockList: list of Blocks
    :return:
    """

    # has tuples of connected blocks
    relationList = []

    # groups different types of block together, and stores the middle most cell for each block
    blockTypes = {0:[], 1:[], 2:[], 3:[]}
    for b in blockList:
        cells = b.getCellLocations()
        mid = cells[len(cells)//2]
        blockTypes[b.type].append((b, mid))

    # create relations for data blocks
    for dblock in blockTypes[0]:
        # relation with column headers
        minDist = (-1,None)
        for chblock in blockTypes[1]:
            dist = math.sqrt( ((dblock[1][0]-chblock[1][0])**2)+((dblock[1][1]-chblock[1][1])**2) )
            if minDist[0]==-1: minDist = (dist, chblock[0])
            elif minDist[0]>dist: minDist = (dist, chblock[0])
        relationList.append((dblock[0], minDist[1]))
        # relation with row headers
        minDist = (-1, None)
        for rhblock in blockTypes[2]:
            dist = math.sqrt( ((dblock[1][0]-rhblock[1][0])**2)+((dblock[1][1]-rhblock[1][1])**2) )
            if minDist[0]==-1: minDist = (dist, rhblock[0])
            elif minDist[0]>dist: minDist = (dist, rhblock[0])
        relationList.append((dblock[0], minDist[1]))

    # create relations for column heading blocks
    for chblock in blockTypes[1]:
        # relation with column headers
        minDist = (-1,None)
        for mdblock in blockTypes[3]:
            dist = math.sqrt( ((chblock[1][0]-mdblock[1][0])**2)+((chblock[1][1]-mdblock[1][1])**2) )
            if minDist[0]==-1: minDist = (dist, mdblock[0])
            elif minDist[0]>dist: minDist = (dist, mdblock[0])
        relationList.append((chblock[0], minDist[1]))

    # create relations for row heading blocks
    for rhblock in blockTypes[2]:
        # relation with column headers
        minDist = (-1,None)
        for chblock in blockTypes[3]:
            dist = math.sqrt( ((rhblock[1][0]-mdblock[1][0])**2)+((rhblock[1][1]-mdblock[1][1])**2) )
            if minDist[0]==-1: minDist = (dist, mdblock[0])
            elif minDist[0]>dist: minDist = (dist, mdblock[0])
        relationList.append((rhblock[0], minDist[1]))

    return relationList



block1 = Block([(0, 1), (0, 2), (0, 3), (0, 4)], 1, "ch-block")
block2 = Block([(1, 0), (2, 0), (3, 0)], 2, "rh-block")
block3 = Block([(0, 1), (0, 2), (0, 3), (0, 4)], 0, "d-block")
block4 = Block([(0, 0)], 3, "md-block")
relations = detectRelationLinks([block1, block2, block3, block4])
for r in relations:
    print(r[0].getName(), " <-> ", r[1].getName())