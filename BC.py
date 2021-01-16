import os,glob
import numpy as np
import pandas as pd
from collections import defaultdict

class BrainCapture_prepossing:

    def preloadAnno(self, path_xlsx_file, file_name_xlsx='MGH_File_Annotations.xlsx', sheet_names=[2, 3, 4],
                        atributes=["Quality Of Eeg", "Is Eeg Usable For Clinical Purposes", "Reader",
                                   "Recording Length [seconds]"], sort=False):
        """
        Read the braincapture exel file and create and opbject self.annoDict with all the anotations.

        str: path_xlsx_file: path to the braincapture folder
        str: file_name_xlsx:
        list: sheet_names: list of the sheets to loop over
        bool: sort: if true files with missing attributes will be deathFlagged
        list: atributes: atribute that you wish to use
        """
        self.annoDict=defaultdict()

        for sheet in sheet_names:
            annotation = pd.read_excel(os.path.join(path_xlsx_file, file_name_xlsx), sheet_name=sheet)
            for idx, path in enumerate(annotation['Recording']):
                name = path.split("/")[-1][:-4]

                self.annoDict[name]={"annotation": annotation.iloc[idx].loc[atributes].to_dict(),"deathFlag":False}
                if sort:
                    for an in atributes:  # deathFlag missing values
                        if isinstance(self.annoDict[name]["annotation"][an], str) == False:
                            if np.isnan(self.annoDict[name]["annotation"][an]):
                                self.annoDict[name]["deathFlag"] = True
                                self.annoDict[name]["reson"] = "atribute one or more atributes is missing"


        # Check if there are files without anotation
        if sort:
            for id in self.annoDict.keys():
                if ("annotation" in self.annoDict[id]) == False:
                    self.annoDict[id]["deathFlag"] = True
                    self.annoDict[id]["reson"] = "annotaiton missing"

    def add_annotation(self,edfDict,delete_unanotatet=False):
        """
        Takes and edfDict and add annotation to the files in it.
        Warning the object self.annoDict must be made in advance
        :dict edfDict:
        :bool delete_unanotatet: if true unanotatet files will be deleted, else it raise a warning.
        :return: edfDict
        """

        for file in list(edfDict.keys()):
            try:
                #Check if all lables are there
                if self.annoDict[file]["deathFlag"]==False:

                    #If theres only one lable add that else ad a list.
                    if len(self.annoDict[file]["annotation"])==1:
                        edfDict[file]["Y"]=self.annoDict[file]["annotation"][0]
                    else:
                        edfDict[file]["Y"] = self.annoDict[file]["annotation"]
                else:
                    if delete_unanotatet:
                        del edfDict[file]
                        print(f"Warning {file} removed because of missing annotation")
                    else:
                        print(f"Warning {file} is not annotatet")
            except:
                raise NameError('annoDict not made, run the function preloadAnno before this function')
        return edfDict

    def findEDF(self,DataDir):
        """
        A function that search a folder for all edf files, and put their path in a dictionary.
        Warning since in the TUH dataset a file may appere multiple palces in the dataset the path is a list
        :str DataDir: path to the TUH dataset
        :return: edfDict
        """
        # find all .edf files
        pathRootInt = len(DataDir.split('\\'))
        paths = ['\\'.join(fDir.split('\\')[pathRootInt:]) for fDir in
                 glob.glob(DataDir + "/**/*.edf", recursive=True)]

        edfDict = defaultdict(dict)
        for path in paths:
            name = path.split('\\')[-1][:-4]

            #Check if file is already in edfDict
            if name in edfDict.keys():
                edfDict[name]["path"].append(path[:-4])
                edfDict[name]["deathFlag"] = True
                edfDict[name]["reson"] = "already existing"
            else:
                edfDict[name]["path"] = []
                edfDict[name]["deathFlag"] = False
                edfDict[name]["path"].append(path[:-4])

            edfDict[name]["Files named %s" % name] = len(edfDict[name]["path"])
        return edfDict



