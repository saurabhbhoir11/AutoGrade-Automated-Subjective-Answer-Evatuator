import re
import textCorrector
import pprint


class answerSeparator:
    def __init__(self):
        self.pattern = re.compile(r"Q(\d+)([A-Z])\s*(.*?)((?=Q\d[A-Z])|$)", re.DOTALL)
        self.corrector = textCorrector.SpellingReplacer()

    def parse_questions(self, text):
        questions = {}
        self.text = text
        matches = self.pattern.findall(self.text)
        for match in matches:
            question_num = match[0]
            sub_question = match[1].strip()
            sub_question_text = match[2].strip().replace("(Begin answer for each question on a new page)", "")
            question_key = f"{question_num}{sub_question}"
            sub_question_text = self.corrector.replace_in_string(sub_question_text)
            questions[question_key] = sub_question_text
        return questions


text = """
Q1A Define Deep Learning? Explain types of Neural Networks?
Q1B Differentiate between DL and ML using following points? 
Data Dependency
Hardware Dependency
Training Time
Feature Selection
Interpretability
Q1C Why is Deep Learning so popular and in demand these days? Explain using following points 
1 Datasets
2 Frameworks
3 Model Architecture
4 Hardware
5 Community 
Q2A Differentiate between a biological neuron and McCulloch-Pitts neuron 
Q2B What is perceptron? explain key components of a perceptron
Q2C What is Multilayer Perceptron? explain how it overcomes limitations of perceptron
Q2D Use proper notations (naming conventions) for the following neural network and find total as well as layer wise trainable parameters
Q3A Explain any five basic terminologies of Deep Learning
Q3B Implement XOR function using McCulloch-Pitt neuron
Q3C Implement AND function using perceptron rule
"""

if __name__ == "__main__":
    separator = answerSeparator()
    with open("text.txt", "r", encoding="utf-8") as file:
        text = file.read()
    text = text
    questions = separator.parse_questions(text)
    pprint.pprint(questions)
