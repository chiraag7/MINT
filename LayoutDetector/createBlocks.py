import yaml
import sys
import getopt
import csv
from LayoutDetector.block import *

def usage():
	print('Usage: python createBlocks.py -c <csv_file> -y <yaml_file>]')


def createBlocks(inputFile, yamlFile):
    """ Creats block from yaml files. Can be used for validating/testing the model """
    nColumns = 0
    nRows = 0
    allBlocks = []
    with open(inputFile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
        nColumns = len(data[0])
        nRows = len(data)
        #print(nColumns, nRows)
    with open(yamlFile) as yamlFile:
        data = yaml.load(yamlFile)
        for b in data['layout']:
            x, y = data['layout'][b]['location'].split(":")
            type = 0
            if ".." in x: type = 1
            if ".." in y: type = 2
            if ".." in y and ".." in x: type = 0
            x = nRows if ".." in x else int(x)
            y = nColumns if ".." in y else int(y)
            #type = 0
            #if ".." in x: type = 1
            #if int(x)==0: type=2
            print(range(3), x, y, b, type)
            cellLocations = [(i, j) for i in range(x+1) for j in range(y+1)]
            block = Block(cellLocations, type, str(b))
            allBlocks.append(block)

    return allBlocks

if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        options, args = getopt.getopt(argv, "hc:y:")
    except getopt.GetoptError:
        print('Incorrect usage')
        usage()
        sys.exit(2)

    for option, arg in options:
        if option == 'h':
            usage()
            sys.exit()
        if option in ("-c"):
            inputFile = arg
        elif option in ("-y"):
            yamlFile = arg
    createBlocks(inputFile, yamlFile)