import use
import keywordsExtractor
import numpy as np
import pandas as pd

class scoreGenerator:
    def __init__(self):
        self.use = use.USE()
        self.keywordsExtractor = keywordsExtractor.keyWords()
        self.score = 0
        self.result = pd.DataFrame(columns = ['Question', 'Score'])

    def generateScore(self, studentResponse, answerKey):
        for key in answerKey:
            question = key
            answer = answerKey[key]
            studentAnswer = studentResponse[key]
            simScore = self.use.get_similarity_score(studentAnswer, answer)
            keyScore = self.keywordsExtractor.extract_keywords(studentAnswer, answer)
            simScore = 0.85 * simScore
            keyScore = 0.15 * keyScore
            self.score = simScore + keyScore
            self.result = self.result.append({'Question': question, 'Score': self.score}, ignore_index=True)


