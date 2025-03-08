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

# variable for selected_text
global selected_text
selected_text = False

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
    
    # cut function
    def cut_text(e):
        global selected_text
        # check if keyboard shortcut used
        if e:
            selected_text = window.clipboard_get()
        else:
            if my_text.selection_get():
                # get selected text
                selected_text = my_text.selection_get()
                # deleted selected text
                my_text.delete("sel.first", "sel.last")
                # clear clipboard then append selected_text
                window.clipboard_clear()
                window.clipboard_append(selected_text)


    # copy function
    def copy_text(e):
        # check how was text copied either shortcut or edit -> copy
        global selected_text
        if e:
            selected_text = window.clipboard_get()

        if my_text.selection_get():
            # get selected text
            selected_text = my_text.selection_get()
            # clear clipboard then append selected_text
            window.clipboard_clear()
            window.clipboard_append(selected_text)

    # paste function
    def paste_text(e):
        global selected_text
        # check if keyboard shortcut used
        if e:
            selected_text = window.clipboard_get()
        else:
            if selected_text:
                position = my_text.index(INSERT)
                my_text.insert(position, selected_text)
                window.clipboard_append(selected_text)

    # dark mode 
    def dark_mode():
        window.config(bg='black')
        my_text.config(bg='black', fg='white', insertbackground='white')  # text box styling
        status_bar.config(bg='gray', fg='white')  # status bar fixed gray color
        my_menu.config(bg='black', fg='white')  # menu bar color
        file_menu.config(bg='black', fg='white')  # file menu color
        edit_menu.config(bg='black', fg='white')  # edit menu color
        settings_menu.config(bg='black', fg='white') # settings menu color

    # light mode 
    def light_mode():
        window.config(bg='white')
        my_text.config(bg='white', fg='black', insertbackground='black')  # text box styling
        status_bar.config(bg='gray', fg='black')  # status bar fixed gray color
        my_menu.config(bg='white', fg='black')  # menu bar color
        file_menu.config(bg='white', fg='black')  # file menu color
        edit_menu.config(bg='white', fg='black')  # edit menu color
        settings_menu.config(bg='white', fg='black') # settings menu color



    # main frame
    my_frame = Frame(window)
    my_frame.pack(pady=5)

    # scroll bar
    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side = RIGHT, fill = Y)
    
    # text box
    my_text = Text(my_frame, width = 40, height = 20, font = ("Fira Mono", 20), selectbackground="yellow", selectforeground="black", undo = True, yscrollcommand = text_scroll.set )
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
    edit_menu.add_command(label="cut    (Ctrl+x)", command=lambda:cut_text(False))
    edit_menu.add_command(label="copy   (Ctrl+c)", command=lambda:copy_text(False))
    edit_menu.add_command(label="paste  (Ctrl+v)", command=lambda:paste_text(False))
    edit_menu.add_command(label="undo")
    edit_menu.add_command(label="redo")

    # dark and light mode
    settings_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="settings", menu = settings_menu)
    settings_menu.add_separator()
    settings_menu.add_command(label="dark mode", command=dark_mode)
    settings_menu.add_command(label="light mode", command=light_mode)

    # status bar at bottom
    status_bar = Label(window, text="ready, set, code!", anchor=E, bg="grey")
    status_bar.pack(fill=X, side=BOTTOM, ipady=5)

    # bindings
    window.bind('<Control-x>', cut_text)
    window.bind('<Control-c>', copy_text)
    window.bind('<Control-v>', paste_text)

    # keeps window open
    window.mainloop()

# call function
main()

