from tkinter import *
import tkinter as tk
from tkinter import messagebox
import PySimpleGUI as sg
import cv2
from PIL import Image, ImageTk
import AddChecker
import AnsKeyUtilis
import Improve

path = "TryTemp3.jpg"
#--------------------------------------------------------------Button Function
def add_checker():
    sg.theme('LightGreen')

    # define the window layout
    layout = [
      [sg.Image(filename='', key='-IMAGE-')],
      [sg.Button('ADD', size=(10, 1))],[sg.Button('Exit', size=(10,1))],[sg.Button('SAVE', size=(10,1))]
    ]

    # create the window and show it without the plot
    window = sg.Window('Add Checker', layout, location=(800, 100))

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture(0)
    #address = "http://192.168.1.104:8080/video"
    #cap.open(address)
    x=0
    while x != 1:
        event, values = window.read(timeout=20)
        #ret, frame = cap.read()
        frame = cv2.imread( path )
        imgGray = AnsKeyUtilis.capAdd(frame)

        if event == 'Exit' or event == sg.WIN_CLOSED:
            cap.release()
            window.close()

        elif event =='ADD':
            imgGray = AnsKeyUtilis.AnsImg()
            x = 1;
        elif event =='SAVE':
            imageArray = ([imgGray,AnsKeyUtilis.AnsImg()])
            imgGray = Improve.stackImages(imageArray, 0.5)
            x = 1;


        imgGray = cv2.resize(imgGray, (600, 700))
        imgbytes = cv2.imencode('.png', imgGray)[1].tobytes()
        window['-IMAGE-'].update(data=imgbytes)

#-------------------------------------------------------------Create Window Object MyMainForm
MyMainForm = Tk()

#------------------------------------------------------------Interface
design1 = Label(MyMainForm, bg = '#737CA1', width = 1400, height = 5).grid(row=0, column=0)
label1 = Label(MyMainForm, text='List of Checker', font=('bold', 14), pady=20).place(x=100, y=100)
checker_listbox = Listbox(MyMainForm, height=30, width=100).place(x=100, y=150)
add_checker_button = Button(MyMainForm, text = 'Add Checker', width=20, command=add_checker).place(x=200, y=650)
del_button = Button(MyMainForm, text = 'Delete Checker', width=20).place(x=400, y=650)

#-------------------------------------------------------------Window Size.
MyMainForm.geometry("1900x800")
Tk_Width = 1900
Tk_Height = 800
x_Left = int(MyMainForm.winfo_screenwidth() / 2 - Tk_Width / 2)
y_Top = int(MyMainForm.winfo_screenheight() / 2 - Tk_Height / 2)
MyMainForm.geometry("+{}+{}".format(x_Left, y_Top))
MyMainForm.title("ProChecker Main")
#------------------------------------------------------------Start MyMainForm mainloop
MyMainForm.mainloop()
