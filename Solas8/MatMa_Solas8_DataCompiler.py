import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import subprocess as sp

listDir = "ls -1 -d */"
Dir = sp.check_output(listDir, shell=True, universal_newlines=True, text=True).strip()

assays = Dir.splitlines()

#def sanatize input
# may want to change the formatting of the user input: print the prompt, list the options, then call input()
def userinput(options, userPrompt):
    for i in range(len(options)):
        print(i+1,':', options[i])
    while True:
        try:
            output = int(input('Please type in the number of the data to {}:'.format(userPrompt)))
            if isinstance(output, int):
                #change to 0 count scale
                output = output - 1
                #there is a bug here. giving a 0 or negative number will rollover the list
                while len(options) <= output:
                    output = int(input('Not a valid selection. Please type the number of the data to {}:'.format(userPrompt)))
                break
        except ValueError:
            print('Not a Number. Please type the Number of the data to {}:'.format(userPrompt))
    return options.pop(output)


print('Available Assays:')
selAssay = userinput(assays, 'use')
print(selAssay, 'Assay Selected.')

# Import Data

#list Assay folders
changeDir = "ls -1 "+selAssay

listRuns=sp.check_output(changeDir, shell=True, universal_newlines=True, text=True)
print(listRuns)

runs = listRuns.splitlines()

#Allowing user def of columns
assembledData = pd.DataFrame() 

for run in runs:
    print('Run ID:',run)
    SOpath = selAssay+run+"/experiment/data/scanoutput.csv"
    importTable = pd.read_table(SOpath, sep=",")
    #import gain.txt and link to importTable
    IDpath = selAssay+run+"/experiment/data/gain.txt"
    fh = open(IDpath)
    contents = fh.read()
    #split the contents into a list w/ one list for each sample - samplesplit
    samplesplit = contents.split('\n\n')
    #create lists for gain.txt to be zipped to dataframe
    #moving this outside the loop as well as the zipping
    sampleIDlist = []
    tubeNumlist = []
    runIDlist = []
    
    for i in range(len(samplesplit)):
        indSplit = samplesplit[i].split('\n')
        #indSplit[0] is tube # and indSplit[1] is sampleID. need to make TUBE int as well
        tubeNum = int(indSplit[0].strip('[]').strip('Tube '))
        sampleID = indSplit[1].strip('sampleID').strip('=')
        #keep tubeNum, SampleID, and runID lists
        tubeNumlist.append(tubeNum)
        sampleIDlist.append(sampleID)
        runIDlist.append(run)
    #get len() of sampleID after split.  
    print("Number of samples in run:",len(sampleIDlist))


    #should i use an array for this?
    #zip list into dataframe
    sampleIDframe = pd.DataFrame(list(zip(sampleIDlist, tubeNumlist, runIDlist)), columns =['sampleID', 'TUBE', 'RunID']) 
    #print(sampleIDframe)
    
    #combine imported table and sampleID - THIS HAS TO BE IN THE LOOP AS WE ARE MATCHING TUBE NUMBER
    importTableID = importTable.merge(sampleIDframe, left_on='TUBE', right_on='TUBE')
    #print(importTableID)
    #now add to global table with run name!
    assembledData=assembledData.append(importTableID, ignore_index= True)
    print('Appended',run, 'to aggregate table.')
    
#ADAPT THIS TO PULL FROM THE DATAFRAME
variableNum = []
#print(assembledData.at[0,'sampleID'])
for i in range(len(assembledData.index)):
    #to grab a specific element:
    #dataframe.loc[row_name, column_name]
    splitID=assembledData.at[i,'sampleID'].split('_')
    #print(splitID)
    variableNum.append(len(splitID))
    #print(len(splitID), "Variables Found in",sampleIDlist[i])

variableNum = np.array(variableNum)
uniqueVar = np.unique(variableNum)
sampleIDonly = assembledData['sampleID'].unique()

print("There are samples with the following lengths:",int(uniqueVar))
print('Random Subset of 5 IDs:')
randomSub = np.unique(np.random.choice(sampleIDonly, 5))
for i in range(4):
    print('\t', randomSub[i])
    
colNames = ['sampleID']
if len(uniqueVar) == 1:
    for i in range(int(uniqueVar)):
        colName = input('Assign Name to part '+str(i+1)+':')
        colNames.append(colName)
        print(colName, 'Assigned to column', i+1)
else:
    print("else")
    #still need to write code to work through the different lengths

#now that we have to add data to the columns

#create Array with column headers 
sampleIDinfo = pd.DataFrame(columns = colNames)

for i in range(len(assembledData.index)):
    sampleInfo = []
    sampleInfo.append(assembledData.at[i,'sampleID'])
    splitID=assembledData.at[i,'sampleID'].split('_')
    for i in range(len(splitID)):
        sampleInfo.append(splitID[i])
    #convert to series
    seriesConv = pd.Series(sampleInfo, index = sampleIDinfo.columns)
    #append series to the array
    sampleIDinfo = sampleIDinfo.append(seriesConv, ignore_index = True)

#merge array
assembledData = assembledData.merge(sampleIDinfo, left_on='sampleID', right_on='sampleID')
    
assembledData.to_csv('assembledData.csv')

print(".csv Exported.")

# Define graph variables:
columns = assembledData.columns.tolist()

#sanatize input for X axis
x = userinput(columns, 'use as x-axis')
print(x, 'selected as x-axis.')

#sanatize input for Y axis
y = userinput(columns, 'use as y-axis')
print(y, 'selected as y-axis.')

#do i still need to create subOptions?
subOptions = columns

#Subsetting of data: removed y and x from potential subsetting options
# X and why are already removed when selecting x and y axis with function
#subOptions.remove(y)
#subOptions.remove(x)

