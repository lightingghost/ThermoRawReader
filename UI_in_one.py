__author__ = 'lighting'

import comtypes
import comtypes.client
import numpy
import os
import tkinter as tk
from tkinter import filedialog
from ctypes import *
from comtypes.automation import *


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


class Image:
    def __init__(self, length=10, width=10):
        self.length = length
        self.width = width
        self.image_data = numpy.empty((self.length, self.width), dtype=numpy.ndarray)
        # self.image_data[:] = numpy.zeros((2, 2))
        self.ms_image = numpy.zeros((self.length, self.width))

    def load_raw(self, path):
        files = os.listdir(path)

        y = 0
        for filename in files:

            if filename.find('.raw') == -1:
                continue
            filepath = path + filename
            rawfile = RawFile(filepath)
            scan_num = rawfile.get_num_spectra()
            if scan_num < self.length:
                print('Not Enough Data Points')
            for x in range(self.length):
                mass_data = rawfile.get_mass_list(x + 1)
                self.image_data[x, y] = mass_data
            y = y + 1
            rawfile.close()
        return self.image_data

    def save_image_data(self, path):
        numpy.save(path, self.image_data)

    def load_image_data(self, filepath):
        self.image_data = numpy.load(filepath)
        return self.image_data

    def get_image(self, peak):
        for y in range(self.length):
            for x in range(self.width):
                self.ms_image[x, y] = get_peak_value_from_mass_data(self.image_data[x, y],peak)
        return self.ms_image

    def plot_image(self, method='contour'):
        import matplotlib.pyplot as plt
        x = range(self.length)
        y = range(self.width)
        max = self.ms_image.max()
        min = self.ms_image.min()
        plt.figure()
        plt.contourf(x, y, self.ms_image,numpy.arange(min,max,(max-min)/1000))
        plt.show()


class ImgProc(tk.Frame):

    def __init__(self,master=None):
        tk.Frame.__init__(self, master)

        #Frame 0

        self.frame_dim = tk.LabelFrame(master, text='Image Dimension')
        self.frame_dim.place(x=15, y=15, height=60, width=570)

        self.label_width = tk.Label(self.frame_dim, text='Width(Scan Num)')
        self.label_width.place(x=10, y=10, height=20, width=120)

        self.entry_width = tk.Entry(self.frame_dim)
        self.entry_width.place(x=140, y=10, height=20, width=60)

        self.label_length = tk.Label(self.frame_dim, text='Length(Num Files)')
        self.label_length.place(x=285, y=10, height=20, width=150)

        self.entry_length = tk.Entry(self.frame_dim)
        self.entry_length.place(x=440, y=10, height=20, width=60)


        #Frame 1
        self.frame_folder = tk.LabelFrame(master, text='Select Folder')
        self.frame_folder.place(x=15, y=90, height=60, width=570)

        self.entry_path = tk.Entry(self.frame_folder)
        self.entry_path.place(x=10, y=10, height=20, width=375)

        self.button_browse = tk.Button(self.frame_folder, text='Browse', command=self.browse_folder)
        self.button_browse.place(x=400, y=10, height=20, width=70)

        self.button_load_folder = tk.Button(self.frame_folder, text='Load', command=self.load_folder)
        self.button_load_folder.place(x=485, y=10, height=20, width=70)

        #Frame 2
        self.frame_info = tk.LabelFrame(master, text='Information')
        self.frame_info.place(x=15, y=165, height=60, width=570)

        self.label_scan = tk.Label(self.frame_info, text='Scan Number')
        self.label_scan.place(x=10, y=10, height=20, width=80)

        self.entry_scan = tk.Entry(self.frame_info)
        self.entry_scan.place(x=90, y=10, height=20, width=80)

        #Frame 3
        self.frame_img = tk.LabelFrame(master, text='Image File')
        self.frame_img.place(x=15, y=240, height=60, width=570)

        self.entry_img_path = tk.Entry(self.frame_img)
        self.entry_img_path.place(x=10, y=10, height=20, width=375)

        self.button_load_img = tk.Button(self.frame_img, text='Load', command=self.load_image)
        self.button_load_img.place(x=400, y=10, height=20, width=70)

        self.button_save_img = tk.Button(self.frame_img, text='Save', command=self.save_image)
        self.button_save_img.place(x=485, y=10, height=20, width=70)

        #Frame 4
        self.frame_plot = tk.LabelFrame(master, text='Plot')
        self.frame_plot.place(x=15, y=315, height=60, width=570)

        self.label_peak = tk.Label(self.frame_plot, text='Peak')
        self.label_peak.place(x=10, y=10, height=20, width=60)

        self.entry_peak = tk.Entry(self.frame_plot)
        self.entry_peak.place(x=90, y=10, height=20, width=60)

        self.button_plot = tk.Button(self.frame_plot, text='Plot Image', command=self.plot_image)
        self.button_plot.place(x=170, y=10, height=20, width=90)

    def browse_folder(self):
        self.path = filedialog.askdirectory()
        if self.path == None:
            return
        self.path = self.path + '/'
        self.entry_path.insert(0,self.path)

    def load_folder(self):
        self.width = int(self.entry_width.get())
        self.length = int(self.entry_length.get())
        self.image = Image(self.length, self.width)
        self.image.load_raw(self.path)

    def load_image(self):
        self.width = int(self.entry_width.get())
        self.length = int(self.entry_length.get())
        filename = filedialog.askopenfilename()
        if filename == None:
            return
        self.entry_img_path.insert(0,filename)
        self.image = Image(self.length, self.width)
        self.image.load_image_data(filename)

    def save_image(self):
        filepath = filedialog.asksaveasfile(mode='w',defaultextension='.npy')
        if filepath == None:
            return
        self.image.save_image_data(filepath.name)

    def plot_image(self):
        peak = float(self.entry_peak.get())
        self.image.get_image(peak)
        self.image.plot_image()


def start_gui():
    top = tk.Tk()
    top.title('Image Generator')
    top.geometry('600x450+0+0')
    app = ImgProc(top)
    app.mainloop()

if __name__ == '__main__':
    start_gui()