import os, mne, re,glob
import pandas as pd
import numpy as np

class TUH_prepropssing:

    def renameChannels(self,EEGseries,CH_names=['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5','T6','Fz', 'Cz', 'Pz']):
        """
        The TUH dataset sometimes use alternative names for channels or indicate the reference setting.
        list: CH_names: names of channels to include, currently we exclude reference channels A1, A2 and T1, T2
        TODO right now it trows away stimuli channels. someone may wish to have them
        """
        for i in EEGseries.info["ch_names"]:
            #Regular expretion to detect EGG "CH" -REF
            reREF = r"(?<=EEG )(.*)(?=-REF)"

            #Detect EEG -LE
            reLE=r"(?<=EEG )(.*)(?=-LE)"

            #Chanels where the seocnd letter need to be lower key.
            reLowC = ['FP1', 'FP2', 'FZ', 'CZ', 'PZ','T','A']

            #Clean chanel names -REF
            if re.search(reREF, i) and re.search(reREF, i).group() in reLowC:
                lowC = i[0:5] + i[5].lower() + i[6:]
                mne.channels.rename_channels(EEGseries.info, {i: re.findall(reREF, lowC)[0]})
            elif re.search(reREF, i):
                mne.channels.rename_channels(EEGseries.info, {i: re.findall(reREF, i)[0]})

            #Clean -Le
            elif re.search(reLE, i) and re.search(reLE, i).group() in reLowC:
                lowC = i[0:5] + i[5].lower() + i[6:]
                mne.channels.rename_channels(EEGseries.info, {i: re.findall(reLE, lowC)[0]})
            elif re.search(reLE, i):
                mne.channels.rename_channels(EEGseries.info, {i: re.findall(reLE, i)[0]})
            else:
                pass
                #print not clean channels
                #print(i)
        #Pick selected chanels
        EEGseries.pick_channels(CH_names)
        return EEGseries

    def findEDF(self,DataDir):
        """
        A function that search a folder for all edf files, and put their path in a dictionary.
        :str DataDir: path to the TUH dataset
        :return: edfDict
        """
        # find all .edf files
        pathRootInt = len(DataDir.split('\\'))
        paths = ['\\'.join(fDir.split('\\')[pathRootInt:]) for fDir in
                 glob.glob(DataDir + "/**/*.edf", recursive=True)]
        # construct defaultDict for data setting
        edfDict = {}
        for path in paths:
            name = path.split('\\')[-1][:-4]
            edfDict[name] = {"path": path.split(".")[0]}
        return edfDict

    def loadAnno(self,annoPath):
        """
        load a TUH anotation file
        :str annoPath: path to the file ekslusive .tse
        :return: a pandas dataframe containing 3 columns and x row's.
        """
        df = pd.read_csv(annoPath+".tse", sep=" ", skiprows=1, header=None)
        df.fillna('null', inplace=True)
        return df

    def annotate_window(self,df,tStart,tEnd):
        """
        Return the lable of a window in so the window is assigned the dormiant label
        :param df: a pandas dataframe made from leadAnno
        :int tStart:
        :int tEnd:
        :return:
        """

        iStart=sum(df[0]<=tStart)-1
        iEnd=sum(df[1]<=tEnd)
        if iStart==iEnd:
            #Assing lable as last started artifact.
            lable=df.iloc[iStart,2]
        else:
            #if and artifact end in the window assign lable to domenet artifact
            lable=df.iloc[[iStart,iEnd][np.argmax([tStart-df.iloc[iStart,0],tEnd-df.iloc[iStart,1]])],2]

        return lable

    def annotate_window_CH(self,annoPath,ch_names,tStart,tEnd):
        """
        Not implemented. Is supposed to loop over all channels.Reacquire someone to teach me which TSE file link to which channel
        :param annoPath:
        :param ch_names:
        :param tStart:
        :param tEnd:
        :return:
        """

        return lable_list


