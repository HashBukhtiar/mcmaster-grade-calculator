import re

MCMASTER_COURSE_LISTINGS = "https://academiccalendars.romcmaster.ca/content.php?catoid=53&navoid=10775"
COURSE_LISTINGS_FILENAME = "course_listings.txt"
GRADE_SCALE = { # 12pt : (letter grade, percentage range, 4pt)
    0 : ("F", "0-49%", 0),
    1 : ("D-", "50-52%", 0.7),
    2 : ("D", "53-56%", 1),
    3 : ("D+", "57-59%", 1.3),
    4 : ("C-", "60-62%", 1.7),
    5 : ("C", "63-66%", 2),
    6 : ("C+", "67-69%", 2.3),
    7 : ("B-", "70-72%", 2.7),
    8 : ("B", "73-76%", 3),
    9 : ("B+", "77-79%", 3.3),
    10 : ("A-", "80-84%", 3.7),
    11 : ("A", "85-89%", 3.9),
    12 : ("A+", "90-100%", 4)
}
with open(COURSE_LISTINGS_FILENAME, 'r') as f: # All McMaster Course Codes in a List
    COURSE_CODES_LIST = [re.sub('[^a-zA-Z0-9 /]', '', line.split("-")[0].rstrip()) for line in f]