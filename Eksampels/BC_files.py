import os

from BC import BrainCapture_prepossing
from General import standard_preprossing
from Plots.Plotly import plot_EEG

"""
Loading Braincapture data and annotate it.
Performe prepossing
and plotit using plotly 
"""


class pipeline(standard_preprossing,BrainCapture_prepossing):
    def __init__(self,datapath):
        self.dataDir=datapath

        #Load anotation file
        self.preloadAnno(datapath, atributes=["Quality Of Eeg", "Is Eeg Usable For Clinical Purposes"], sort=True)

    def makeDataset(self):
        #make edfDict
        edfDict=self.findEDF(self.dataDir)
        #annotate edfDict
        edfDict=self.add_annotation(edfDict,delete_unanotatet=True)

        #loop over all the files
        for name in list(edfDict.keys()):
            #load EEG
            EEG_serie=self.readRawEdf(edfDict[name]["path"][0])
            #filet
            EEG_serie=self.Makoto(EEG_serie,lpfq=0,hpfq=50,notchfq=50)

            #Plot the serie interactive.
            plot_EEG(EEG_serie,title=edfDict[name]["Y"])






if __name__ == '__main__':

    path=os.path.join(os.getcwd(),"Dummy_BC")
    pl=pipeline(path)
    data=pl.makeDataset()