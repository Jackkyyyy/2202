import tkinter as tk
import face_recognition
from tkinter import *
import os
from tkinter import filedialog, messagebox, ttk
import csv
import webbrowser


def compare():

    FilePath = directoryEntry.get()
    ImagePath = directorySuspect.get()
    print(ImagePath)
    Copy_to_path = "/home/deeplearning/sus/"
    d = 0
    known_image = face_recognition.load_image_file(ImagePath)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    images = []
    location = []
    for filename in os.listdir(FilePath +'/'):
        location = filename

        filename = face_recognition.load_image_file(FilePath + '/' + filename)

        unknown_encoding = face_recognition.face_encodings(filename)[0]
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        if results[0] == True:
            print("It's a picture of the culprit!")
            name = "suspect_%d.jpg" % d
            os.system("cp" + ' ' + FilePath + '/' + location + ' ' + Copy_to_path + name)
            d += 1

        else:
            print("It's not a picture of the culprit!")

    tk.messagebox.showinfo("Information", "Analysing of faces has been completed, suspect's picture is saved in /home/deeplearning/sus folder")


def browse():

    directoryEntry.configure(state=NORMAL)
    dirname = filedialog.askdirectory(initialdir="/", title="Select a directory to compare")
    directoryEntry.insert(END, dirname)
    directoryEntry.configure(state=DISABLED)

def browseSus():

    directorySuspect.configure(state=NORMAL)
    fileName = filedialog.askopenfilenames(title="Please select an image file of the target", filetypes=[("image Files", ".jpg, .jpeg")])
    directorySuspect.insert(END, fileName)
    directorySuspect.configure(state=DISABLED)

def DisplayData():

    with open('exitf.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            make = row['make']
            model = row['model']
            datetime = row['date time']
            datetimeO = row['date time original']
            latitude = row['latitude']
            longitude = row['longitude']
            GMap = row['GMap Url']
            address = row['address']

            tree.insert("", 0, values=(make, model, datetime, datetimeO, latitude, longitude, GMap, address))

    tk.messagebox.showinfo("Information", "Data has been displayed")


def cmd():
    os.system("python3 2202.py")
    tk.messagebox.showinfo("Information", "Extracting of metadata has been completed")

def DisplayMap():

    Filename = 'file:///'+os.getcwd()+'/' + '/gmplot.html'
    webbrowser.open_new_tab(Filename)
    tk.messagebox.showinfo("Information", "Map has been displayed successfully")


root = tk.Tk()
root.title("Team ABC - Analyzer")


extractFrame = tk.LabelFrame(root, height="100", bg="white", relief="sunken", bd="1")
extractFrame.pack(fill="x")

extractFrameLabel = tk.Label(extractFrame, text="Selected Data Set", font=("Arial", 9, 'bold'), bg="white")
extractFrameLabel.pack(anchor="w", padx=7, pady=(5, 0))

directoryEntry = tk.Entry(extractFrame, width="50", bg="white", state='disabled')
directoryEntry.pack(side="left", padx=(10, 0), pady=(0, 10))
directoryEntry.focus()

directoryButton = tk.Button(extractFrame, text="Browse", relief="flat", command=lambda: browse())
directoryButton.pack(side="left", padx=(0, 50), pady=(6, 10))

directorySuspect = tk.Entry(extractFrame, width="50", bg="white", state='disabled')
directorySuspect.pack(side="left", padx=(10, 0), pady=(0, 10))
directorySuspect.focus()

directorySuspectButton = tk.Button(extractFrame, text="Browse", relief="flat", command=lambda: browseSus())
directorySuspectButton.pack(side="left", padx=(0, 50), pady=(6, 10))

functionsFrame = tk.LabelFrame(root, height="650", bg="white", relief="sunken", bd="1")
functionsFrame.pack(fill="y", side="left")

functionsFrameLabel = tk.Label(functionsFrame, text="Functions", font=("Arial", 9, 'bold'), bg="white")
functionsFrameLabel.pack(anchor="w", padx=5, pady=10)

f8Button = tk.Button(functionsFrame, text="Function 1\nCompare", command=compare, width="25", relief="flat")
f8Button.pack(padx=20, pady=5)

f4Button = tk.Button(functionsFrame, text="Function 2\nExport metadata", command=cmd, width="25",
                     relief="flat")
f4Button.pack(padx=20, pady=5)

f3Button = tk.Button(functionsFrame, text="Function 3\nList Display data obtained", command=DisplayData, width="25",
                     relief="flat")
f3Button.pack(padx=20, pady=5)

f3Button = tk.Button(functionsFrame, text="Function 4\nList Display Map", command=DisplayMap, width="25",
                     relief="flat")
f3Button.pack(padx=20, pady=5)

TableMargin = Frame(root, bg="#F7F7F7", width="400")
TableMargin.pack(fill="both", expand= TRUE, side="top")
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("make", "model", "date time", "date time original", "latitude", "longitude", "GMap Url", "address", ), height=600, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('make', text="make", anchor=W)
tree.heading('model', text="model", anchor=W)
tree.heading('date time', text="date time", anchor=W)
tree.heading('date time original', text="date time", anchor=W)
tree.heading('latitude', text="latitude", anchor=W)
tree.heading('longitude', text="longitude", anchor=W)
tree.heading('GMap Url', text="GMap", anchor=W)
tree.heading('address', text="address", anchor=W)

tree.column('#0', stretch=False, minwidth=0, width=0)
tree.column('#1', stretch=False, minwidth=0, width=100)
tree.column('#2', stretch=False, minwidth=0, width=200)
tree.column('#3', stretch=False, minwidth=0, width=200)
tree.column('#4', stretch=False, minwidth=0, width=200)
tree.column('#5', stretch=False, minwidth=0, width=200)
tree.column('#6', stretch=False, minwidth=0, width=200)
tree.column('#7', stretch=False, minwidth=0, width=600)
tree.column('#8', stretch=False, minwidth=0, width=700)
tree.pack()

root.update()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.mainloop()