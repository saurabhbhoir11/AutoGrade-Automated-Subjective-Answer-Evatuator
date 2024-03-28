import scoreGenerator
import answerSeparator
import math
import textExtractor
import keywordsExtractor
import pandas as pd
import os
import time


textExtractor = textExtractor.textExtractor()
separator = answerSeparator.answerSeparator()
score = scoreGenerator.scoreGenerator()
keywordsExtractor = keywordsExtractor.keyWords()


# with open("text.txt", "r", encoding="utf-8") as file:
#     text = file.read()

with open("answers.txt", "r", encoding="utf-8") as file:
    answers = file.read()

answers = separator.parse_questions(answers)
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


# text = textExtractor.extractText(filename)
#
# text = separator.parse_questions(text)
#
#
# print(load - start)
#
# solution = score.generateScore(text, answers)
#
# total = 0
#
# for key in solution:
#     if key in ["2A", "2B", "3A", "3B"]:
#         solution[key] = math.ceil(solution[key] * 10)
#     else:
#         solution[key] = math.ceil(solution[key] * 5)
#     total += solution[key]
# pprint.pprint(solution)
# pprint.pprint(total)


# def words_to_myspell(words, filename):
#     with open(filename, "w", encoding="utf-8") as f:
#         for word in words:
#             f.write(word + "\n")
#
#
# # Example string with words to convert
# with open("answers.txt", "r", encoding="utf-8") as f:
#     words_to_convert = f.read()
#
# # Convert the words to MySpell format and write to a file
# words_to_myspell(words_to_convert.split(), "custom_dict.txt")

dirName = "D:/papers/"

data = pd.DataFrame(columns=["RollNo", "Actual", "Predicted", "Difference"])
start = time.time()
for file in os.listdir(dirName):
    if file.endswith(".pdf"):
        filepath = os.path.join(dirName, file)
        predicted = getScore(filepath)
        filename = os.path.splitext(file)[0]
        rollno = filename.split("_")[0]
        actual = filename.split("_")[1]
        difference = abs(int(actual) - predicted)
        data = data._append(
            {
                "RollNo": rollno,
                "Actual": actual,
                "Predicted": predicted,
                "Difference": difference,
            },
            ignore_index=True,
        )
        print(time.time() - start)
        start = time.time()

print(data)
