import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import font

# tkinter window
window = tk.Tk()
window.title("text-editor")
window.geometry("1200x660")

# variable for open_file_name
global open_file_name
open_file_name = False

def main():
    
    # create new file function
    def new_file():
        # delete old text
        my_text.delete("1.0", END)
        # update status bars
        window.title("new file | text-editor")
        status_bar.config(text="new file")
        
        global open_file_name
        open_file_name = False
    
    # create open file function
    def open_file():
        # delete old text
        my_text.delete("1.0", END)

        # update status bars
        get_file = filedialog.askopenfilename(initialdir="/home/ish/code/text-editor/", title="open file", filetypes=(("text files", "*.txt"), ("python", "*.py"), ("all files", "*.*")))
        # check filename
        if get_file:
            #  make filename global
            global open_file_name
            open_file_name = get_file
        
        name = get_file
        status_bar.config(text=f'saved {name}')
        name = name.replace("/home/ish/", "~/")
        window.title(f'{name} | text-editor')

        # open file
        get_file = open(get_file, 'r')
        content = get_file.read()
        # add file content to text box
        my_text.insert(END, content)
        # close opened file
        get_file.close()

    # save as function
    def save_as_file():
        get_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="/home/ish/code/text-editor/", title="save file", filetypes=(("text files", "*.txt"), ("python", "*.py"), ("all files", "*.*")))
        if get_file:
            # update status bars
            name = get_file
            status_bar.config(text=f'{name}')
            name = name.replace("/home/ish/", "~/")
            window.title(f'{name} | text-editor')

            # save file
            get_file = open(get_file, 'w')
            get_file.write(my_text.get(1.0, END))
            get_file.close()

    # save function
    def save_file():
        global open_file_name
        if open_file_name:
            # save file
            get_file = open(open_file_name, 'w')
            get_file.write(my_text.get(1.0, END))
            get_file.close()
            # add a pop up box here for the saved file


            
            status_bar.config(text=f'{open_file_name}')
        else:
            save_as_file()



    # main frame
    my_frame = Frame(window)
    my_frame.pack(pady=5)

    # scroll bar
    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side = RIGHT, fill = Y)
    
    # text box
    my_text = Text(my_frame, width = 50, height = 20, font = ("Fira Mono", 20), selectbackground="yellow", selectforeground="black", undo = True, yscrollcommand = text_scroll.set )
    my_text.pack()

    # configure
    text_scroll.config(command = my_text.yview)

    # menu bar
    my_menu = Menu(window)
    window.config(menu = my_menu)
    # file
    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="file", menu = file_menu)
    file_menu.add_command(label="new", command=new_file)
    file_menu.add_command(label="open", command=open_file)
    file_menu.add_command(label="save", command=save_file)
    file_menu.add_command(label="save as", command=save_as_file)

    file_menu.add_separator()
    file_menu.add_command(label="exit", command = window.quit )
    # edit
    edit_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="edit", menu = edit_menu)
    edit_menu.add_command(label="cut")
    edit_menu.add_command(label="copy")
    edit_menu.add_command(label="paste")
    edit_menu.add_command(label="undo")
    edit_menu.add_command(label="redo")

    # status bar at bottom
    status_bar = Label(window, text="ready, set, code!", anchor=E, bg="silver")
    status_bar.pack(fill=X, side=BOTTOM, ipady=5)

    # keeps window open
    window.mainloop()

# call function
main()

