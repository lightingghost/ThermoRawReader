__author__ = 'lighting'

import comtypes
import comtypes.client
import numpy
from ctypes import *
from comtypes.automation import *
import os

def GetMassDataFromFile(filename):
    RawFile = comtypes.client.CreateObject('MSFileReader.XRawfile')
    try:
        RawFile.open(filename)
    except:
        pass
    RawFile.SetCurrentController(0,1)
    NumSpectra = c_long()
    RawFile.GetNumSpectra(NumSpectra)

    # set up values for MSFileReader.GetMassListFromScanNumber:
    Filter = u''
    IntensityCutoffType = 0
    IntensityCutoffValue = 0
    MaxNumberOfPeaks = 0
    CentroidResult = 0
    MassList = VARIANT()
    PeakFlags = VARIANT()
    ArraySize = c_long()


    for ScanNum in range(1,NumSpectra.value+1):
        RawFile.GetMassListFromScanNum(
            c_long(ScanNum),
            Filter,
            c_long(IntensityCutoffType),
            c_long(IntensityCutoffValue),
            c_long(MaxNumberOfPeaks),
            c_long(CentroidResult),
            c_double(0),
            MassList,
            PeakFlags,
            ArraySize
            )

        MassList = numpy.array(MassList.value)
        return MassList

def GetAvMassSpecFromFile(filename):
    RawFile = comtypes.client.CreateObject('MSFileReader.XRawfile')
    try:
        RawFile.open(filename)
    except:
        pass
    RawFile.SetCurrentController(0,1)
    NumSpectra = c_long()
    RawFile.GetNumSpectra(NumSpectra)
    ScanNum = NumSpectra.value
    ScansToAverage = (c_long * ScanNum)(* range(1,ScanNum+1))


    # set up values for MSFileReader.GetAveragedMassSpectrum:
    CentroidResult = 0
    MassList = VARIANT()
    PeakFlags = VARIANT()
    ArraySize = c_long()
    ArraySize.value = 0

    RawFile.GetAveragedMassSpectrum(
        ScansToAverage,
        c_long(ScanNum),
        c_long(CentroidResult),
        MassList,
        PeakFlags,
        ArraySize
        )

    MassList = numpy.array(MassList.value)
    RawFile.close()
    return MassList

def GetPeakValueFromMassData(MassData,peak = 178.08):
    min = peak - 0.005
    max = peak + 0.005
    intensity = numpy.array([])
    for i in range(int(MassData.size/2)):
        if (MassData[0,i] >= min) & (MassData[0,i] <= max):
            intensity = numpy.append(intensity,MassData[1,i])
    PeakValue = intensity.max()
    return PeakValue

def GetIntegratedIntensityFromMassData(MassData):
    x = MassData[0,:]
    y = MassData[1,:]
    return numpy.trapz(y,x)

def TraverseFiles(Path,func):
    files = os.listdir(Path)
    for filename in files:
        func(filename)
    return 0

if __name__ == '__main__':

    Path = os.getcwd()
    Files = os.listdir(Path)

    OutFile = open('result.txt','w')

    for filename in Files:
        if filename.find('.raw') == -1:
            continue
        underline = filename.find('_')
        if underline != -1:
            name = filename[0:underline]
        else:
            name = filename[0:-4]
        MassList = GetAvMassSpecFromFile(filename)
        PeakValue = GetPeakValueFromMassData(MassList, 178.08)

        OutFile.write(name + '\t' + str(PeakValue) + '\n')

    OutFile.close()