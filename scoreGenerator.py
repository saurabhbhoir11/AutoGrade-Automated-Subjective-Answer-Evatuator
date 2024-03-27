import use
import keywordsExtractor
import numpy as np
import pandas as pd


class scoreGenerator:
    def __init__(self):
        self.use = use.USE()
        self.keywordsExtractor = keywordsExtractor.keyWords()
        self.score = 0
        self.result = {}

    def generateScore(self, studentResponse, answerKey):
        for key in studentResponse:
            question = key
            answer = answerKey[key]
            studentAnswer = studentResponse[key]
            simScore = self.use.get_similarity_score(studentAnswer, answer, question)
            keyScore = self.keywordsExtractor.extract_keywords(studentAnswer, answer, question)
            simScore = 0.85 * simScore
            keyScore = 0.15 * keyScore
            self.score = simScore + keyScore
            self.result[question] = self.score
        return self.result

    def getEmbeddings(self, sentences):
        for key in sentences:
            sentence = sentences[key]
            kw = self.keywordsExtractor.get_keywords(sentence)
            sen = [s for s in sentence.split(".")]
            embeddings = self.use.get_embeddings(sen)
            scores = [np.sum(embedding) for embedding in embeddings]
            # sentences[key] = (scores, kw)
            sentences[key] = scores
        return sentences


