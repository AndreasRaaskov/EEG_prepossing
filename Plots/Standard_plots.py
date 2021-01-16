import os
import numpy as np
from collections import  defaultdict
from scipy import signal
from skimage.transform import resize
import matplotlib.pyplot as plt


def spectrogram(EEGseries=None,lable=None,upercut=None,plot=False,localSave=None,resized=False,newSize=(224,224)):
    """
    Trun and EEG signal into a spectrogram for each channel
    :param EEGseries:
    :list or str lable: if given a string it will asign that to the lable of all the image, if given a list it will
     assign each label to the coresponding chanel
    :int upercut: cut the upper part of the signal of. Ex. upercut=50 would remove all frequence aboce 50Hz
    :Bool plot: Will show the spectrogram
    :str localSave: path+name of the place the spectrogram will be saved. For each channel a spectrogram would be made
    with the name: name+_channelname.png
    :Bool resized: should the image be resized
    :tulip newSize: if resize=True indicate new size as (height,with)
    :return: dict opbject with the channels as keys. if localSave is defined return the path to each image,
    else return the image as a 2D numpy array
    """

    ch_dict = defaultdict()
    fTemp, tTemp, Sxx = signal.spectrogram(EEGseries.get_data(), fs=EEGseries.info["sfreq"])

    for i, ch in enumerate(EEGseries.ch_names):
        if isinstance(upercut,int):
            image = np.log(Sxx[i] + np.finfo(float).eps)[0:upercut]

        else:
            image = np.log(Sxx[i] + np.finfo(float).eps)


        if resized:
            image = resize(image, newSize,anti_aliasing=True)

        if isinstance(lable,list):
            L=ch+" "+lable[i]
            write_label=True
        elif isinstance(lable,str):
            L=ch+" "+lable
            write_label = True
        else:
            write_label = False

        if plot:
            plt.imshow(image)
            if write_label:
               plt.title(L)
            plt.show()

        if isinstance(localSave,str):
            ax=plt.imshow(image)
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            if write_label:
               plt.title(L)
            plt.savefig(os.path.join(localSave+f"_{ch}"))

            #ad part to dict
            ch_dict[ch]=localSave+f"_{ch}"+r".png"
        else:
            #ad window to dict
            ch_dict[ch]=image


    return ch_dict