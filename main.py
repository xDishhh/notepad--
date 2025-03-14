import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import font
import os
from pathlib import Path

# Get user's home directory
HOME_DIR = str(Path.home())

# tkinter window
window = tk.Tk()
window.title("text-editor")
window.geometry("1200x700")

# variable for open_file_name
global open_file_name
open_file_name = False

# variable for selected_text
global selected_text
selected_text = False

# variable for line numbers visibility
global show_line_numbers
show_line_numbers = True

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
        
        # Update line numbers
        update_line_numbers()
    
    # create open file function
    def open_file():
        # delete old text
        my_text.delete("1.0", END)

        # update status bars
        get_file = filedialog.askopenfilename(
            initialdir=HOME_DIR, 
            title="open file", 
            filetypes=(("text files", "*.txt"), ("python", "*.py"), ("all files", "*.*"))
        )
            
        # check filename
        if get_file:
            #  make filename global
            global open_file_name
            open_file_name = get_file
        
            name = get_file
            status_bar.config(text=f'opened {name}')
            
            # Replace the full home directory path with ~ for display
            name = name.replace(HOME_DIR, "~")
            window.title(f'{name} | text-editor')

            try:
                # open file
                with open(get_file, 'r') as file:
                    content = file.read()
                # add file content to text box
                my_text.insert(END, content)
                
            except Exception as e:
                status_bar.config(text=f'Error opening file: {str(e)}')
            
            # Update line numbers
            update_line_numbers()

    # save as function
    def save_as_file():
        get_file = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            initialdir=HOME_DIR, 
            title="save file", 
            filetypes=(("text files", "*.txt"), ("python", "*.py"), ("all files", "*.*"))
        )
            
        if get_file:
            # update status bars
            name = get_file
            status_bar.config(text=f'saved {name}')
            
            # Replace the full home directory path with ~ for display
            name = name.replace(HOME_DIR, "~")
            window.title(f'{name} | text-editor')

            try:
                # save file
                with open(get_file, 'w') as file:
                    file.write(my_text.get(1.0, END))
                    
                # Update global variable
                global open_file_name
                open_file_name = get_file
                    
            except Exception as e:
                status_bar.config(text=f'Error saving file: {str(e)}')

    # save function
    def save_file():
        global open_file_name
        if open_file_name:
            try:
                # save file
                with open(open_file_name, 'w') as file:
                    file.write(my_text.get(1.0, END))
                
                status_bar.config(text=f'saved {open_file_name}')
            except Exception as e:
                status_bar.config(text=f'Error saving file: {str(e)}')
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
                # Update line numbers
                update_line_numbers()


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
                # Update line numbers after pasting
                update_line_numbers()

    # dark mode 
    def dark_mode():
        window.config(bg='black')
        my_text.config(bg='black', fg='white', insertbackground='white')  # text box styling
        line_numbers.config(bg='#2d2d2d', fg='#909090')  # line numbers styling for dark mode
        status_bar.config(bg='gray', fg='white')  # status bar fixed gray color
        my_menu.config(bg='black', fg='white')  # menu bar color
        file_menu.config(bg='black', fg='white')  # file menu color
        edit_menu.config(bg='black', fg='white')  # edit menu color
        settings_menu.config(bg='black', fg='white') # settings menu color

    # light mode 
    def light_mode():
        window.config(bg='white')
        my_text.config(bg='white', fg='black', insertbackground='black')  # text box styling
        line_numbers.config(bg='#f0f0f0', fg='#606060')  # line numbers styling for light mode
        status_bar.config(bg='gray', fg='black')  # status bar fixed gray color
        my_menu.config(bg='grey', fg='black')  # menu bar color
        file_menu.config(bg='grey', fg='black')  # file menu color
        edit_menu.config(bg='grey', fg='black')  # edit menu color
        settings_menu.config(bg='grey', fg='black') # settings menu color
    
    # Toggle line numbers
    def toggle_line_numbers():
        global show_line_numbers
        show_line_numbers = not show_line_numbers
        
        if show_line_numbers:
            line_numbers.pack(side=LEFT, fill=Y)
            update_line_numbers()
        else:
            line_numbers.pack_forget()
    
    # Update line numbers function
    def update_line_numbers(event=None):
        if not show_line_numbers:
            return
            
        # Clear previous line numbers
        line_numbers.config(state=NORMAL)
        line_numbers.delete('1.0', END)
        
        # Get total number of lines
        total_lines = my_text.get('1.0', END).count('\n')
        
        # Create line numbers
        line_count = ''
        for i in range(1, total_lines + 1):
            line_count += f"{i}\n"
        
        # Insert line numbers
        line_numbers.insert('1.0', line_count)
        line_numbers.config(state=DISABLED)
        
        # Synchronize scrolling of line numbers with text
        top = my_text.yview()[0]
        line_numbers.yview_moveto(top)
    
    # Function to keep line numbers and text scroll in sync
    def on_text_scroll(*args):
        # Update the line numbers view
        line_numbers.yview_moveto(args[0])
        
        # Update the original scrollbar
        text_scroll.set(*args)

    # main frame
    my_frame = Frame(window)
    my_frame.pack(pady=0, fill=BOTH, expand=True)

    # scroll bar
    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side=RIGHT, fill=Y)
    
    # Line numbers text widget
    line_numbers = Text(my_frame, width=4, padx=4, highlightthickness=0, 
                         takefocus=0, bd=0, background='#f0f0f0', foreground='#606060',
                         font=("Fira Mono", 20), state=DISABLED)
    if show_line_numbers:
        line_numbers.pack(side=LEFT, fill=Y)
    
    # text box
    my_text = Text(my_frame, width=100, height=20, font=("Fira Mono", 20), 
                   selectbackground="yellow", selectforeground="black", undo=True)
    my_text.pack(side=LEFT, fill=BOTH, expand=True)

    # configure scrollbar
    my_text.config(yscrollcommand=on_text_scroll)
    text_scroll.config(command=my_text.yview)

    # menu bar
    my_menu = Menu(window)
    window.config(menu=my_menu)
    # file
    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="file", menu=file_menu)
    file_menu.add_command(label="new", command=new_file)
    file_menu.add_command(label="open", command=open_file)
    file_menu.add_command(label="save", command=save_file)
    file_menu.add_command(label="save as", command=save_as_file)

    file_menu.add_separator()
    file_menu.add_command(label="exit", command=window.quit)
    # edit
    edit_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="edit", menu=edit_menu)
    edit_menu.add_command(label="cut", command=lambda:cut_text(False), accelerator="(Ctrl+x)")
    edit_menu.add_command(label="copy", command=lambda:copy_text(False), accelerator="(Ctrl+c)")
    edit_menu.add_command(label="paste", command=lambda:paste_text(False), accelerator="(Ctrl+v)")
    edit_menu.add_separator()
    # undo and redo
    edit_menu.add_command(label="undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
    edit_menu.add_command(label="redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")

    # dark and light mode
    settings_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="settings", menu=settings_menu)
    settings_menu.add_command(label="toggle line numbers", command=toggle_line_numbers)
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
    
    # Bind text modifications and scrolling to update line numbers
    my_text.bind('<KeyPress>', update_line_numbers)
    my_text.bind('<KeyRelease>', update_line_numbers)
    my_text.bind('<MouseWheel>', update_line_numbers)
    
    # Initial line number update
    update_line_numbers()

    # keeps window open
    window.mainloop()

# call function
main()