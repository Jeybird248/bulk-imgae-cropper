import os
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

root = Tk()


def loadFiles():
    global filesNum
    global path
    try:
        path = filedialog.askdirectory(title="Choose your Image Folder", initialdir="insert path here")
        for file in os.listdir(path):
            try:
                Image.open(path + "/" + file)
                files.insert(END, file)
                filesNum += 1
                files.update()
            except:
                pass
    except FileNotFoundError:
        pass


def cropImage():
    global progress
    global path
    global filesDone
    widthSVal = int(widthS.get())
    widthEVal = int(widthE.get())
    heightSVal = int(heightS.get())
    heightEVal = int(heightE.get())
    outputVal = outputFolder.get()
    outputDir = os.path.join(path, outputVal)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    for index in files.curselection():
        file = files.get(index)
        try:
            im = Image.open(path + "/" + file)
            box = (widthSVal, heightSVal, widthEVal, heightEVal)
            cropimg = im.crop(box)
            if(CheckVar.get() == 0):
                cropimg.save(outputDir + "/crop.png", "png")
            else:
                renameVal = rename.get()
                if(CheckVar2.get() == 1):
                    print(outputDir + "/" + renameVal + str(filesDone) + ".png")
                    cropimg.save(outputDir + "/" + renameVal + str(filesDone) + ".png", "png")
                else:
                    print(outputDir + "/" + renameVal + str(filesDone+1) + ".png")
                    cropimg.save(outputDir + "/" + renameVal + str(filesDone+1) + ".png", "png")
            filesDone += 1
            progress.set(filesDone / filesNum)
            progressbar.update_idletasks()
        except Exception as e: 
            print(e)
    print("done")


def preview(self):
    global cropimg
    widthSVal = int(widthS.get())
    widthEVal = int(widthE.get())
    heightSVal = int(heightS.get())
    heightEVal = int(heightE.get())
    file = files.get(files.curselection())
    im = Image.open(path + "/" + file)
    cropimg = ImageTk.PhotoImage(im.crop((widthSVal, heightSVal, widthEVal, heightEVal)))
    canvas.config(width=widthEVal - widthSVal, height=heightEVal - heightSVal)
    canvas.create_image(0, 0, image=cropimg, anchor="nw")
    # previewlabel.config(width=widthEVal - widthSVal, height=heightEVal - heightSVal, image=cropimg)


def delImage():
    for file in files.curselection():
        files.delete(file)


filesNum = 0
filesDone = 0
progress = DoubleVar()
cropimg = PhotoImage()
path = ""
root.title("GUI")
root.resizable(False, False)
listframe = Frame(root)
listframe.pack(padx=10, pady=10)
inputframe = Frame(root)
inputframe.pack(side="left")
previewframe = Frame(root)
previewframe.pack(side="right", padx=10, pady=10)
buttonframe = Frame(root)
buttonframe.pack()
#################################################################
previewlabel = Label(previewframe, text="Preview:")
previewlabel.pack(padx=20, pady=10)
canvas = Canvas(previewframe, width=0, height=0)
canvas.pack(padx=10, pady=10)

label1 = Label(inputframe, text="Enter the starting width")
label1.pack()
widthS = Entry(inputframe, width=25)
widthS.pack(padx=20, pady=10)
widthS.insert(END, "0")

label2 = Label(inputframe, text="Enter the ending width")
label2.pack()
widthE = Entry(inputframe, width=25)
widthE.pack(padx=20, pady=10)
widthE.insert(END, "100")

label3 = Label(inputframe, text="Enter the starting height")
label3.pack()
heightS = Entry(inputframe, width=25)
heightS.pack(padx=20, pady=10)
heightS.insert(END, "0")

label4 = Label(inputframe, text="Enter the ending height")
label4.pack()
heightE = Entry(inputframe, width=25)
heightE.pack(padx=20, pady=10)
heightE.insert(END, "100")

label5 = Label(inputframe, text="Enter the output folder name")
label5.pack()
outputFolder = Entry(inputframe, width=25)
outputFolder.pack(padx=20, pady=10)
outputFolder.insert(END, "cropped")

label6 = Label(inputframe, text="Enter the file name format")
label6.pack()
rename = Entry(inputframe, width=25)
rename.pack(padx=20, pady=10)
rename.insert(END, "cropped_image")

progressbar = ttk.Progressbar(root, maximum=1, variable=progress)
progressbar.pack(padx=10, pady=10)

CheckVar = IntVar(value=1)
checkbutton = Checkbutton(root, text="Check to use a file name format", variable=CheckVar)
checkbutton.pack(pady=10)

CheckVar2 = IntVar(value=1)
zerobutton = Checkbutton(root, text="Check to start from 0", variable=CheckVar2)
zerobutton.pack(pady=10)

scrollbar = Scrollbar(listframe)
scrollbar.pack(side="right", fill="y")

files = Listbox(listframe, selectmode="extended", height=10, width=50, yscrollcommand=scrollbar.set)
files.bind('<Double-1>', preview)
files.pack(padx=10, pady=10)

scrollbar.config(command=files.yview)

##################################################################

loadButton = Button(buttonframe, text="Load Files", command=loadFiles)
loadButton.pack(padx=10, pady=10)

cropButton = Button(buttonframe, text="Crop Files", command=cropImage)
cropButton.pack(padx=10, pady=10)

delButton = Button(buttonframe, text="Delete Files", command=delImage)
delButton.pack(padx=10, pady=10)
#################################################################
root.mainloop()  
