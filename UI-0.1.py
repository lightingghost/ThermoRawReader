__author__ = 'lighting'

import tkinter as tk
from tkinter import filedialog

class ImgProc(tk.Frame):

    def __init__(self,master=None):
        tk.Frame.__init__(self, master)

        #Frame 1
        self.frame_folder = tk.LabelFrame(master, text='Select Folder')
        self.frame_folder.place(x=15, y=15, height=60, width=570)

        self.entry_path = tk.Entry(self.frame_folder)
        self.entry_path.place(x=10, y=10, height=20, width=375)

        self.button_browse = tk.Button(self.frame_folder, text='Browse', command=self.loadfolder)
        self.button_browse.place(x=400, y=10, height=20, width=70)

        self.button_load_folder = tk.Button(self.frame_folder, text='Load')
        self.button_load_folder.place(x=485, y=10, height=20, width=70)

        #Frame 2
        self.frame_info = tk.LabelFrame(master, text='Information')
        self.frame_info.place(x=15, y=90, height=60, width=570)

        self.label_scan = tk.Label(self.frame_info, text='Scan Number')
        self.label_scan.place(x=10, y=10, height=20, width=80)

        self.entry_scan = tk.Entry(self.frame_info)
        self.entry_scan.place(x=90, y=10, height=20, width=80)

        #Frame 3
        self.frame_img = tk.LabelFrame(master, text='IMG File')
        self.frame_img.place(x=15, y=165, height=60, width=570)

        self.entry_img_path = tk.Entry(self.frame_img)
        self.entry_img_path.place(x=10, y=10, height=20, width=375)

        self.button_load_img = tk.Button(self.frame_img, text='Load')
        self.button_load_img.place(x=400, y=10, height=20, width=70)

        self.button_save_img = tk.Button(self.frame_img, text='Save')
        self.button_save_img.place(x=485, y=10, height=20, width=70)

    def loadfolder(self):
        self.path = filedialog.askdirectory()
        self.entry_path.insert(0,self.path)





top = tk.Tk()
top.title('HeHe')
top.geometry('600x450+0+0')

app = ImgProc(top)
app.mainloop()