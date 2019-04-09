from LayoutDetector.DetectRelation import getRelations
from LayoutDetector.getBlocks import getBlocks
import yaml

#createBlocks("-c data/FAOSTAT_South_Sudan_Food_Security_Indicators_data_2014-2016.csv -y data/FAO_STAT_South_Sudan.yaml")
""" Creates a yaml file representation using the blocks detected from BlockDetector 
and relations detected from LayoutDetector"""

def generateRepresentaion():
    detectedBlocks = getBlocks("data/LivestockLoss_Cattle_Warrap_2017.csv")
    detectedRelations = getRelations("data/LivestockLoss_Cattle_Warrap_2017.csv", "data/Livestock_Loss.yaml")

    layoutJson = {
                "version": "1",
                "resources":"<r_name>",
                "transformation": [],
                "layout": [],
                "mappings": [],
                "semantic_model":{
                    "semantic_types":[],
                    "semantic_relations":[],
                    "ontology_prefixes":{"schema":"http://schema.org/"}
                    }
                }
    for block in detectedBlocks:
        layoutJson["layout"][block.name] = "0:1.."
    #print("detectedRelations : ", detectedRelations)
    for relation in detectedRelations:
        if relation[0] and relation[1]:
            mapping = {
                    "type": "dimension_mapping",
                    "one2one": ''.join([relation[0].getName(),":0 <-> ", relation[1].getName(), ": 0"])
                   }
            layoutJson['mappings'].append(mapping)

    print("\n-------------------- REPRESENTATION -----------------------\n")
    print(layoutJson)
    return layoutJson

representaion = generateRepresentaion()
with open('representaion.yml', 'w') as output:
    yaml.dump(representaion, output, default_flow_style=False)


def getDotNotation(cellLocations):
    mini = cellLocations[0][0]
    minj = cellLocations[0][1]
    samei = True
    samej = True
    previ, prevj = mini, minj
    for i,j in cellLocations[1:]:
        if i < mini:
            mini = i
        if j < minj:
            minj = j
        if prevj != j:
            samej = False
        if previ != i:
            samei = False
    string = str(mini)
    if !samei:
        string += ".."
    string += ":" + str(minij)
    if !samej:
        string += ".."
    return string