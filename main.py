import logic
import config

def main():
    while True:
        option_selected = logic.load_menu()

        if option_selected == 1:
            logic.view_gpa_breakdown(config.GPA_FILE)

        elif option_selected == 2:
            logic.add_classes(config.GPA_FILE, config.COURSE_LISTINGS)

        else:
            break



if __name__ == '__main__':
    main()