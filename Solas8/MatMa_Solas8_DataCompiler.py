import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import subprocess as sp

#Select assay

listDir = "ls -1 -d */"
Dir = sp.check_output(listDir, shell=True, universal_newlines=True, text=True).strip()

assays = Dir.splitlines()
print('Available Assays:')
num = 1
for i in assays:
    print(num,': ',i)
    num = num +1
    
#sanatize input
while True:
  try:
    assay = int(input('Please Type in the number of your desired assay: '))
    if isinstance(assay, int):  #optional
        #change to 0 count scale
        assay = assay-1
        while len(assays) <= assay:
            assay = int(input('Not a valid selection. Please type the number of your desired assay: '))
        break
  except ValueError:
    print("Not a Number. Please type the Number of your desired assay: ")
selAssay = assays[assay].strip()
print(assays[assay], 'Assay Selected.')

# Import Data

#list Assay folders
changeDir = "ls -1 "+selAssay

listRuns=sp.check_output(changeDir, shell=True, universal_newlines=True, text=True)
print(listRuns)

runs = listRuns.splitlines()
print(runs)

#import table
#SO stands for scanoutput
assembledData = pd.DataFrame() 

for run in runs:
    print('Run ID:',run)
    SOpath = assays[assay]+run+"/experiment/data/scanoutput.csv"
    importTable = pd.read_table(SOpath, sep=",")
#import gain.txt and link to importTable
    IDpath = assays[assay]+run+"/experiment/data/gain.txt"
    fh = open(IDpath)
    contents = fh.read()
    #split the contents into a list w/ one list for each sample - samplesplit
    samplesplit = contents.split('\n\n')
    #create lists for gain.txt to be zipped to dataframe
    sampleIDlist = []
    tubeNumlist = []
    runIDlist = []
    daylist = []
    sampletypelist = []
    #add sample ID and tubeNum to list for all samples in gain.txt
    for i in range(len(samplesplit)):
        indSplit = samplesplit[i].split('\n')
        #indSplit[0] is tube # and indSplit[1] is sampleID. need to make TUBE int as well
        tubeNum = int(indSplit[0].strip('[]').strip('Tube '))
        sampleID = indSplit[1].strip('sampleID=')
        
        if sampleID.find("Leg") > -1:
            sampleType = "Leg"
        elif sampleID.find("Rearing") > -1:
            sampleType = "Rearing"
        elif sampleID.find("FemaleDTWP") > -1:
            sampleType = "Female DTWP"
        elif sampleID.find("MaleDTWP") > -1:
            sampleType = "Male DTWP"
        else:
            sampleType = "NA"
        
        day = sampleID.split('-d')
        if len(day) != 2:
            day.append('0')
            #NA day assigned to 0 to allow for creation of integer from Day
        day = int(day[1])
        tubeNumlist.append(tubeNum)
        sampleIDlist.append(sampleID)
        runIDlist.append(run)
        daylist.append(day)
        sampletypelist.append(sampleType)
        
    print("Number of samples in run:",len(sampleIDlist))

    #zip list into dataframe
    sampleIDframe = pd.DataFrame(list(zip(sampleIDlist, tubeNumlist, runIDlist, daylist, sampletypelist)), columns =['sampleID', 'TUBE', 'RunID', 'Day', 'SampleType']) 
    #print(sampleIDframe)
    
    #combine imported table and sampleID 
    importTableID = importTable.merge(sampleIDframe, left_on='TUBE', right_on='TUBE')
    #print(importTableID)
    #now add to global table with run name!
    assembledData=assembledData.append(importTableID)
    print('Appended',run, 'to aggregate table.')
    
#print(assembledData)
assembledData.to_csv('assembledData.csv')
#IT WORKS!!!!


#subsetting Data: assembledData

#day1subset
    #DTWP male
