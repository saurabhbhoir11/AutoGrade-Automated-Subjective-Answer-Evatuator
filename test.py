import scoreGenerator
import answerSeparator
import math
import textExtractor
import keywordsExtractor
import pandas as pd
import os
import time
from pprint import pprint


textExtractor = textExtractor.textExtractor()
separator = answerSeparator.answerSeparator()
score = scoreGenerator.scoreGenerator()
keywordsExtractor = keywordsExtractor.keyWords()


# with open("text.txt", "r", encoding="utf-8") as file:
#     text = file.read()

with open("answers.txt", "r", encoding="utf-8") as file:
    answers = file.read()

answers = separator.parse_answers(answers)
# with open("text.txt", "r", encoding="utf-8") as file:
#     text = file.read()


def getScore(filename):
    # text = textExtractor.extractText(filename)
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    text = separator.parse_questions(text)

    solution = score.generateScore(text, answers)

    total = 0

    for key in solution:
        if key in ["2A", "2B", "3A", "3B"]:
            solution[key] = math.ceil(solution[key] * 10)
        else:
            solution[key] = math.ceil(solution[key] * 5)
        total += solution[key]
    print(solution)
    return total


# total = getScore("D:/papers/35_36.pdf")
#
#
# pprint(total)


dirName = "D:/output/"

data = pd.DataFrame(columns=["RollNo", "Actual", "Predicted", "Difference", "Absolute Difference"])
start = time.time()
temp = start
val = 0
absVal = 0
count = 0
for file in os.listdir(dirName):
    if file.endswith(".txt"):
        filepath = os.path.join(dirName, file)
        predicted = getScore(filepath)
        filename = os.path.splitext(file)[0]
        print(filename)
        rollno = filename.split("_")[0]
        actual = filename.split("_")[1]
        difference = int(actual) - predicted
        absDifference = abs(int(actual) - predicted)
        val = val + difference
        absVal = absVal + absDifference
        data = data._append(
            {
                "RollNo": rollno,
                "Actual": actual,
                "Predicted": predicted,
                "Difference": difference,
                "Absolute Difference": absDifference,
            },
            ignore_index=True,
        )
        print(time.time() - temp)
        temp = time.time()
        count += 1

avg = val / count
absAvg = absVal / count
print(absAvg)
print(avg)
pprint(data)
print(time.time() - start)