while True:
  try:
    subset = input('Would you like to subset your graphs? (y/n): ').lower()
    if subset == "y":  #optional
        print('Subsetting Graphs:')
        
        
        #Define Column Subset
        colSub = userinput(columns, 'subset graphs by columns')
        colUniq = assembledData[colSub].unique()
        #ensure that there aren't more than 10 potential columns
        while len(colUniq) > 10:
            print("Subsetting by your selection would create more than 10 columns of graphs. Please select a different column:")
            colSub = userinput(columns, 'subset graphs by columns')
            colUniq = assembledData[colSub].unique()
            
        print(len(colUniq), "Unique variables found.") 
        try: 
            for i in range(len(rowUniq)):
                colUniq[i] = int(colUniq[i])
        
        except ValueError:
            pass
        colUniq.sort()
        for i in range(len(colUniq)):
            print(i+1,':',colUniq[i])
        print("Subsetting graph into",len(colUniq), "columns.\n")
        # Define Row Subset
        rowSub = userinput(columns, 'subset graphs by rows')
        rowUniq = assembledData[rowSub].unique()
        #ensure that there aren't more than 10 potential rows
        while len(rowUniq) > 10:
            print("Subsetting by your selection would create more than 10 rows of graphs. Please select a different column:")
            rowSub = userinput(columns, 'subset graphs by rows')
            rowUniq = assembledData[rowSub].unique()
            #if can be converted to int, it will and then sort
        print(len(rowUniq), "Unique variables found.")
        try: 
            for i in range(len(rowUniq)):
                rowUniq[i] = int(rowUniq[i])
        except ValueError:
            pass
        rowUniq.sort()
        for i in range(len(rowUniq)):
            print(i+1,':',rowUniq[i])
        print("Subsetting graph into",len(rowUniq), "rows.\n")
            
        break
    elif subset == "n":
        print('No Data Subsetting')
        break
    else:
        print('Please type y or n: ')
  except TypeError:
    print("Please type y or n: ")


rowUniq.sort()
print("x:", x, "y:", y, "colSub:", colSub, "rowSub:", rowSub, 'colUniq:',colUniq,'rowUniq:', rowUniq)

# Define graph variables:
columns = assembledData.columns.tolist()

#sanatize input for X axis
x = userinput(columns, 'use as x-axis')
print(x, 'selected as x-axis.')

#sanatize input for Y axis
y = userinput(columns, 'use as y-axis')
print(y, 'selected as y-axis.')

#do i still need to create subOptions?
subOptions = columns


print('Subsetting Graphs:')


#Define Column Subset
colSub = userinput(columns, 'subset graphs by columns')
colUniq = assembledData[colSub].unique()
#ensure that there aren't more than 10 potential columns
while len(colUniq) > 10:
    print("Subsetting by your selection would create more than 10 columns of graphs. Please select a different column:")
    colSub = userinput(columns, 'subset graphs by columns')
    colUniq = assembledData[colSub].unique()

print(len(colUniq), "Unique variables found.") 
try: 
    for i in range(len(rowUniq)):
        colUniq[i] = int(colUniq[i])

except ValueError:
    pass
colUniq.sort()
for i in range(len(colUniq)):
    print(i+1,':',colUniq[i])
print("Subsetting graph into",len(colUniq), "columns.\n")
# Define Row Subset
rowSub = userinput(columns, 'subset graphs by rows')
rowUniq = assembledData[rowSub].unique()
#ensure that there aren't more than 10 potential rows
while len(rowUniq) > 10:
    print("Subsetting by your selection would create more than 10 rows of graphs. Please select a different column:")
    rowSub = userinput(columns, 'subset graphs by rows')
    rowUniq = assembledData[rowSub].unique()
    #if can be converted to int, it will and then sort
print(len(rowUniq), "Unique variables found.")
try: 
    for i in range(len(rowUniq)):
        rowUniq[i] = int(rowUniq[i])
except ValueError:
    pass
rowUniq.sort()
for i in range(len(rowUniq)):
    print(i+1,':',rowUniq[i])
print("Subsetting graph into",len(rowUniq), "rows.\n")

#Graphing
fig = plt.figure(figsize=(12,24))
fig, axs = plt.subplots(len(rowUniq), len(colUniq), figsize=(25,20), sharex='all', sharey='all')

#going through columns
for col in range(len(colUniq)):
    #going through rows
    for row in range(len(rowUniq)):
        #GSS allele
        GSSsub = assembledData.query("(`{0}` == '{1}') & (`{2}` == '{3}') & (CHANNEL == 3)"
                                     .format(colSub, colUniq[col], rowSub, rowUniq[row]))
        GSSxVal = GSSsub[x].tolist()
        GSSyVal = GSSsub[y].tolist()
        axs[row, col].plot(GSSxVal, GSSyVal, 'b.', label='GSS Allele')
        #WT Allele
        WTsub = assembledData.query("(`{0}` == '{1}') & (`{2}` == '{3}') & (CHANNEL == 2)"
                                     .format(colSub, colUniq[col], rowSub, rowUniq[row]))
        WTxVal = WTsub[x].tolist()
        WTyVal = WTsub[y].tolist()
        axs[row, col].plot(WTxVal, WTyVal, 'r.', label='WT Allele')
        axs[row, col].set_title('{0}: {1}, {2}: {3}'.format(colSub, colUniq[col], rowSub, rowUniq[row]))
        
#adding labels to graph
axs[0, 0].legend(loc='upper left')
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("{0}".format(x))
plt.ylabel("{0}".format(y))

plt.savefig('MatMa_AgeSignal.png',format='png')