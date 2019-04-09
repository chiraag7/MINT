import yaml
import requests
import json
import re

# Given yaml file, dataset and resource, display layout and mapping on UI


serverURL = "https://mira.isi.edu"

with open("Livestock_Loss.yaml", 'r') as stream:
    dataMap = yaml.safe_load(stream)

layout = dataMap["layout"]
mappings = dataMap["mappings"]

loginPayload = {
    "email": "tester",
    "password": "tester123"
}

# monthPayload = {
#     "id": "month",
#     "value": "literal",
#     "sorted": "null",
#     "type": "unspecified",
#     "unique": False,
#     "missing_values": [],
#     "location": {"resource_id": "live stock",
#                  "slices": [{"type": "index_slice", "idx": 0},
#                             {"type": "range_slice", "start": 1, "end": None, "step": 1}]}
# }

# mappingPayload = [
#     {
#         "type": "dimension_mapping",
#         "source_var": "loss_percentage",
#         "target_var": "reason",
#         "source_dims": [0],
#         "target_dims": [0]
#     },
#     {
#         "type": "dimension_mapping",
#         "source_var": "loss_percentage",
#         "target_var": "month",
#         "source_dims": [1],
#         "target_dims": [1]
#     }
# ]


def generate_mapping_id_and_index():
    mapping_pair = list()

    mapping_item_array = str(one2one).split("<->")
    for i in range(2):
        item1 = mapping_item_array[i]
        arr = item1.split(":")
        item1_id = arr[0].strip()
        item1_index = arr[1].strip()
        mapping_pair.append((item1_id, int(item1_index)))

    return mapping_pair


def generate_slice_json(index_description):
    match = re.search("\\.\\.", index_description)
    if match is None:
        item = {"type": "index_slice", "idx": int(index_description)}
    else:
        start_and_end = index_description.split("..")
        start = int(start_and_end[0])
        end = None
        if start_and_end[1] != "":
            print("not empty string")
            end = int(start_and_end[1])
        item = {"type": "range_slice", "start": start, "end": end, "step": 1}

    return item


# login
response = requests.post(serverURL + "/login", data=json.dumps(loginPayload))
if response.status_code == 200:
    json_data = json.loads(response.text)
    print(json_data)
    authToken = json_data["auth_token"]

    response = requests.get(serverURL + "/datasets/draft", headers={'Authorization': authToken})
    json_data = json.loads(response.text)
    resources = json_data["resources"]
    resourceId = list(resources.keys())[0]
    # print(resourceId)

    # create variables
    for variableId in layout:
        layoutDescription = layout[variableId]["location"]
        arr = str(layoutDescription).split(":")
        x = arr[0]
        y = arr[1]
        itemX = generate_slice_json(x)
        itemY = generate_slice_json(y)

        resourcePayload = {
            "id": variableId,
            "value": "literal",
            "sorted": "null",
            "type": "unspecified",
            "unique": False,
            "missing_values": [],
            "location": {"resource_id": resourceId,
                         "slices": [itemX, itemY]}
        }

        response = requests.post(serverURL + "/datasets/draft/variables", headers={'Authorization': authToken},
                                 data=json.dumps(resourcePayload))
        json_data = json.loads(response.text)
        print("create variables: " + str(json_data))

    # create mappings
    mappingPayload = []
    for mapping in mappings:
        mappingType = mapping["type"]
        one2one = mapping["one2one"]

        mappingPair = generate_mapping_id_and_index()
        itemPayload = {
            "type": mappingType,
            "source_var": mappingPair[0][0],
            "target_var": mappingPair[1][0],
            "source_dims": [mappingPair[0][1]],
            "target_dims": [mappingPair[1][1]]
        }
        mappingPayload.append(itemPayload)

    response = requests.post(serverURL + "/datasets/draft/mappings", headers={'Authorization': authToken},
                             data=json.dumps(mappingPayload))
    json_data = json.loads(response.text)
    print("create mappings: " + str(json_data))
