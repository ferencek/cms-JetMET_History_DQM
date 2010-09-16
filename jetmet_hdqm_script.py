#!/usr/bin/env python

import os, sys, string, re
from ROOT import *
from array import array

##################################################################################################################################
#### User Section

# Please don't change anything outside the User Section
# Description of different variables is provided below
# More detailed instructions available at https://twiki.cern.ch/twiki/bin/view/CMS/JetMETHistoryDQM

# Turn on/off the run range mode
runRangeMode = False # set to True if you want to turn on the run range mode

# Run range defined as [first,last] (used only if runRangeMode = True)
runRange = [144010,144114]

# List of runs to be processed
runNumbers = [144010,144011,144083,144086,144089,144112,144114]

# List of BAD runs to be processed and overlaid on the same canvas with runNumbers
# specified above. If this list is left empty, no overlay is done
runNumbers_BAD = [144083]

# Location of the DQM output root files
fileLocation = '/uscmst1b_scratch/lpc1/lpcphys/ferencek/JetMET/CMSSW_3_8_1_patch2/test/JetMET_HDQM'

# List of DQM Monitor Elements to be processed
# For each Monitor Element a list of entries is defined with the following meaning:
# Entry 0: Specifies the Monitor Element
# Entry 1: Specifies the quantity to be extracted from the Monitor Element. Can be 'mean' or 'rms'
# Entries 2 and 3: Define the y-axis range. If both numbers are equal, the ROOT default is used
# Entry 4: Monitor Element title
# Entry 5: y-axis title
# Entry 6: File format of the final plot ('png', 'eps', 'pdf', etc.)
dqmMEs = [
  ### CaloMET
  ['MET/CaloMET/BasicCleanup/METTask_CaloMET','mean',-1,-1,'CaloMET_BasicCleanup_METTask_CaloMET_Mean','CaloMET Mean [GeV]','png'],

  ['MET/CaloMET/BasicCleanup/METTask_CaloSumET','mean',-1,-1,'CaloMET_BasicCleanup_METTask_CaloSumET_Mean','CaloSumET Mean [GeV]','png'],

  #['MET/CaloMET/BasicCleanup/METTask_CaloMEx','mean',-1,-1,'CaloMET_BasicCleanup_METTask_CaloMEx_Mean','CaloMEx Mean [GeV]','png'],

  #['MET/CaloMET/BasicCleanup/METTask_CaloMEx','rms',-1,-1,'CaloMET_BasicCleanup_METTask_CaloMEx_RMS','CaloMEx RMS [GeV]','png'],

  #['MET/CaloMET/BasicCleanup/METTask_CaloMEy','mean',-1,-1,'CaloMET_BasicCleanup_METTask_CaloMEy_Mean','CaloMEy Mean [GeV]','png'],

  #['MET/CaloMET/BasicCleanup/METTask_CaloMEy','rms',-1,-1,'CaloMET_BasicCleanup_METTask_CaloMEy_RMS','CaloMEy RMS [GeV]','png'],

  #['MET/CaloMET/ExtraCleanup/METTask_CaloMET','mean',-1,-1,'CaloMET_ExtraCleanup_METTask_CaloMET_Mean','CaloMET Mean [GeV]','png'],

  #['MET/CaloMET/ExtraCleanup/METTask_CaloSumET','mean',-1,-1,'CaloMET_ExtraCleanup_METTask_CaloSumET_Mean','CaloSumET Mean [GeV]','png'],

  #['MET/CaloMET/ExtraCleanup/METTask_CaloMEx','mean',-1,-1,'CaloMET_ExtraCleanup_METTask_CaloMEx_Mean','CaloMEx Mean [GeV]','png'],

  #['MET/CaloMET/ExtraCleanup/METTask_CaloMEx','rms',-1,-1,'CaloMET_ExtraCleanup_METTask_CaloMEx_RMS','CaloMEx RMS [GeV]','png'],

  #['MET/CaloMET/ExtraCleanup/METTask_CaloMEy','mean',-1,-1,'CaloMET_ExtraCleanup_METTask_CaloMEy_Mean','CaloMEy Mean [GeV]','png'],

  #['MET/CaloMET/ExtraCleanup/METTask_CaloMEy','rms',-1,-1,'CaloMET_ExtraCleanup_METTask_CaloMEy_RMS','CaloMEy RMS [GeV]','png'],
  #### CaloMETNoHF
  #['MET/CaloMETNoHF/BasicCleanup/METTask_CaloMET','mean',-1,-1,'CaloMETNoHF_BasicCleanup_METTask_CaloMET_Mean','CaloMET Mean [GeV]','png'],

  #['MET/CaloMETNoHF/BasicCleanup/METTask_CaloSumET','mean',-1,-1,'CaloMETNoHF_BasicCleanup_METTask_CaloSumET_Mean','CaloSumET Mean [GeV]','png'],

  #['MET/CaloMETNoHF/BasicCleanup/METTask_CaloMEx','mean',-1,-1,'CaloMETNoHF_BasicCleanup_METTask_CaloMEx_Mean','CaloMEx Mean [GeV]','png'],

  #['MET/CaloMETNoHF/BasicCleanup/METTask_CaloMEx','rms',-1,-1,'CaloMETNoHF_BasicCleanup_METTask_CaloMEx_RMS','CaloMEx RMS [GeV]','png'],

  #['MET/CaloMETNoHF/BasicCleanup/METTask_CaloMEy','mean',-1,-1,'CaloMETNoHF_BasicCleanup_METTask_CaloMEy_Mean','CaloMEy Mean [GeV]','png'],

  #['MET/CaloMETNoHF/BasicCleanup/METTask_CaloMEy','rms',-1,-1,'CaloMETNoHF_BasicCleanup_METTask_CaloMEy_RMS','CaloMEy RMS [GeV]','png'],

  #['MET/CaloMETNoHF/ExtraCleanup/METTask_CaloMET','mean',-1,-1,'CaloMETNoHF_ExtraCleanup_METTask_CaloMET_Mean','CaloMET Mean [GeV]','png'],

  #['MET/CaloMETNoHF/ExtraCleanup/METTask_CaloSumET','mean',-1,-1,'CaloMETNoHF_ExtraCleanup_METTask_CaloSumET_Mean','CaloSumET Mean [GeV]','png'],

  #['MET/CaloMETNoHF/ExtraCleanup/METTask_CaloMEx','mean',-1,-1,'CaloMETNoHF_ExtraCleanup_METTask_CaloMEx_Mean','CaloMEx Mean [GeV]','png'],

  #['MET/CaloMETNoHF/ExtraCleanup/METTask_CaloMEx','rms',-1,-1,'CaloMETNoHF_ExtraCleanup_METTask_CaloMEx_RMS','CaloMEx RMS [GeV]','png'],

  #['MET/CaloMETNoHF/ExtraCleanup/METTask_CaloMEy','mean',-1,-1,'CaloMETNoHF_ExtraCleanup_METTask_CaloMEy_Mean','CaloMEy Mean [GeV]','png'],

  #['MET/CaloMETNoHF/ExtraCleanup/METTask_CaloMEy','rms',-1,-1,'CaloMETNoHF_ExtraCleanup_METTask_CaloMEy_RMS','CaloMEy RMS [GeV]','png'],
  #### TcMET
  #['MET/TcMET/BasicCleanup/METTask_MET','mean',-1,-1,'TcMET_BasicCleanup_METTask_MET_Mean','MET Mean [GeV]','png'],

  #['MET/TcMET/BasicCleanup/METTask_SumET','mean',-1,-1,'TcMET_BasicCleanup_METTask_SumET_Mean','SumET Mean [GeV]','png'],

  #['MET/TcMET/BasicCleanup/METTask_MEx','mean',-1,-1,'TcMET_BasicCleanup_METTask_MEx_Mean','MEx Mean [GeV]','png'],

  #['MET/TcMET/BasicCleanup/METTask_MEx','rms',-1,-1,'TcMET_BasicCleanup_METTask_MEx_RMS','MEx RMS [GeV]','png'],

  #['MET/TcMET/BasicCleanup/METTask_MEy','mean',-1,-1,'TcMET_BasicCleanup_METTask_MEy_Mean','MEy Mean [GeV]','png'],

  #['MET/TcMET/BasicCleanup/METTask_MEy','rms',-1,-1,'TcMET_BasicCleanup_METTask_MEy_RMS','MEy RMS [GeV]','png'],

  #['MET/TcMET/ExtraCleanup/METTask_MET','mean',-1,-1,'TcMET_ExtraCleanup_METTask_MET_Mean','MET Mean [GeV]','png'],

  #['MET/TcMET/ExtraCleanup/METTask_SumET','mean',-1,-1,'TcMET_ExtraCleanup_METTask_SumET_Mean','SumET Mean [GeV]','png'],

  #['MET/TcMET/ExtraCleanup/METTask_MEx','mean',-1,-1,'TcMET_ExtraCleanup_METTask_MEx_Mean','MEx Mean [GeV]','png'],

  #['MET/TcMET/ExtraCleanup/METTask_MEx','rms',-1,-1,'TcMET_ExtraCleanup_METTask_MEx_RMS','MEx RMS [GeV]','png'],

  #['MET/TcMET/ExtraCleanup/METTask_MEy','mean',-1,-1,'TcMET_ExtraCleanup_METTask_MEy_Mean','MEy Mean [GeV]','png'],

  #['MET/TcMET/ExtraCleanup/METTask_MEy','rms',-1,-1,'TcMET_ExtraCleanup_METTask_MEy_RMS','MEy RMS [GeV]','png'],
  #### MuCorrMET
  #['MET/MuCorrMET/BasicCleanup/METTask_MET','mean',-1,-1,'MuCorrMET_BasicCleanup_METTask_MET_Mean','MET Mean [GeV]','png'],

  #['MET/MuCorrMET/BasicCleanup/METTask_SumET','mean',-1,-1,'MuCorrMET_BasicCleanup_METTask_SumET_Mean','SumET Mean [GeV]','png'],

  #['MET/MuCorrMET/BasicCleanup/METTask_MEx','mean',-1,-1,'MuCorrMET_BasicCleanup_METTask_MEx_Mean','MEx Mean [GeV]','png'],

  #['MET/MuCorrMET/BasicCleanup/METTask_MEx','rms',-1,-1,'MuCorrMET_BasicCleanup_METTask_MEx_RMS','MEx RMS [GeV]','png'],

  #['MET/MuCorrMET/BasicCleanup/METTask_MEy','mean',-1,-1,'MuCorrMET_BasicCleanup_METTask_MEy_Mean','MEy Mean [GeV]','png'],

  #['MET/MuCorrMET/BasicCleanup/METTask_MEy','rms',-1,-1,'MuCorrMET_BasicCleanup_METTask_MEy_RMS','MEy RMS [GeV]','png'],

  #['MET/MuCorrMET/ExtraCleanup/METTask_MET','mean',-1,-1,'MuCorrMET_ExtraCleanup_METTask_MET_Mean','MET Mean [GeV]','png'],

  #['MET/MuCorrMET/ExtraCleanup/METTask_SumET','mean',-1,-1,'MuCorrMET_ExtraCleanup_METTask_SumET_Mean','SumET Mean [GeV]','png'],

  #['MET/MuCorrMET/ExtraCleanup/METTask_MEx','mean',-1,-1,'MuCorrMET_ExtraCleanup_METTask_MEx_Mean','MEx Mean [GeV]','png'],

  #['MET/MuCorrMET/ExtraCleanup/METTask_MEx','rms',-1,-1,'MuCorrMET_ExtraCleanup_METTask_MEx_RMS','MEx RMS [GeV]','png'],

  #['MET/MuCorrMET/ExtraCleanup/METTask_MEy','mean',-1,-1,'MuCorrMET_ExtraCleanup_METTask_MEy_Mean','MEy Mean [GeV]','png'],

  #['MET/MuCorrMET/ExtraCleanup/METTask_MEy','rms',-1,-1,'MuCorrMET_ExtraCleanup_METTask_MEy_RMS','PfMEy RMS [GeV]','png'],
  #### PfMET
  #['MET/PfMET/BasicCleanup/METTask_PfMET','mean',-1,-1,'PfMET_BasicCleanup_METTask_MET_Mean','PfMET Mean [GeV]','png'],

  #['MET/PfMET/BasicCleanup/METTask_PfSumET','mean',-1,-1,'PfMET_BasicCleanup_METTask_SumET_Mean','PfSumET Mean [GeV]','png'],

  #['MET/PfMET/BasicCleanup/METTask_PfMEx','mean',-1,-1,'PfMET_BasicCleanup_METTask_MEx_Mean','PfMEx Mean [GeV]','png'],

  #['MET/PfMET/BasicCleanup/METTask_PfMEx','rms',-1,-1,'PfMET_BasicCleanup_METTask_MEx_RMS','PfMEx RMS [GeV]','png'],

  #['MET/PfMET/BasicCleanup/METTask_PfMEy','mean',-1,-1,'PfMET_BasicCleanup_METTask_MEy_Mean','PfMEy Mean [GeV]','png'],

  #['MET/PfMET/BasicCleanup/METTask_PfMEy','rms',-1,-1,'PfMET_BasicCleanup_METTask_MEy_RMS','PfMEy RMS [GeV]','png'],

  #['MET/PfMET/ExtraCleanup/METTask_PfMET','mean',-1,-1,'PfMET_ExtraCleanup_METTask_MET_Mean','PfMET Mean [GeV]','png'],

  #['MET/PfMET/ExtraCleanup/METTask_PfSumET','mean',-1,-1,'PfMET_ExtraCleanup_METTask_SumET_Mean','PfSumET Mean [GeV]','png'],

  #['MET/PfMET/ExtraCleanup/METTask_PfMEx','mean',-1,-1,'PfMET_ExtraCleanup_METTask_MEx_Mean','PfMEx Mean [GeV]','png'],

  #['MET/PfMET/ExtraCleanup/METTask_PfMEx','rms',-1,-1,'PfMET_ExtraCleanup_METTask_MEx_RMS','PfMEx RMS [GeV]','png'],

  #['MET/PfMET/ExtraCleanup/METTask_PfMEy','mean',-1,-1,'PfMET_ExtraCleanup_METTask_MEy_Mean','PfMEy Mean [GeV]','png'],

  #['MET/PfMET/ExtraCleanup/METTask_PfMEy','rms',-1,-1,'PfMET_ExtraCleanup_METTask_MEy_RMS','PfMEy RMS [GeV]','png']
]

