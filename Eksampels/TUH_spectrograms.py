import os
from General import standard_preprossing,window_prepossing
from TUH import TUH_prepropssing
from Plots.Standard_plots import spectrogram

"""
And example on how to laod a singel TUH file.
Perrom a standard prepossing 
Turn it into windows 
add anotation to each window.
and save it as spectrograms.  
"""

class pipeline(TUH_prepropssing,standard_preprossing,window_prepossing):

    def makeDataset(self,Data_path):

        edfDict=self.findEDF(Data_path)
        self.dataDir=Data_path

        #Only go over one file
        file=list(edfDict.keys())[0]
        EEG_serie=self.readRawEdf(edfDict[file]["path"])
        EEG_serie.plot()
        print(EEG_serie.ch_names)
        EEG_serie=self.renameChannels(EEG_serie) #Remove bad chanels
        print(EEG_serie.ch_names)
        EEG_serie=self.Makoto(EEG_serie,lpfq=None,hpfq=None)
        EEG_serie.plot()

        #EEG_serie=self.applyMontage(EEG_serie,'standard_1005')

        #load TSE file
        self.annotations=self.loadAnno(EEG_serie.filenames[0][:-4])

        windowdict=self.slidingWindow(EEG_serie,tWindow=60,overlap=0.25,DataMaker=True)
        return windowdict

    def DataMaker(self,EEGserie,meta):
        """
        This function is called from make window and will be performed on all windows
        :param EEGserie:
        :param meta:
        :return:
        """
        windowdict={}
        lable=self.annotate_window(self.annotations,meta["tStart"],meta["tEnd"])

        #plot the spectrgras
        windowdict["X"]=spectrogram(EEGserie,plot=True, lable=lable, resized=True, upercut=50)

        #Save the spectrograms
        #savepath=os.path.join(os.getcwd(),r"Eksampels\Test",f"{meta['window']}")
        #spectrogram(EEGserie,lable=lable,resized=True,localSave=savepath,upercut=50)

        windowdict["X"]=spectrogram(EEGserie,resized=True,upercut=50)
        windowdict["Y"]=lable
        return windowdict



if __name__ == '__main__':
    Datapath=os.getcwd()+"\Dummy_TUH"
    pl=pipeline()
    data=pl.makeDataset(Datapath)
    print(data)