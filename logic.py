import requests
from bs4 import BeautifulSoup
import os
import json
from time import time
from config import *

def load_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("McMaster University Grade Calculator")
        print("By Hashim Bukhtiar\n")
        print("1. View Current GPA Breakdown")
        print("2. Add Classes")
        print("3. Exit")

        try:
            choice = int(input("Enter choice: "))
            if choice in [1, 2, 3]:
                os.system('cls' if os.name == 'nt' else 'clear')
                return choice
        except:
            pass

def view_gpa_breakdown(filename):
    with open(filename, "r") as f:
        data = json.load(f)

        total_units = 0
        total_grade_points = 0

        for course in data["courses"]:
            code = course["code"]
            units = course["units"]
            grade = course["grade"]

            total_units += int(units)
            total_grade_points += int(grade) * int(units)

            print(f"{code}\t {grade}")
        
        cGPA_12 = round(total_grade_points / total_units, 2)
        cGPA_4 = GRADE_SCALE[round(cGPA_12)][-1]

        print(f"\ncGPA (12-pt): {cGPA_12}")
        print(f"cGPA (4-pt): {cGPA_4}")


        input("Press enter to continue...")

def add_classes(filename, courses_filename):
    with open(filename, "r") as f:
        data = json.load(f)
    
    while True:
        code = input("Enter course code (or 'quit'): ")

        if code == "quit":
            break

        name = get_course_name(code, courses_filename)
        units = get_course_units(code)
        grade = input("Enter course grade: ")
        new_class = {
            "code": code,
            "name": name,
            "units": units,
            "grade": grade
        }

        data["courses"].append(new_class)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)   

def get_course_name(course_code, filename):
    with open(filename, "r") as f:
        for line in f:
            line = line.split("-")
            if course_code in line[0]:
                return line[1].strip()
        return input(f"{course_code} not found. Enter course name: ")

def get_course_units(course_code):
    key = course_code.split()[1]
    units = ""
    for i in range(1, len(key)):
        if key[i].isdigit():
            units += key[i]
    return units

def update_class_data(filename):
    # (str, str) -> None
    # Takes a filename and URL and updates the course listings file with the page content
    
    print("Updating course listings...")
    print("Clearing file...")
    with open(filename, "w") as f:  pass # clear the file

    num_page = 1
    URL = f"https://academiccalendars.romcmaster.ca/content.php?catoid=53&catoid=53&navoid=10775&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={num_page}#acalog_template_course_filter"

    print(f"Accessing '{URL}'...")
    print("Parsing pages...")
    start_time = time()
    while True:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        page_content = format_cl_page_content(text)

        if page_content == ['']:
            end_time = time()
            break

        num_page += 1
        URL = f"https://academiccalendars.romcmaster.ca/content.php?catoid=53&catoid=53&navoid=10775&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={num_page}#acalog_template_course_filter"

        with open(filename, "a", encoding='utf-8') as f:
            for line in page_content:
                f.write(line + "\n")
    page_content = sorted(set(page_content))
    print(f"File updated, {num_page-1} pages parsed")
    print(f"Time elapsed: {round(end_time - start_time, 2)} seconds")

def format_cl_page_content(content):
    # (str) -> list
    # Takes a string of the page content and returns a list of the lines
    
    formatted_lines = []
    content = content.splitlines()

    for line in content:
        if "•" in line:
            formatted_line = line.replace("�", "").split()
            formatted_lines.append(" ".join(formatted_line[1:]))

    return formatted_lines

def calc_sem_GPA(course_data, round_to=1):
    # (dict) -> float
    # Takes a dictionary of course data and returns the semester GPA
    
    total_units = 0
    total_grade_points = 0

    for course in course_data.values():
        total_units += float(course['course_units'])
        total_grade_points += float(course['course_units']) * float(course['course_grade'])
    
    return round(total_grade_points / total_units, round_to)