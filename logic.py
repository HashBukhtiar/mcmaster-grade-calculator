import requests
from bs4 import BeautifulSoup
from time import time

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

def option1():
    print("Option 1 selected")

def option2():
    print("Option 2 selected")