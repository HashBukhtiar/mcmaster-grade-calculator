from tkinter import *
from tkinter import messagebox
from logic import *
from config import COURSE_LISTINGS_FILENAME
import threading

# Autocomplete Class
class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        return [w for w in self.lista if w.lower().startswith(self.var.get().lower())]

# Main Window
root = Tk()
root.title("McMaster Grade Calculator")
root.geometry("1080x720")
root.configure(bg="#7a003c")

def main_menu():
    # Main Frame for app
    main_frame = Frame(root, bg="#7a003c")
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    app_title = Label(root, text="McMaster Grade Calculator", font=("Garamond", 50), bg="#7a003c", fg="#FDBF57")
    app_title.place(relx=0.5, rely=0.1, anchor='c')

    byline = Label(root, text="By: Hashim Bukhtiar", font=("Garamond", 20, 'bold'), bg="#7a003c", fg="#FDBF57")
    byline.place(relx=0.5, rely=0.2, anchor='c')

    # Frame for Main Menu Buttons
    global buttons_frame
    buttons_frame = Frame(main_frame, bg="#7a003c")
    buttons_frame.place(relx=0.5, rely=0.5, anchor='c', relwidth=0.7, relheight=0.4)

    # Main Menu Buttons
    global BUTTON_HEIGHT, VERTICAL_SPACING
    BUTTON_HEIGHT = 50
    VERTICAL_SPACING = 20

    button1 = Button(buttons_frame, text="Calculate GPA", command=calculate_GPA_screen, bg="#FDBF57", fg="#7a003c", font=("Garamond", 18, 'bold'))
    button1.place(relx=0.5, y=40, anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)

    button2 = Button(buttons_frame, text="Update Course Listings", command=update_data_screen, bg="#FDBF57", fg="#7a003c", font=("Garamond", 18, 'bold'))
    button2.place(relx=0.5, y=40 + BUTTON_HEIGHT + VERTICAL_SPACING, anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)

    button3 = Button(buttons_frame, text="Exit", bg="#FDBF57", fg="#7a003c", font=("Garamond", 18, 'bold'), command=root.quit)
    button3.place(relx=0.5, y=40 + 2*(BUTTON_HEIGHT +  VERTICAL_SPACING), anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)

def calculate_GPA_screen():
    GPA_screen_frame = Frame(root, bg="#7a003c")
    GPA_screen_frame.place(relx=0.5, rely=0.5, anchor='c', relwidth=1, relheight=1)

    fields_frame = Frame(GPA_screen_frame, bg="#7a003c", bd=2, relief="solid") # remove border once done
    fields_frame.place(x=10, y=160, anchor='nw', relwidth=0.5, relheight=0.8)

    def add_field():
        course_row = Frame(fields_frame, bg="#7a003c")
        course_row.pack(side='top', fill='x', padx=10)

        course_code = AutocompleteEntry(COURSE_CODES_LIST, course_row, bg='#5E6A71', width=20)
        course_code.pack(side='left', padx=20, pady=10)
        course_code.config(font=('Garamond', 14, 'bold'), fg='#FDBF57')

        course_units = Entry(course_row, bg='#5E6A71', width=5, justify='right')
        course_units.pack(side='left', padx=20, pady=10)
        course_units.config(font=('Garamond', 14, 'bold'), fg='#FDBF57')

        course_grade = Entry(course_row, bg='#5E6A71', width=12, justify='right')
        course_grade.pack(side='left', padx=20, pady=10)
        course_grade.config(font=('Garamond', 14, 'bold'), fg='#FDBF57')

    add_button = Button(GPA_screen_frame, text="Add Course", command=add_field, bg="#FDBF57", fg="#7a003c", font=("Garamond", 14))
    add_button.place(x=10, y=80, anchor='nw', relwidth=0.2, height=BUTTON_HEIGHT*0.7)

    course_code_label = Label(GPA_screen_frame, text="Course Code", bg="#7a003c", fg="#FDBF57", font=("Garamond", 14, 'bold'))
    course_code_label.place(x=40, y=130, anchor='nw')
    units_label = Label(GPA_screen_frame, text="Units", bg="#7a003c", fg="#FDBF57", font=("Garamond", 14, 'bold'))
    units_label.place(x=265, y=130, anchor='nw')
    grade_label = Label(GPA_screen_frame, text="Grade (/12)", bg="#7a003c", fg="#FDBF57", font=("Garamond", 14, 'bold'))
    grade_label.place(x=355, y=130, anchor='nw')

    back_button = Button(GPA_screen_frame, text="⬅ Back to Main Menu", command=main_menu, bg="#FDBF57", fg="#7a003c", font=("Garamond", 14))
    back_button.place(x=10, y=10, relwidth=0.2, height=BUTTON_HEIGHT*0.7)

def update_data_screen():
    loading_frame = Frame(buttons_frame, bg="#FDBF57")
    loading_frame.place(relx=0.5, y=40 + BUTTON_HEIGHT + VERTICAL_SPACING, anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)
    Label(loading_frame, text="Please wait, this could take up to 1 minute...", bg="#FDBF57", fg="#7a003c", font=("Garamond", 18, 'bold')).pack(fill=BOTH, expand=True)
    # Run the long running function in a separate thread so it doesn't block the GUI
    thread = threading.Thread(target=update_class_data, args=(COURSE_LISTINGS_FILENAME,))
    thread.start()
    root.after(100, check_if_done, loading_frame, thread)

def check_if_done(loading_frame, thread):
    if thread.is_alive():
        # If the long running function is still running, check again after 100 ms
        root.after(100, check_if_done, loading_frame, thread)
    else:
        # If the long running function is done, close the loading window and show a completion message
        loading_frame.destroy()
        messagebox.showinfo("Done", "Courses updated successfully!")

main_menu()
root.mainloop()