day1DTWPmaleGSSa = assembledData.loc[ (assembledData.Day == 1) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Male DTWP")]
day1DTWPmaleWTa = assembledData.loc[ (assembledData.Day == 1) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Male DTWP")]

#print(type(day1DTWPmaleGSSa))
#day1DTWPmaleGSSa.to_csv('day1DTWPmaleGSSa.csv')

x0_0gss = day1DTWPmaleGSSa['TIME'].tolist()
y0_0gss = day1DTWPmaleGSSa['SIGNAL'].tolist()

x0_0wt = day1DTWPmaleWTa['TIME'].tolist()
y0_0wt = day1DTWPmaleWTa['SIGNAL'].tolist()

    #DTWP Female
day1DTWPfemaleGSSa = assembledData.loc[ (assembledData.Day == 1) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Female DTWP")]
day1DTWPfemaleWTa = assembledData.loc[ (assembledData.Day == 1) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Female DTWP")]

x0_1gss = day1DTWPfemaleGSSa['TIME'].tolist()
y0_1gss = day1DTWPfemaleGSSa['SIGNAL'].tolist()

x0_1wt = day1DTWPfemaleWTa['TIME'].tolist()
y0_1wt = day1DTWPfemaleWTa['SIGNAL'].tolist()

    #WT
day1RearingGSSa = assembledData.loc[ (assembledData.Day == 1) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Rearing")]
day1RearingWTa = assembledData.loc[ (assembledData.Day == 1) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Rearing")]

x0_2gss = day1RearingGSSa['TIME'].tolist()
y0_2gss = day1RearingGSSa['SIGNAL'].tolist()

x0_2wt = day1RearingWTa['TIME'].tolist()
y0_2wt = day1RearingWTa['SIGNAL'].tolist()


#day7subset
   #DTWP male
day7DTWPmaleGSSa = assembledData.loc[ (assembledData.Day == 7) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Male DTWP")]
day7DTWPmaleWTa = assembledData.loc[ (assembledData.Day == 7) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Male DTWP")]

x1_0gss = day7DTWPmaleGSSa['TIME'].tolist()
y1_0gss = day7DTWPmaleGSSa['SIGNAL'].tolist()

x1_0wt = day7DTWPmaleWTa['TIME'].tolist()
y1_0wt = day7DTWPmaleWTa['SIGNAL'].tolist()

    #DTWP Female
day7DTWPfemaleGSSa = assembledData.loc[ (assembledData.Day == 7) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Female DTWP")]
day7DTWPfemaleWTa = assembledData.loc[ (assembledData.Day == 7) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Female DTWP")]

x1_1gss = day7DTWPfemaleGSSa['TIME'].tolist()
y1_1gss = day7DTWPfemaleGSSa['SIGNAL'].tolist()

x1_1wt = day7DTWPfemaleWTa['TIME'].tolist()
y1_1wt = day7DTWPfemaleWTa['SIGNAL'].tolist()

    #WT
day7RearingGSSa = assembledData.loc[ (assembledData.Day == 7) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Rearing")]
day7RearingWTa = assembledData.loc[ (assembledData.Day == 7) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Rearing")]

x1_2gss = day7RearingGSSa['TIME'].tolist()
y1_2gss = day7RearingGSSa['SIGNAL'].tolist()

x1_2wt = day7RearingWTa['TIME'].tolist()
y1_2wt = day7RearingWTa['SIGNAL'].tolist()


#Day14 subset
   #DTWP male
day14DTWPmaleGSSa = assembledData.loc[ (assembledData.Day == 14) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Male DTWP")]
day14DTWPmaleWTa = assembledData.loc[ (assembledData.Day == 14) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Male DTWP")]

x2_0gss = day14DTWPmaleGSSa['TIME'].tolist()
y2_0gss = day14DTWPmaleGSSa['SIGNAL'].tolist()

x2_0wt = day14DTWPmaleWTa['TIME'].tolist()
y2_0wt = day14DTWPmaleWTa['SIGNAL'].tolist()

    #DTWP Female
day14DTWPfemaleGSSa = assembledData.loc[ (assembledData.Day == 14) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Female DTWP")]
day14DTWPfemaleWTa = assembledData.loc[ (assembledData.Day == 14) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Female DTWP")]

x2_1gss = day14DTWPfemaleGSSa['TIME'].tolist()
y2_1gss = day14DTWPfemaleGSSa['SIGNAL'].tolist()

x2_1wt = day14DTWPfemaleWTa['TIME'].tolist()
y2_1wt = day14DTWPfemaleWTa['SIGNAL'].tolist()

    #WT
day14RearingGSSa = assembledData.loc[ (assembledData.Day == 14) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Rearing")]
day14RearingWTa = assembledData.loc[ (assembledData.Day == 14) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Rearing")]

x2_2gss = day14RearingGSSa['TIME'].tolist()
y2_2gss = day14RearingGSSa['SIGNAL'].tolist()

x2_2wt = day14RearingWTa['TIME'].tolist()
y2_2wt = day14RearingWTa['SIGNAL'].tolist()


#day21subset
   #DTWP male
day21DTWPmaleGSSa = assembledData.loc[ (assembledData.Day == 21) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Male DTWP")]
day21DTWPmaleWTa = assembledData.loc[ (assembledData.Day == 21) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Male DTWP")]

x3_0gss = day21DTWPmaleGSSa['TIME'].tolist()
y3_0gss = day21DTWPmaleGSSa['SIGNAL'].tolist()

x3_0wt = day21DTWPmaleWTa['TIME'].tolist()
y3_0wt = day21DTWPmaleWTa['SIGNAL'].tolist()

    #DTWP Female
day21DTWPfemaleGSSa = assembledData.loc[ (assembledData.Day == 21) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Female DTWP")]
day21DTWPfemaleWTa = assembledData.loc[ (assembledData.Day == 21) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Female DTWP")]

x3_1gss = day21DTWPfemaleGSSa['TIME'].tolist()
y3_1gss = day21DTWPfemaleGSSa['SIGNAL'].tolist()

x3_1wt = day21DTWPfemaleWTa['TIME'].tolist()
y3_1wt = day21DTWPfemaleWTa['SIGNAL'].tolist()

    #WT
day21RearingGSSa = assembledData.loc[ (assembledData.Day == 21) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Rearing")]
day21RearingWTa = assembledData.loc[ (assembledData.Day == 21) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Rearing")]

x3_2gss = day21RearingGSSa['TIME'].tolist()
y3_2gss = day21RearingGSSa['SIGNAL'].tolist()

x3_2wt = day21RearingWTa['TIME'].tolist()
y3_2wt = day21RearingWTa['SIGNAL'].tolist()


#day28subset
   #DTWP male
day28DTWPmaleGSSa = assembledData.loc[ (assembledData.Day == 28) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Male DTWP")]
day28DTWPmaleWTa = assembledData.loc[ (assembledData.Day == 28) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Male DTWP")]

x4_0gss = day28DTWPmaleGSSa['TIME'].tolist()
y4_0gss = day28DTWPmaleGSSa['SIGNAL'].tolist()

x4_0wt = day28DTWPmaleWTa['TIME'].tolist()
y4_0wt = day28DTWPmaleWTa['SIGNAL'].tolist()

    #DTWP Female
day28DTWPfemaleGSSa = assembledData.loc[ (assembledData.Day == 28) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Female DTWP")]
day28DTWPfemaleWTa = assembledData.loc[ (assembledData.Day == 28) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Female DTWP")]

x4_1gss = day28DTWPfemaleGSSa['TIME'].tolist()
y4_1gss = day28DTWPfemaleGSSa['SIGNAL'].tolist()

x4_1wt = day28DTWPfemaleWTa['TIME'].tolist()
y4_1wt = day28DTWPfemaleWTa['SIGNAL'].tolist()

    #WT
day28RearingGSSa = assembledData.loc[ (assembledData.Day == 28) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Rearing")]
day28RearingWTa = assembledData.loc[ (assembledData.Day == 28) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Rearing")]

x4_2gss = day28RearingGSSa['TIME'].tolist()
y4_2gss = day28RearingGSSa['SIGNAL'].tolist()

x4_2wt = day28RearingWTa['TIME'].tolist()
y4_2wt = day28RearingWTa['SIGNAL'].tolist()


#day35subset
   #DTWP male
day35DTWPmaleGSSa = assembledData.loc[ (assembledData.Day == 35) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Male DTWP")]
day35DTWPmaleWTa = assembledData.loc[ (assembledData.Day == 35) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Male DTWP")]

x5_0gss = day35DTWPmaleGSSa['TIME'].tolist()
y5_0gss = day35DTWPmaleGSSa['SIGNAL'].tolist()

x5_0wt = day35DTWPmaleWTa['TIME'].tolist()
y5_0wt = day35DTWPmaleWTa['SIGNAL'].tolist()

    #DTWP Female
day35DTWPfemaleGSSa = assembledData.loc[ (assembledData.Day == 35) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Female DTWP")]
day35DTWPfemaleWTa = assembledData.loc[ (assembledData.Day == 35) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Female DTWP")]

x5_1gss = day35DTWPfemaleGSSa['TIME'].tolist()
y5_1gss = day35DTWPfemaleGSSa['SIGNAL'].tolist()

x5_1wt = day35DTWPfemaleWTa['TIME'].tolist()
y5_1wt = day35DTWPfemaleWTa['SIGNAL'].tolist()

    #WT
day35RearingGSSa = assembledData.loc[ (assembledData.Day == 35) & (assembledData.CHANNEL == 3) & (assembledData.SampleType == "Rearing")]
day35RearingWTa = assembledData.loc[ (assembledData.Day == 35) & (assembledData.CHANNEL == 2) & (assembledData.SampleType == "Rearing")]

x5_2gss = day35RearingGSSa['TIME'].tolist()
y5_2gss = day35RearingGSSa['SIGNAL'].tolist()

x5_2wt = day35RearingWTa['TIME'].tolist()
y5_2wt = day35RearingWTa['SIGNAL'].tolist()

fig = plt.figure(figsize=(12,24))
fig, axs = plt.subplots(6, 3, figsize=(25,20), sharex='col', sharey='row')

#column 1
axs[0, 0].plot(x0_0gss, y0_0gss, 'b.', label='GSS Allele')
axs[0, 0].plot(x0_0wt, y0_0wt, 'r.', label ='WT Allele')

axs[0, 0].set_title('DTWP Male Day 1')
axs[0, 0].set_ylabel('Signal')
axs[0, 0].legend(loc='upper left')


axs[1, 0].plot(x1_0gss, y1_0gss, 'b.')
axs[1, 0].plot(x1_0wt, y1_0wt, 'r.')
axs[1, 0].set_title('DTWP Male Day 7')
axs[1, 0].set_ylabel('Signal')


axs[2, 0].plot(x2_0gss, y2_0gss, 'b.')
axs[2, 0].plot(x2_0wt, y2_0wt, 'r.')
axs[2, 0].set_title('DTWP Male Day 14')
axs[2, 0].set_ylabel('Signal')


axs[3, 0].plot(x3_0gss, y3_0gss, 'b.')
axs[3, 0].plot(x3_0wt, y3_0wt, 'r.')
axs[3, 0].set_title('DTWP Male Day 21')
axs[3, 0].set_ylabel('Signal')


axs[4, 0].plot(x4_0gss, y4_0gss, 'b.')
axs[4, 0].plot(x4_0wt, y4_0wt, 'r.')
axs[4, 0].set_title('DTWP Male Day 28')
axs[4, 0].set_ylabel('Signal')


axs[5, 0].plot(x5_0gss, y5_0gss, 'b.')
axs[5, 0].plot(x5_0wt, y5_0wt, 'r.')
axs[5, 0].set_title('DTWP Male Day 35')
axs[5, 0].set_xlabel('Time (Minutes)')
axs[5, 0].set_ylabel('Signal')


#column 2
axs[0, 1].plot(x0_1gss, y0_1gss, 'b.')
axs[0, 1].plot(x0_1wt, y0_1wt, 'r.')
axs[0, 1].set_title('DTWP Female Day 1')

axs[1, 1].plot(x1_1gss, y1_1gss, 'b.')
axs[1, 1].plot(x1_1wt, y1_1wt, 'r.')
axs[1, 1].set_title('DTWP Female Day 7')

axs[2, 1].plot(x2_1gss, y2_1gss, 'b.')
axs[2, 1].plot(x2_1wt, y2_1wt, 'r.')
axs[2, 1].set_title('DTWP Female Day 14')

axs[3, 1].plot(x3_1gss, y3_1gss, 'b.')
axs[3, 1].plot(x3_1wt, y3_1wt, 'r.')
axs[3, 1].set_title('DTWP Female Day 21')

axs[4, 1].plot(x4_1gss, y4_1gss, 'b.')
axs[4, 1].plot(x4_1wt, y4_1wt, 'r.')
axs[4, 1].set_title('DTWP Female Day 28')

axs[5, 1].plot(x5_1gss, y5_1gss, 'b.')
axs[5, 1].plot(x5_1wt, y5_1wt, 'r.')
axs[5, 1].set_title('DTWP Female Day 35')
axs[5, 1].set_xlabel('Time (Minutes)')


#column 3
axs[0, 2].plot(x0_2gss, y0_2gss, 'b.')
axs[0, 2].plot(x0_2wt, y0_2wt, 'r.')
axs[0, 2].set_title('Rearing Day 1')

axs[1, 2].plot(x1_2gss, y1_2gss, 'b.')
axs[1, 2].plot(x1_2wt, y1_2wt, 'r.')
axs[1, 2].set_title('Rearing Day 7')

axs[2, 2].plot(x2_2gss, y2_2gss, 'b.')
axs[2, 2].plot(x2_2wt, y2_2wt, 'r.')
axs[2, 2].set_title('Rearing Day 14')

axs[3, 2].plot(x3_2gss, y3_2gss, 'b.')
axs[3, 2].plot(x3_2wt, y3_2wt, 'r.')
axs[3, 2].set_title('Rearing Day 21')

axs[4, 2].plot(x4_2gss, y4_2gss, 'b.')
axs[4, 2].plot(x4_2wt, y4_2wt, 'r.')
axs[4, 2].set_title('Rearing Day 28')

axs[5, 2].plot(x5_2gss, y5_2gss, 'b.')
axs[5, 2].plot(x5_2wt, y5_2wt, 'r.')
axs[5, 2].set_title('Rearing Day 35')
axs[5, 2].set_xlabel('Time (Minutes)')

plt.savefig('MatMa_AgeSignal.png',format='png')