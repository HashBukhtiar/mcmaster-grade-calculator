from tkinter import *
from tkinter import messagebox
from logic import *
from config import COURSE_LISTINGS_FILENAME
import threading

root = Tk()
root.title("McMaster Grade Calculator")
root.geometry("1080x720")
root.configure(bg="#7a003c")

def main_menu():
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
    GPA_screen_frame = Frame(root, bg="red", bd=5, relief="solid")
    GPA_screen_frame.place(relx=0.5, rely=0.5, anchor='c', relwidth=1, relheight=1)

    button1 = Button(GPA_screen_frame, text="Back", command=main_menu)
    button1.place(x=10, y=10)

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
        messagebox.showinfo("Done", "Classes updated successfully!")

main_menu()
root.mainloop()