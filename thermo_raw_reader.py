__author__ = 'lighting'

import comtypes
import comtypes.client
import numpy
from ctypes import *
from comtypes.automation import *
import os

class RawFile:

    DLL = comtypes.client.CreateObject('MSFileReader.XRawfile')


    def __init__(self, filename):
        self.filename = filename
        self.DLL.Open(filename)
        self.DLL.SetCurrentController(0,1)


    def get_num_spectra(self):
        num_spectra = c_long()
        self.DLL.GetNumSpectra(num_spectra)
        return num_spectra.value

    def get_mass_list(self,scan_num):

        # set up values for MSFileReader.GetMassListFromScanNumber:
        Filter = u''
        IntensityCutoffType = 0
        IntensityCutoffValue = 0
        MaxNumberOfPeaks = 0
        CentroidResult = 0
        MassList = VARIANT()
        PeakFlags = VARIANT()
        ArraySize = c_long()

        code = self.DLL.GetMassListFromScanNum(
            c_long(scan_num),
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

        MassData = numpy.array(MassList.value)
        return MassData

    def get_average_mass_list(self, start=1, end=1):

        # set up values for MSFileReader.GetAverageMassList:
        FirstAvgScanNumber = start
        LastAvgScanNumber = end
        FirstBkg1ScanNumber = 0
        LastBkg1ScanNumber = 0
        FirstBkg2ScanNumber = 0
        LastBkg2ScanNumber = 0
        Filter = u''
        IntensityCutoffType = 0
        IntensityCutoffValue = 0
        MaxNumberOfPeaks = 0
        CentroidResult = False
        CentroidPeakWidth = c_double()
        MassList = VARIANT()
        PeakFlags = VARIANT()
        ArraySize = c_long()

        # Attention!!! The Parameters of the function in MSFileReader-30-SP1-Ref is wrong!!!
        self.DLL.GetAverageMassList(
            c_long(FirstAvgScanNumber),
            c_long(LastAvgScanNumber),
            c_long(FirstBkg1ScanNumber),
            c_long(LastBkg1ScanNumber),
            c_long(FirstBkg2ScanNumber),
            c_long(LastBkg2ScanNumber),
            Filter,
            c_long(IntensityCutoffType),
            c_long(IntensityCutoffValue),
            c_long(MaxNumberOfPeaks),
            CentroidResult,
            CentroidPeakWidth,
            MassList,
            PeakFlags,
            ArraySize
        )

        MassData = numpy.array(MassList.value)
        return MassData

    def close(self):
        self.DLL.Close()

def get_peak_value_from_mass_data(MassData,peak = 178.08):
    min = peak - 0.005
    max = peak + 0.005
    intensity = numpy.array([])
    for i in range(int(MassData.size/2)):
        if (MassData[0,i] >= min) & (MassData[0,i] <= max):
            intensity = numpy.append(intensity,MassData[1,i])
    if intensity.size == 0:
        return 0
    peak_value = intensity.max()
    return peak_value

if __name__ == '__main__':

    Path = os.getcwd()
    Files = ('Caffeine_01.raw',)
    OutFile = open('test.txt','w')
    for filename in Files:
        if filename.find('.raw') == -1:
            continue
        underline = filename.find('_')
        if underline != -1:
            name = filename[0:underline]
        else:
            name = filename[0:-4]

        raw = RawFile(filename)
        scan_num = raw.get_num_spectra()
        for j in range(scan_num):
            MassList = raw.get_mass_list(j+1)
            PeakValue = get_peak_value_from_mass_data(MassList, 195.09)
            OutFile.write(str(PeakValue))
            OutFile.write('\n')
            #for i in range(int(MassList.size/2)):
            #    OutFile.write(str(MassList[0,i]) + '\t' + str(MassList[1,i]) + '\n')
        raw.close()

    OutFile.close()
