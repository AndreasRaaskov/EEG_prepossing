import glob
from collections import defaultdict


def findEDF(DataDir):
    """
    A function that search a folder for all edf files, and put their path in a dictionary.
    Warning back in the days (2020) Braincapture had the same file stored multiple places in their dataset.
    If this is still the cases see David's reposetory has and older version of this function.
    """
    # find all .edf files
    pathRootInt = len(DataDir.split('\\'))
    paths = ['\\'.join(fDir.split('\\')[pathRootInt:]) for fDir in
                   glob.glob(DataDir + "/**/*.edf", recursive=True)]
    # construct defaultDict for data setting
    edfDefDict = defaultdict(dict)
    for n,path in enumerate(paths):
        edfDefDict[n]={"path": path.split(".")[0]}
    return edfDefDict

