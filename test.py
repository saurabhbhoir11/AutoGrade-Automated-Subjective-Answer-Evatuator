import scoreGenerator
import answerSeparator
import math
import textExtractor
import keywordsExtractor

# import pandas as pd
import time
import pprint


start = time.time()

textExtractor = textExtractor.textExtractor()
separator = answerSeparator.answerSeparator()
score = scoreGenerator.scoreGenerator()
keywordsExtractor = keywordsExtractor.keyWords()

load = time.time()

print(load - start)


# with open("text.txt", "r", encoding="utf-8") as file:
#     text = file.read()

with open("answers.txt", "r", encoding="utf-8") as file:
    answers = file.read()

answers = separator.parse_questions(answers)
# with open("text.txt", "r", encoding="utf-8") as file:
#     text = file.read()

start = load
load = time.time()
print(load - start)

filename = "D:/papers/35_36.pdf"

text = textExtractor.extractText(filename)

text = separator.parse_questions(text)

start = load
load = time.time()
print(load - start)

solution = score.generateScore(text, answers)

total = 0

for key in solution:
    if key in ["2A", "2B", "3A", "3B"]:
        solution[key] = math.ceil(solution[key] * 10)
    else:
        solution[key] = math.ceil(solution[key] * 5)
    total += solution[key]
pprint.pprint(solution)
pprint.pprint(total)
end = time.time()
print(end - load)


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
