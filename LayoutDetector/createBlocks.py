import yaml
import sys
import getopt
import csv
from LayoutDetector.block import *
from LayoutDetector.DetectRelation import detectRelationLinks


def usage():
	print('Usage: python createBlocks.py -c <csv_file> -y <yaml_file>]')


def main(argv):
    #print("ljsbdgv : ", argv )
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
            x = nRows if ".." in x else int(x)
            y = nColumns if ".." in y else int(y)
            #type = 0
            #if ".." in x: type = 1
            #if int(x)==0: type=2
            print(range(3), x, y, b, type)
            cellLocations = [(i, j) for i in range(x+1) for j in range(y+1)]
            block = Block(cellLocations, type, str(b))
            allBlocks.append(block)

    relations = detectRelationLinks(allBlocks)
    print("\n------------------------ RELATIONS ----------------------\n")
    #print(relations)
    #print("------ Relations ------")
    for r in relations:
        if r[0] and r[1]:
            print(r[0].getName(), " <-> ", r[1].getName())
        if r[0]: print(r[0].getName())
        if r[1]: print(r[1].getName())

    return relations

if __name__ == '__main__':
	main(sys.argv[1:])