import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def parse_answer_key(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f, "html.parser")
    table = soup.find("table", {"id": "ctl00_LoginContent_grAnswerKey"})
    data = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            data.append([cell.text for cell in cells])
    key = {}
    for arr in data:
        key[arr[2].strip('\n')] = arr[3].strip('\n')
    return key

def parse_response_sheet(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f, "html.parser")
    tables = soup.find_all("table", {"class": "menu-tbl"})
    values = {}
    data = []
    for table in tables:
        sub = []
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 0:
                sub.extend([cell.text for cell in cells])
        data.append(sub)
    answers = []
    tables = soup.find_all("table",{"class": "questionRowTbl"})
    for table in tables:
        sub = []
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 0:
                sub.extend([cell.text for cell in cells])
        answers.append(sub)
    counter = 0
    for question in data:
        if 'MCQ' in question and 'Answered' in question:
            chosen = int(question[15])
            question_id = question[3]
            answer_id = question[3+chosen*2]
            values[question_id] = answer_id
        if 'SA' in question:
            answer = answers[counter]
            if 'Answered' in question:
                question_id = question[3]
                answer_id = answer[5]
                values[question_id] = answer_id
        counter += 1
    return values

def calculate_score(key, values):
    correct = 0
    for question_id in key.keys():
        if question_id in values.keys() and key[question_id] == values[question_id]:
            correct += 1
    return correct

answer_key_file = select_file()
response_sheet_file = select_file()
answer_key = parse_answer_key(answer_key_file)
response_sheet = parse_response_sheet(response_sheet_file)
score = calculate_score(answer_key, response_sheet)
print("Your score is:", score)
