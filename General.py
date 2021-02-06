import mne
from mne.io import read_raw_edf
from collections import defaultdict
import os

class standard_preprossing:
    """
    A class for the most basic loading of data.
    Use as a prarent for more specific pipelines
    """
    def Makoto(self,EEGseries, lpfq=None, hpfq=None, notchfq=50, reSam=250):
        # Follows Makoto's_Preprocessing_Pipeline recommended for EEGlab's ICA
        # https: // sccn.ucsd.edu / wiki / Makoto % 27s_preprocessing_pipeline
        # combined with Early State Preprocessing: PREP


        # Resample to desired frequence
        if isinstance(reSam,int):
            EEGseries.resample(reSam)

        # Apply filters
        EEGseries.filter(l_freq=lpfq,h_freq=hpfq, fir_design='firwin')

        #self.montagetype = "standard_1005"
        #Import channel info -> configure cap setup and channel names. montagetype must be difinde in a child class
        ##EEGseries.set_montage(mne.channels.make_standard_montage(kind=self.montagetype, head_size=0.095))

        #Apply Notch filter
        if isinstance(notchfq,int):
            EEGseries.notch_filter(freqs=notchfq, notch_widths=5)

        EEGseries.set_eeg_reference()

        return EEGseries

    def applyMontage(self,EEGseries,montage):
        """
        Usefull for more advance MNE plot.
        for TUH montage use "standard_1005"
        for BC montage use "easycap-M1"

        """
        EEGseries.set_montage(mne.channels.make_standard_montage(kind=montage, head_size=0.095))
        return EEGseries

    def readRawEdf(self,path, read_raw_edf_param={'preload':True, 'stim_channel':'auto','verbose':'WARNING'}):
        """
        Load a singel file edf file.
        :str path: path to edf file exclusive edf
        :param read_raw_edf_param:
        :return: an MNE EEG opbject
        """

        EEGserie = read_raw_edf(os.path.join(self.dataDir,path)+".edf", **read_raw_edf_param)
        return EEGserie

class window_prepossing:
    """
    If the signal should be split into windows use this class
    """

    def slidingWindow(self,EEGseries,tWindow,overlap=0,DataMaker=False):
        """
        Split singal up into windows. Note if signal length is not divisible by twindow will the last part of the signal
        be trown away.
        :EEGseries:
        :float tWindow: how long each window should be. in seconds
        :float Overlap: must be in range [0,1[
        :Bool datamaker: will call the opbject DataMake if it exist in a child class.
        :return: dictionary with all the windows.
        """
        windowEEG = defaultdict(list)


        #Get the lengt of the signal in seconds
        tSignal=EEGseries._last_time

        for n,tStart in enumerate(range(0, int(tSignal), int(tWindow*overlap))):
            windowKey = f"window_{n}"
            tEnd=tStart + tWindow
            if tEnd<tSignal:
                windowEEG[windowKey]=EEGseries.copy().crop(tmin=tStart,tmax=tEnd)
                if DataMaker:
                    windowEEG[windowKey] = self.DataMaker(windowEEG[windowKey],meta={"tStart": tStart,"tEnd": tEnd,"window": n})
            else:
                #Ignore the last window if there isen't enough left of the original signal
                pass

        return windowEEG


