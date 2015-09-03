__author__ = 'lighting'

import tkinter as tk
from tkinter import filedialog
import img_gen

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
        self.image = img_gen.Image(self.length, self.width)
        self.image.load_raw(self.path)

    def load_image(self):
        self.width = int(self.entry_width.get())
        self.length = int(self.entry_length.get())
        filename = filedialog.askopenfilename()
        if filename == None:
            return
        self.entry_img_path.insert(0,filename)
        self.image = img_gen.Image(self.length, self.width)
        self.image.load_image_data(filename)

    def save_image(self):
        filepath = filedialog.asksaveasfile(mode='w',defaultextension='.npy')
        if filepath == None:
            return
        self.image.save_image_data(filepath)

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