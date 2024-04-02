import scoreGenerator
import answerSeparator
import math
import textExtractor
import keywordsExtractor
import pandas as pd
import os
import time
import pprint


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
    text = textExtractor.extractText(filename)

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


total = getScore("C:/Users/hp/Downloads/papers/64_15.pdf")


pprint.pprint(total)


# dirName = "D:/papers/"
#
# data = pd.DataFrame(columns=["RollNo", "Actual", "Predicted", "Difference"])
# start = time.time()
# for file in os.listdir(dirName):
#     if file.endswith(".pdf"):
#         filepath = os.path.join(dirName, file)
#         predicted = getScore(filepath)
#         filename = os.path.splitext(file)[0]
#         rollno = filename.split("_")[0]
#         actual = filename.split("_")[1]
#         difference = abs(int(actual) - predicted)
#         data = data._append(
#             {
#                 "RollNo": rollno,
#                 "Actual": actual,
#                 "Predicted": predicted,
#                 "Difference": difference,
#             },
#             ignore_index=True,
#         )
#         print(time.time() - start)
#         start = time.time()
#
# print(data)
