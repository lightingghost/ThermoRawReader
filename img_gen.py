__author__ = 'lighting'

import numpy
import os


def get_peak_value_from_mass_data(MassData, peak):
    min = peak - 0.005
    max = peak + 0.005
    intensity = numpy.array([])
    for i in range(int(MassData.size / 2)):
        if (MassData[0, i] >= min) & (MassData[0, i] <= max):
            intensity = numpy.append(intensity, MassData[1, i])
    if intensity.size == 0:
        #print(0)
        return 0
    peak_value = intensity.max()
    #print(peak_value)
    return peak_value


class Image:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.image_data = numpy.empty((self.length, self.width), dtype=numpy.ndarray)
        # self.image_data[:] = numpy.zeros((2, 2))
        self.ms_image = numpy.zeros((self.length, self.width))

    def load_raw(self, path):
        import thermo_raw_reader as reader

        files = os.listdir(path)

        y = 0
        for filename in files:

            if filename.find('.raw') == -1:
                continue
            filepath = path + filename
            rawfile = reader.RawFile(filepath)
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


if __name__ == '__main__':
    length = 60
    width = 60
    path = 'D:\\Documents\\MyDocuments\\Zare\\Imaging\\08272015\\'

    image = Image(length, width)
    #image.load_raw(path)
    #image.save_image_data(path+'image_data.npy')
    image_data = image.load_image_data(path+'image_data.npy')
    image.get_image(195.09)
    image.plot_image()
