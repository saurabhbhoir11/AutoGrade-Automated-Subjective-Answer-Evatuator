import numpy as np
import keywordsExtractor
import use


class scoreGenerator:
    def __init__(self):
        self.use = use.USE()
        self.keywordsExtractor = keywordsExtractor.keyWords()

    def generateScore(self, studentResponse, answerKey):
        result = {}
        score = 0
        for key in studentResponse:
            question = key
            answer = answerKey[key]
            studentAnswer = studentResponse[key]
            simScore = self.use.get_similarity_score(studentAnswer, answer[0], question)
            keyScore = self.keywordsExtractor.extract_keywords(studentAnswer, answer[1], question)
            simScore = 0.80 * simScore
            keyScore = 0.20 * keyScore
            score = simScore + keyScore
            print((simScore, keyScore))
            result[question] = score
        return result

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


