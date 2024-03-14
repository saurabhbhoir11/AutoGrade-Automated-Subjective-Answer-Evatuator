import re
import pprint

class answerSeparator:
    def __init__(self):
        self.pattern = re.compile(r"Q\.(\d+)\.\s*(\w+)\.\s*(.*?)((?=Q\.\d)|$)", re.DOTALL)

    def parse_questions(self, text):
        questions = {}
        self.text = text
        matches = self.pattern.findall(self.text)
        for match in matches:
            question_num = match[0]
            sub_question = match[1].strip()
            sub_question_text = match[2].strip()
            question_key = f"{question_num}{sub_question}"
            questions[question_key] = sub_question_text
        return questions


text = """
Q.1. A. Define Deep Learning? Explain types of Neural Networks?
Q.1. B. Differentiate between DL and ML using following points? 
Data Dependency
Hardware Dependency
Training Time
Feature Selection
Interpretability
Q.1. C.  Why is Deep Learning so popular and in demand these days? Explain using following points. 
1. Datasets
2. Frameworks
3. Model Architecture
4. Hardware
5. Community 
Q.2. A. Differentiate between a biological neuron and McCulloch-Pitts neuron 
Q.2. B. What is perceptron? explain key components of a perceptron.
Q.2. C. What is Multilayer Perceptron? explain how it overcomes limitations of perceptron.
Q.2. D. Use proper notations (naming conventions) for the following neural network and find total as well as layer wise trainable parameters.
Q.3. A. Explain any five basic terminologies of Deep Learning
Q.3. B. Implement XOR function using McCulloch-Pitt neuron.
Q.3. C. Implement AND function using perceptron rule.
"""

if __name__ == "__main__":
    separator = answerSeparator()
    with open("text.txt", "r", encoding="utf-8") as file:
        text = file.read()
    questions = separator.parse_questions(text)
    pprint.pprint(questions)