#### End of User Section
##################################################################################################################################


def make_graphs(fRunRangeMode,fRunRange,fRunNumbers,fFileLocation,fDQMMEs,fColor):

  if not os.path.isdir(fFileLocation):
    print ('Sorry, %s is not a directory'%(fFileLocation))
    sys.exit()

  x = []
  ex = []
  fileNames = []

  for i in os.listdir(fFileLocation):
    if not os.path.isfile(os.path.join(fFileLocation,i)):
      continue
    if(i.find('_R')==-1 or not re.search('.root$',i)):
      continue
    run=string.atoi(i[(i.find('_R')+2):(i.find('_R')+11)])
    if(fRunRangeMode):
      if(len(fRunRange)<2):
        print 'Please define a range of runs to be processed'
        sys.exit()
      if(run>=fRunRange[0] and run<=fRunRange[1]):
        if(x.count(run)>0):
          print ('Multiple DQM files found for run %i'%(run))
          print 'Aborting'
          sys.exit()
        x.append(run)
        ex.append(0)
        fileNames.append(os.path.join(fFileLocation,i))
    else:
      for j in range(len(fRunNumbers)):
        if(run==fRunNumbers[j]):
          if(x.count(run)>0):
            print ('Multiple DQM files found for run %i'%(run))
            print 'Aborting'
            sys.exit()
          x.append(run)
          ex.append(0)
          fileNames.append(os.path.join(fFileLocation,i))


  if (len(x)==0):
    print ('No DQM files corresponding to the requested run numbers found in ' + fFileLocation)
    sys.exit()

  y_arrays_transposed = []
  ey_arrays_transposed = []

  for i in range(len(x)):
    print ('Processing %s'%(fileNames[i]))
    y_tr = []
    ey_tr = []
    try:
      inputFile = TFile(fileNames[i])
      hist = TH1F()
      for j in range(len(fDQMMEs)):
        histoName = ('DQMData/Run %i/JetMET/Run summary/'%(x[i])) + fDQMMEs[j][0]
        try:
          hist=inputFile.Get(histoName)
          if(fDQMMEs[j][1]=='mean'):
            y_tr.append(hist.GetMean())
            ey_tr.append(hist.GetMeanError())
          elif(fDQMMEs[j][1]=='rms'):
            y_tr.append(hist.GetRMS())
            ey_tr.append(hist.GetRMSError())
        except:
          print ('Could not find ' + histoName + ' in ' + fileNames[i])
          continue
    except:
      print ('Could not open ' + fileNames[i])
      continue
    if(len(y_tr)!=len(fDQMMEs) or len(ey_tr)!=len(fDQMMEs)):
      print 'Could not find some Monitor Elements. Please check that their names were typed in correctly'
      print 'Aborting'
      sys.exit()
    y_arrays_transposed.append(y_tr)
    ey_arrays_transposed.append(ey_tr)

  if(len(y_arrays_transposed)!=len(x) or len(ey_arrays_transposed)!=len(x)):
    print 'Could not open some DQM root files. These files might be corrupted'
    print 'Aborting'
    sys.exit()

  graphs = []

  for i in range(len(fDQMMEs)):
    y = []
    ey = []
    for j in range(len(x)):
      y.append(y_arrays_transposed[j][i])
      ey.append(ey_arrays_transposed[j][i])

    graph = TGraphErrors(len(x),array('d',x),array('d',y),array('d',ex),array('d',ey))
    graph.SetTitle(fDQMMEs[i][4])
    graph.GetXaxis().SetTitle('Run Number')
    graph.GetYaxis().SetTitle(fDQMMEs[i][5])
    graph.SetMarkerStyle(20)
    graph.SetMarkerColor(fColor)
    if(fDQMMEs[i][2]!=fDQMMEs[i][3]):
      graph.SetMinimum(fDQMMEs[i][2])
    if(fDQMMEs[i][2]!=fDQMMEs[i][3]):
      graph.SetMaximum(fDQMMEs[i][3])
    graphs.append(graph)

  return graphs


