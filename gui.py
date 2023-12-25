from tkinter import *

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
    buttons_frame = Frame(main_frame, bg="#7a003c")
    buttons_frame.place(relx=0.5, rely=0.5, anchor='c', relwidth=0.7, relheight=0.4)

    # Main Menu Buttons
    BUTTON_HEIGHT = 50
    VERTICAL_SPACING = 20

    button1 = Button(buttons_frame, text="Calculate GPA", command=calculate_GPA_screen)
    button1.place(relx=0.5, y=40, anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)

    button2 = Button(buttons_frame, text="Update Course Listings")
    button2.place(relx=0.5, y=40 + BUTTON_HEIGHT + VERTICAL_SPACING, anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)

    button3 = Button(buttons_frame, text="Exit", command=root.quit)
    button3.place(relx=0.5, y=40 + 2*(BUTTON_HEIGHT +  VERTICAL_SPACING), anchor='n', relwidth=0.7, height=BUTTON_HEIGHT)

def calculate_GPA_screen():
    GPA_screen_frame = Frame(root, bg="red", bd=5, relief="solid")
    GPA_screen_frame.place(relx=0.5, rely=0.5, anchor='c', relwidth=1, relheight=1)

    button1 = Button(GPA_screen_frame, text="Back", command=main_menu)
    button1.place(x=10, y=10)

main_menu()
root.mainloop()