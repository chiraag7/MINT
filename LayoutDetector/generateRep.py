from LayoutDetector.DetectRelation import getRelations
from LayoutDetector.getBlocks import getBlocks
import yaml

#createBlocks("-c data/FAOSTAT_South_Sudan_Food_Security_Indicators_data_2014-2016.csv -y data/FAO_STAT_South_Sudan.yaml")
""" Creates a yaml file representation using the blocks detected from BlockDetector 
and relations detected from LayoutDetector"""

def generateRepresentaion():
    detectedBlocks = getBlocks()
    detectedRelations = getRelations("data/LivestockLoss_Cattle_Warrap_2017.csv", "data/Livestock_Loss.yaml")

    layoutJson = {"version": "1",
                                    "resources":"<r_name>",
                                    "transformation": [],
                                    "layout": [],
                                    "mappings": [],
                                    "semantic_model":
                                        {
                                            "semantic_types":[],
                                            "semantic_relations":[],
                                            "ontology_prefixes":
                                                {"schema":"http://schema.org/"}
                                        }
                                    }

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