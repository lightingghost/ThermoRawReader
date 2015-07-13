__author__ = 'lighting'

import comtypes
import comtypes.client
from ctypes import *
from comtypes.automation import *
import sys
import numpy

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
    return MassList

def GetPeakValueFromMassData(MassData,peak = 178.08):
    min = peak - 0.005
    max = peak + 0.005
    rng = [(MassData[0]>=min)&(MassData[0]<=max)]
    dataout = numpy.array((MassData[0][rng],MassData[1][rng])).transpose()
    intensity = dataout[:,1]
    PeakValue = intensity.max()
    return PeakValue

def GetIntegratedIntensityFromMassData(MassData):
    x = MassData[0,:]
    y = MassData[1,:]
    return numpy.trapz(y,x)


if __name__ == '__main__':

    filename = '140426.raw'
    MassList = GetAvMassSpecFromFile(filename)
    PeakValue = GetPeakValueFromMassData(MassList, 178.08)
    IntegratedIntensity = GetIntegratedIntensityFromMassData(MassList)
    print(PeakValue)
    print(IntegratedIntensity)