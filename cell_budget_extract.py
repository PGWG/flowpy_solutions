# MODLFOW CellBudgetFileExtractor.py #

# Program Exectution from the commandline 
# python cell_budget_extract.py > V38_Temp_V9.cbb.extract.RiverLeakage.txt

# koshlan@pgwg.com (November 30, 2016)
# Script Narrative: Given a transient binary MODFLOW output (.cbb), 
# extract the river flux (i.e. "RIVER LEAKAGE") values and 
# output result as:
    # TimeStep, Row, Column, Value
    


import sys
import flopy.utils.binaryfile as bf

# run paramters
n_stress_periods = 132 # ! remember 0 indexing !
idx_time_step = 4
parameter_name = "RIVER LEAKAGE"
idx_layer = 0 
delim = "\t"


# supply a binary .cbb modflow output file
cbb_filename = "/Users/Maru/Desktop/MODFLOW_HUGE/V38_Temp_V9.cbb"
cbb = bf.CellBudgetFile(cbb_filename)


rc = [] # row-column tuples [(row,column),...(row,column)]
# supply a tab-delimited filename of zero indexed row and column positions:
# row   column
# 1     2
# 2     4

river_filename = "/Users/Maru/Dropbox/JKMB001_flopy/FA128_RIVER.txt"
# This block loads the row-column indexed values identifying river cells
fh = open(river_filename , "r"); fh.readline() # skip header row
[rc.append([int(x) for x in line.strip().split(delim)]) for line in fh]

# This block loops through stress periods i to n_stress_periods, gets the data layer
for i in range(n_stress_periods):
    rec = cbb.get_data(kstpkper=(idx_time_step,i), text = parameter_name)
    layer = rec[0][idx_layer]
    for cell in rc:
        sys.stdout.write("%i,%i,%i,%f\n" %(i+1, cell[0]+1, cell[1]+1, rec[0][idx_layer][cell[0], cell[1]]))
