import PyPDF2
import sys
import tkinter
import tkinter.filedialog

files = sys.argv[1:]
merger = PyPDF2.PdfFileMerger()


# if files:
#     for file in files:
#         merger.merge(file)

#    with open('Merged.pdf', 'w+') as new_file:
#        merger.write(new_file)

class ReorderableListbox(tkinter.Listbox):
    """ A Tkinter listbox with drag & drop reordering of lines """

    def __init__(self, master, **kw):
        kw['selectmode'] = tkinter.EXTENDED
        tkinter.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<Control-1>', self.toggleSelection)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.bind('<Leave>', self.onLeave)
        self.bind('<Enter>', self.onEnter)
        self.selectionClicked = False
        self.left = False
        self.unlockShifting()
        self.ctrlClicked = False

    def orderChangedEventHandler(self):
        pass

    def onLeave(self, event):
        # prevents changing selection when dragging
        # already selected items beyond the edge of the listbox
        if self.selectionClicked:
            self.left = True
            return 'break'

    def onEnter(self, event):
        # TODO
        self.left = False

    def setCurrent(self, event):
        self.ctrlClicked = False
        i = self.nearest(event.y)
        self.selectionClicked = self.selection_includes(i)
        if self.selectionClicked:
            return 'break'

    def toggleSelection(self, event):
        self.ctrlClicked = True

    def moveElement(self, source, target):
        if not self.ctrlClicked:
            element = self.get(source)
            Listelem = pdfList[source]
            del pdfList[source]
            pdfList.insert(target, Listelem)
            print(pdfList)
            self.delete(source)
            self.insert(target, element)

    def unlockShifting(self):
        self.shifting = False

    def lockShifting(self):
        # prevent moving processes from disturbing each other
        # and prevent scrolling too fast
        # when dragged to the top/bottom of visible area
        self.shifting = True

    def shiftSelection(self, event):
        if self.ctrlClicked:
            return
        selection = self.curselection()
        if not self.selectionClicked or len(selection) == 0:
            return

        selectionRange = range(min(selection), max(selection))
        currentIndex = self.nearest(event.y)

        if self.shifting:
            return 'break'

        lineHeight = 15
        bottomY = self.winfo_height()
        if event.y >= bottomY - lineHeight:
            self.lockShifting()
            self.see(self.nearest(bottomY - lineHeight) + 1)
            self.master.after(500, self.unlockShifting)
        if event.y <= lineHeight:
            self.lockShifting()
            self.see(self.nearest(lineHeight) - 1)
            self.master.after(500, self.unlockShifting)

        if currentIndex < min(selection):
            self.lockShifting()
            notInSelectionIndex = 0
            for i in selectionRange[::-1]:
                if not self.selection_includes(i):
                    self.moveElement(i, max(selection) - notInSelectionIndex)
                    notInSelectionIndex += 1
            currentIndex = min(selection) - 1
            self.moveElement(currentIndex, currentIndex + len(selection))
            self.orderChangedEventHandler()
        elif currentIndex > max(selection):
            self.lockShifting()
            notInSelectionIndex = 0
            for i in selectionRange:
                if not self.selection_includes(i):
                    self.moveElement(i, min(selection) + notInSelectionIndex)
                    notInSelectionIndex += 1
            currentIndex = max(selection) + 1
            self.moveElement(currentIndex, currentIndex - len(selection))
            self.orderChangedEventHandler()
        self.unlockShifting()
        return 'break'


pdfList = []


def mergeAndSave():
    print(pdfList)
    if pdfList:
        for pdf in pdfList:
            merger.append(pdf)
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.pdf')
        print(f.name)
        if f is None:
            return
        merger.write(f.name)
        f.close()
        # with open('Merged.pdf', 'bw+') as new_file:
        #     merger.write(new_file)


root = tkinter.Tk()
root.title("PDF Merger")
root.geometry("600x400")

root.bind('<Double-Button-1>', lambda e: lsbox.select_clear(0, tkinter.END))

menu = tkinter.Menu(root)
item = tkinter.Menu(menu)
item.add_command(label="new")
menu.add_cascade(label="new2", menu=item)
root.config(menu=menu)

lbl = tkinter.Label(root, text="Hello!")
lbl.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# txt = tkinter.Entry(root, width=8)
# txt.place(x=0, rely=0.1)

lsbox = ReorderableListbox(root)
lsbox.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.5, anchor=tkinter.CENTER)

scrbar = tkinter.Scrollbar(lsbox, orient='vertical')
scrbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
scrbar.config(command=lsbox.yview)
lsbox.config(yscrollcommand=scrbar.set)


def clicked():
    fls = tkinter.filedialog.askopenfilenames(parent=root, title="Choose a file")
    new_files = []
    for file in list(fls):
        pdfList.append(file)
        new_files.append((file))
    # i = lsbox.size()+1
    for pdf in new_files:
        name = pdf.split("/")[-1]
        lsbox.insert(tkinter.END, name)
        # i += 1
    # res = "You wrote: " + txt.get()
    # answer = tkinter.Label(root, text=res)
    # answer.grid(column=1, row=1)
    # lbl.configure(text="Well Done!")


def remove():
    selection = lsbox.curselection()
    for item in reversed(selection):
        lsbox.delete(item)
        del pdfList[item]
    print(pdfList)


btn = tkinter.Button(root, text="Add files", fg="green", command=clicked)
btn.place(relx=0.15, rely=0.8)

btn_merge = tkinter.Button(root, text="Merge and save", fg="green", command=mergeAndSave)
btn_merge.place(relx=0.85, rely=0.8, anchor=tkinter.NE)

btn_remove = tkinter.Button(root, text="Remove selected files", fg="green", command=remove)
btn_remove.place(relx=0.5, rely=0.8, anchor=tkinter.N)

root.mainloop()
