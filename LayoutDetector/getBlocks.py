'''
Generates blocks based on the cell position
(Currently works for 2D resource files)

<<<<<<< HEAD
@param inputFile: Input CSV file for which YAML
				  representation must be generated.

'''
import csv
from LayoutDetector.block import *

def getBlocks(inputFile):
    metadata = []
    data = []
    column_header = []
    row_header = []

    with open(inputFile, "r") as csvf:
        rows = csv.reader(csvf, delimiter=',')

        for i, row in enumerate(rows):
            for j, col in enumerate(row):

                if col.strip() != '':
                    if i == 0 and j == 0:
                        metadata.append((i, j))
                    elif i == 0:
                        column_header.append((i, j))
                    elif j == 0:
                        row_header.append((i, j))
                    else:
                        data.append((i, j))

    metaDataBlock = Block(metadata, 3, "metadata")
    dataBlock = Block(data, 0, "data")
    colHeaderBlock = Block(column_header, 1, "column_header")
    rowHeaderBlock = Block(row_header, 2, "row_header")
    allBlocks = [metaDataBlock, dataBlock, colHeaderBlock, rowHeaderBlock]
    return allBlocks
