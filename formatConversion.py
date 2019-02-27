### Convert representations from Arun's to Bihn's

import json
import re
import os

def mapChar(c):
    # convert excel letter cell names to indices
    return str((len(c) - 1) * 26 + ord(c[-1]) - 65)

def mapNum(n):
    # convert excel numbers to indices
    return int(n)-1

def getBlockRange(low, high):
    # Block is group of cells that are found to be similar.
    # return the boundaries of them in Bhin's format.
    indexes = re.split('(\d+)', low)
    lrow = str(mapNum(indexes[1]))
    lcolumn = str(mapChar(indexes[0]))
    indexes = re.split('(\d+)', high)
    hrow = str(mapNum(indexes[1]))
    hcolumn = str(mapChar(indexes[0]))
    if lrow==hrow: # 1-D row
        return lrow + ":"+lcolumn+".."+hcolumn
    if lcolumn==hcolumn: # 1-D column
        return lrow+".."+hrow+":"+lcolumn
    return lrow+".."+hrow+":"+lcolumn+".."+hcolumn

# Search through the folders to find the json files and convert the layout representation of each

path = ".\\Dataset\\annotated_files"
for root, dirs, fs in os.walk(path, topdown=False):
    for name in dirs:
        print(os.path.join(root, name))
        for rt, d, files in os.walk(os.path.join(root, name), topdown=False):
            for filename in files:
                if re.match('annotation.json', filename):
                    with open(path+"\\"+name+"\\"+filename) as ann:
                        annData = json.load(ann)
                        for key in annData:
                            print(key, type(annData), name)
                            jsonData = annData[key]["regions"][0]["labels"]
                            layoutJson = {"layout": []}

                            for block in jsonData:
                                range = block["range"]
                                label = block["label"]
                                low, high = range.split(":")
                                blockRange = getBlockRange(low, high)
                                labelLoc = {"location": blockRange}
                                layoutJson["layout"].append({label: labelLoc})

                            with open('.\\Dataset\\annotated_files\\'+name+'\\bihnsRep'+key+'.txt','w') as output:
                                output.write(json.dumps(layoutJson, indent=4, sort_keys=True))
