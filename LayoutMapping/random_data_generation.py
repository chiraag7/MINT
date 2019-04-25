import csv
import random
import string
import yaml
from collections import OrderedDict

# variable = ["month", "year", "rainfall"]
# layout = ["0:1..", "1..:0", "1..:1.."]
# mapping = [("year:0", "rainfall:0"), ("month:1", "rainfall:1")]

# rowNum % (rowGroup * subRowNum) = 0
rowNum = 6
rowGroup = 1
subRowNum = 1
colNum = 12
colGroup = 4
subColNum = 1


# 1: percentage, 2: decimal number, 3: string
dataType = list()
totalDataType = list()

monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
dataList = list()
subColList = list()
subRowList = list()


def random_generator(size=6, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for i in range(size))


def insert_data_cell_into_list(type_index, tmp_list):
    for y in range(colNum):
        if dataType[type_index] == 1:
            data_cell = str(random.randint(0, 100)) + "%"
        elif dataType[type_index] == 2:
            data_cell = str(round(random.random(), 2))
        elif dataType[type_index] == 3:
            data_cell = random_generator()
        else:
            data_cell = random_generator()
        tmp_list.append(data_cell)

    return tmp_list


for i in range(subRowNum):
    subRowList.append("r" + str(i))


if subRowNum > 1:
    dataTypeSize = subRowNum
elif subColNum > 1:
    dataTypeSize = subColNum
else:
    dataTypeSize = max(rowGroup, colGroup)
for i in range(dataTypeSize):
    dataType.append(random.randint(1, 3))

print(dataType)

# cut horizontally
if rowGroup > 1:
    for typeIndex in range(rowGroup):
        for x in range(int((rowNum / rowGroup) / subRowNum)):
            if subRowNum > 1:
                for x2 in range(subRowNum):
                    year = random.randint(0, 101)
                    subList = list()
                    subList.append(str(year + 1918))
                    subList.append(subRowList[x2])

                    totalDataType.append(dataType[x2])
                    subList = insert_data_cell_into_list(x2, subList)
                    dataList.append(subList)
            else:
                year = random.randint(0, 101)
                subList = list()
                subList.append(str(year + 1918))

                totalDataType.append(dataType[typeIndex])
                subList = insert_data_cell_into_list(typeIndex, subList)
                dataList.append(subList)

# cut vertically
else:
    tmpDataList = list()
    subList = list()
    for y in range(rowNum):
        year = random.randint(0, 101)
        subList.append(str(year + 1918))
    tmpDataList.append(subList)

    for typeIndex in range(colGroup):
        for x in range(int((colNum / colGroup) / subColNum)):
            if subColNum > 1:
                for x2 in range(subColNum):
                    subList = list()
                    totalDataType.append(dataType[x2])
                    subList = insert_data_cell_into_list(x2, subList)
                    tmpDataList.append(subList)

            else:
                subList = list()
                totalDataType.append(dataType[typeIndex])
                subList = insert_data_cell_into_list(typeIndex, subList)
                tmpDataList.append(subList)

    # do rotation
    for y in range(rowNum):
        subList = list()
        for x in range(colNum + 1):
            subList.append(tmpDataList[x][y])

        dataList.append(subList)


print("totalDataType: " + str(totalDataType))

# write csv
outputFileName = "random_data.csv"
with open(outputFileName, "w") as fp:
    # fp.write("#,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec" + "\n")
    headerList = list()

    headerList.append("#")
    if subRowNum > 1:
        headerList.append("#")

    for i in range(int(colNum / subColNum)):
        for j in range(subColNum):
            headerList.append(monthList[i])

    # add 2-level column header
    subHeaderList = list()
    subHeaderList.append("#")
    for i in range(int(colNum / subColNum)):
        for j in range(subColNum):
            subHeaderList.append("c" + str(j))

    w = csv.writer(fp)
    w.writerow(headerList)
    if subColNum > 1:
        w.writerow(subHeaderList)
    w.writerows(dataList)


def setup_yaml():
    yaml.add_representer(OrderedDict, _represent_dictorder)


def _represent_dictorder(self, data):
    return self.represent_mapping('tag:yaml.org,2002:map', data.items())


yamlData = OrderedDict()
yamlData['version'] = '1'
yamlData['resources'] = 'csv'

layoutObj = OrderedDict()
layoutObj['month'] = {
    'location': '0:1..'
}
layoutObj['year'] = {
    'location': '1..:0'
}

# cut horizontally
block = 0
if rowGroup > 1:
    lastIndex = 1
    for i in range(1, len(totalDataType)):
        if totalDataType[i] != totalDataType[i - 1]:
            variableStr = 'rainfall_' + str(block)
            if i == lastIndex:
                layoutObj[variableStr] = {
                    'location': str(i) + ':1..'
                }
            else:
                layoutObj[variableStr] = {
                    'location': str(lastIndex) + '..' + str(i) + ':1..'
                }
            block += 1
            lastIndex = i + 1

    variableStr = 'rainfall_' + str(block)
    if lastIndex == rowNum:
        layoutObj[variableStr] = {
            'location': str(rowNum) + ':1..'
        }
    else:
        layoutObj[variableStr] = {
            'location': str(lastIndex) + '..' + str(rowNum) + ':1..'
        }
    block += 1

    yamlData['layout'] = layoutObj

# cut vertically
else:
    lastIndex = 1
    for i in range(1, len(totalDataType)):
        if totalDataType[i] != totalDataType[i - 1]:
            variableStr = 'rainfall_' + str(block)
            if i == lastIndex:
                layoutObj[variableStr] = {
                    'location': '1..:' + str(i)
                }
            else:
                layoutObj[variableStr] = {
                    'location': '1..:' + str(lastIndex) + '..' + str(i)
                }
            block += 1
            lastIndex = i + 1

    variableStr = 'rainfall_' + str(block)
    if lastIndex == colNum:
        layoutObj[variableStr] = {
            'location': '1..:' + str(colNum)
        }
    else:
        layoutObj[variableStr] = {
            'location': '1..:' + str(lastIndex) + '..' + str(colNum)
        }
    block += 1

    yamlData['layout'] = layoutObj


mappingArray = list()
for i in range(block):
    variableStr = 'rainfall_' + str(i)
    mappingObj1 = dict()
    mappingObj1['type'] = 'dimension_mapping'
    mappingObj1['one2one'] = variableStr + ':0 <-> year:0'
    mappingArray.append(mappingObj1)

    mappingObj2 = dict()
    mappingObj2['type'] = 'dimension_mapping'
    mappingObj2['one2one'] = variableStr + ':1 <-> month:1'
    mappingArray.append(mappingObj2)

yamlData['mappings'] = mappingArray


# write yaml file
with open('random_data.yml', 'w') as outfile:
    setup_yaml()
    yaml.dump(yamlData, outfile, default_flow_style=False)