def main(fRunRangeMode,fRunRange,fRunNumbers,fRunNumbers_BAD,fFileLocation,fDQMMEs):

  gROOT.SetBatch(kTRUE);
  gStyle.SetCanvasColor(0)
  gStyle.SetCanvasBorderMode(0)
  gStyle.SetPadColor(0)
  gStyle.SetPadBorderMode(0)
  gStyle.SetFrameBorderMode(0)
  gStyle.SetPadTickX(1)
  gStyle.SetPadTickY(1)
  gStyle.SetPalette(1)

  graphs = make_graphs(fRunRangeMode,fRunRange,fRunNumbers,fFileLocation,fDQMMEs,kRed)
  graphs_BAD = []
  if(len(fRunNumbers_BAD)>0): graphs_BAD = make_graphs(False,fRunRange,fRunNumbers_BAD,fFileLocation,fDQMMEs,kBlue)

  for i in range(len(fDQMMEs)):

    c = TCanvas('c');
    c.cd();

    graphs[i].Draw('ap')
    legend = TLegend(0.15,0.7,0.32,0.84);
    if(len(fRunNumbers_BAD)>0):
      graphs_BAD[i].Draw('p')
      legend.AddEntry(graphs[i],'GOOD runs','lp');
      legend.AddEntry(graphs_BAD[i],'BAD runs','lp');
      legend.Draw();

    c.SaveAs((fDQMMEs[i][4] + '.' + fDQMMEs[i][6]))

    del legend
    del c

  print 'Output files successfully created'
  sys.exit()

if __name__ == '__main__':
  main(runRangeMode,runRange,runNumbers,runNumbers_BAD,fileLocation,dqmMEs)
