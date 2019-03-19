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
        self.name = name #"block"+str(type)+"_"+str(len(cellLocations))
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
