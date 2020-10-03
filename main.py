import PyPDF2
import sys
import tkinter
import tkinter.filedialog

files = sys.argv[1:]
merger = PyPDF2.PdfFileMerger()

if files:
    for file in files:
        merger.merge(file)

    with open('Merged.pdf', 'w+') as new_file:
        merger.write(new_file)

root = tkinter.Tk()
root.title("PDF Merger")
root.geometry("500x300")

menu = tkinter.Menu(root)
item = tkinter.Menu(menu)
item.add_command(label="new")
menu.add_cascade(label="new2", menu=item)
root.config(menu=menu)

lbl = tkinter.Label(root, text="Hello!")
lbl.place(relx=0.5, rely=0)

# txt = tkinter.Entry(root, width=8)
# txt.place(x=0, rely=0.1)


def clicked():
    fls = tkinter.filedialog.askopenfilenames(parent=root, title="Choose a file")
    pdfList = list(fls)
    lsbox = tkinter.Listbox(root)
    i = 1
    for pdf in pdfList:
        name = pdf.split("/")[-1]
        lsbox.insert(i, name)
        i+=1
    lsbox.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.5)
    # res = "You wrote: " + txt.get()
    # answer = tkinter.Label(root, text=res)
    # answer.grid(column=1, row=1)
    # lbl.configure(text="Well Done!")


btn = tkinter.Button(root, text="Add files", fg="green", command=clicked)

btn.place(relx=0.5, rely=0.8)

root.mainloop()
