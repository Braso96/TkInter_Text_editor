import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Menubar:

    def __init__(self, parent):  # let's define our menu
        font_specs = ('ubuntu', 14)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        # we create submenus
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label='New file',
                                  accelerator='Ctrl+N',
                                  command=parent.new_file)
        file_dropdown.add_command(label='Open file',
                                  accelerator='Ctrl+O',
                                  command=parent.open_file)
        file_dropdown.add_command(label='Save',
                                  accelerator='Ctrl+S',
                                  command=parent.save)
        file_dropdown.add_command(label='Save as',
                                  accelerator='Ctrl+Shift+S',
                                  command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit',
                                  command=parent.master.destroy)  # destroy mode causes the program to close
        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label='Release Notes',
                                   command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label='About',
                                   command=self.show_about_message)

        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='About', menu=about_dropdown)

    # let's create popoups

    def show_about_message(self):
        box_title = 'About PyText'
        box_message = 'A simple Text Editor created with Python and Tkinter!'
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = 'Release Notes'
        box_message = 'Version 0.1 - Wilde'
        messagebox.showinfo(box_title, box_message)

# we create a statusbar that will inform the customer
# (user experience)
class Statusbar:

    def __init__(self, parent):
        font_specs = ('ubuntu', 12)
        self.status = tk.StringVar()  # let's create a string variable
        self.status.set('PyText - 0.1 Wilde')

        label = tk.Label(parent.textarea, textvariable=self.status, fg='black',
                         bg='lightgrey', anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)    # we offer a location within the interface geometry

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set('Your File has been Saved!')
        else:
            self.status.set('PyText - 0.1 Wilde')




class PyText:

    def __init__(self, master):
        master.title('Untitled - PyText')
        master.geometry('1200x700')

        font_specs = ('ubuntu', 18) # we set the font and size with a tuple
        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)     # we scroll the bar either with the mouse cursor or by pressing
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # we use pack to fill the screen
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y) # vertical

        self.menubar = Menubar(self) # I initialize the menubar section via the Menubar class to which I pass itself
        self.statusbar = Statusbar(self)
        self.bind_shortcuts()

    # we define all the functions of the submenu

    def set_window_title(self, name=None):  # allows us to change the title of the screen based on the file we are working on
        if name:
            self.master.title(name + ' - PyText')
        else:
            self.master.title('Untitled - PyText')

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension='.txt',
            filetypes=[('All Files', '*.*'),
                       ('Text File', '*.txt'),
                       ('Script Python', '*.py'),
                       ('Markdown Text', '*.md'),
                       ('File JavaScript', '*.js'),
                       ('Html Documents', '*.html'),
                       ('CSS Documents', '*.css')])
        if self.filename:
            self.textarea.delete(1.0, tk.END)  # clears the whole screen
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read()) # we fill with the contents of the selected file
                self.set_window_title(self.filename)

    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile='Untitled.txt',
                defaultextension='.txt',
                filetypes=[('All Files', '*.*'),
                           ('Text File', '*.txt'),
                           ('Script Python', '*.py'),
                           ('Markdown Text', '*.md'),
                           ('File JavaScript', '*.js'),
                           ('Html Documents', '*.html'),
                           ('CSS Documents', '*.css')])
            textarea_content = self.textarea.get(1.0, tk.END)  # we open the file in writing mode
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def bind_shortcuts(self):   # method for shortcuts
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.update_status)



if __name__ == "__main__":  # we instantiate the main window
    master = tk.Tk()
    pt = PyText(master)
    master.mainloop()
