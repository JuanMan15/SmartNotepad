import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image
import pytesseract

def change_color():
    color = colorchooser.askcolor(title="Pick a color")
    text_area.config(fg=color[1])

def change_font(*args):
    text_area.config(font=(font_name.get(), size_box.get()))

def new_file():
    window.title("Untitled")
    text_area.delete(1.0, END)

def openFile():
    file = askopenfilename(defaultextension=".txt", file=[("All files", "*.*"),
                                                          ("Text Documents", "*.txt")])
    try:
        window.title(os.path.basename(file))
        text_area.delete(1.0, END)

        with open(file, "r") as f:
            text_area.insert(1.0, f.read())

    except Exception as e:
        print("Couldn't read file", e)

def saveFile():
    file = filedialog.asksaveasfilename(initialfile='untitled.txt',
                                        defaultextension=".txt",
                                        filetypes=[("All files", "*.*"),
                                                   ("Text Documents", "*.txt")])
    if file is None:
        return

    try:
        window.title(os.path.basename(file))
        with open(file, "w") as f:
            f.write(text_area.get(1.0, END))

    except Exception as e:
        print("Couldn't save file", e)

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def undo():
    text_area.event_generate("<<Undo>>")

def redo():
    text_area.event_generate("<<Redo>>")

def about():
    showinfo("About this program", "This is a program made by JuanMan")

def quit():
    window.destroy()

def extract_text_from_image():
    image_file = askopenfilename(defaultextension=".png", file=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if image_file:
        try:
            text = pytesseract.image_to_string(Image.open(image_file))
            text_area.insert(END, text)
        except Exception as e:
            print("Couldn't extract text from image", e)

window = Tk()
window.title("Notepad JuanMan :)")
file = None

window_width = 600
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

font_name = StringVar(window)
font_name.set("Sans Serif")

font_size = StringVar(window)
font_size.set("15")

# Create the text area with horizontal and vertical scrollbars
text_frame = Frame(window)
text_frame.pack(fill=BOTH, expand=1)

text_area = Text(text_frame, font=(font_name.get(), font_size.get()), undo=True, wrap=NONE)  # Enable undo/redo and disable wrapping
text_area.pack(side=LEFT, fill=BOTH, expand=1)

# Scrollbars
scroll_y = Scrollbar(text_frame, orient=VERTICAL, command=text_area.yview)
scroll_y.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroll_y.set)

scroll_x = Scrollbar(window, orient=HORIZONTAL, command=text_area.xview)
scroll_x.pack(side=BOTTOM, fill=X)
text_area.config(xscrollcommand=scroll_x.set)

frame = Frame(window)
frame.pack()

color_btn = Button(frame, text="Color", command=change_color)
color_btn.grid(row=0, column=0)

font_box = OptionMenu(frame, font_name, *font.families(), command=change_font)
font_box.grid(row=0, column=1)

size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font)
size_box.grid(row=0, column=2)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=openFile)
file_menu.add_command(label="Save", command=saveFile)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About...", command=about)

# Add Tesseract functionality
image_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Image", menu=image_menu)
image_menu.add_command(label="Extract Text from Image", command=extract_text_from_image)

# Bind shortcuts
window.bind('<Control-x>', lambda event: cut())
window.bind('<Control-c>', lambda event: copy())
window.bind('<Control-v>', lambda event: paste())
window.bind('<Control-z>', lambda event: undo())
window.bind('<Control-y>', lambda event: redo())

window.mainloop()
