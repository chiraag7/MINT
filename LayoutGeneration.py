import csv

def generateLayout(inputFile, dimension):
    layout = {}

    with open(inputFile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ### Find out if it is 1D or 2D?
        ### ---- How to find this??? -- For, now, take as input
        if dimension==1:
            # Now, do for 1-D
            ### Find row-wise or column-wise(If 1D)?

            # Do for column-wise:
            variableRow = reader.next()
            # add these variables to layout
            for v in xrange(len(variableRow)):
                ### Find where the row ends?
                # assuming whole column for now
                layout[variableRow[v]] = {'location': str(v)+":1.."}
        if dimension==2:
            # Now, do for 2-D
            ### Find variable name for the dimensions??? - eg: Month and Year
            ### -- For now, giving names manually
            ### -- Value comes into picture now - corresponding to 2 dimensions
            layout['month']= {'location': "0:1.."}
            layout['year']={'location': "1..:0"}
            layout['value']={'location':"1..:1.."}

        return layout

print "\nGenerating layout for file with 1-D"
inputFile = "inputFiles\\2014-01-01-2017-04-30-Eastern_Africa-South_Sudan.csv"
print generateLayout(inputFile, 1)

print "\nGenerating layout for file with 2-D"
inputFile = "inputFiles\\rice_import_at_Kaya_2014-2017_data_table.csv"
print generateLayout(inputFile, 2)