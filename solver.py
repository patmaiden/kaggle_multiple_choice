import random

global answerToIndex
answerToIndex = {"A":0, "B":1, "C":2, "D":3, "UNKNOWN":-1}
global indexToAnswer
indexToAnswer = ["A", "B","C", "D"]
"""
class Question
Holds a single question consisting of:
    - id (int) the question id
    - answerInd (int) the index of the correct answer in the answers array. -1 indicates a question where the answer is not known
    - answers (string array) the array of possibleanswers
"""
class Question():
    def __init__(self, i, question, correctAnswerLetter, answerArray):
        self.id = int(i)
        self.question = question
        self.answerInd = answerToIndex[correctAnswerLetter]
        self.answers = answerArray
    
    def __str__(self):
        return str(self.id) + " : " + self.question + "\n\t" + \
        ("A*: " if self.answerInd == 0 else "A: ") + self.answers[0] + '\n\t' + \
        ("B*: " if self.answerInd == 1 else "B: ") + self.answers[1] + '\n\t' + \
        ("C*: " if self.answerInd == 2 else "C: ") + self.answers[2] + '\n\t' + \
        ("D*: " if self.answerInd == 3 else "D: ") + self.answers[3]

"""
class Solver
Takes in data, labels the validation data with answers, and writes to an output file in specified format
    - training_f (string) the name of the file with the training data
    - validation_f (string) the name of the file with the validation data, lacking answers
    - output_f (string) the name of the output file, which will contain id,answer pairs for each question from validation_f
"""
class Solver():
    def __init__(self, training_f, validation_f, output_f):
        self.training = process_training_data(training_f)
        self.train()
        self.validation = process_validation_data(validation_f)
        self.solve()
        self.create_submission(output_f)
    
    def train(self):
        pass
    
    def solve(self):
        for q in self.validation:
            q.answerInd = random.randint(0,3)

    def create_submission(self, filename):
        with open(filename, 'w') as f:
            f.write('id,correctAnswer')
            for q in self.validation:
                f.write('\n' + str(q.id) + ',' + indexToAnswer[q.answerInd])


def process_training_data(filename):
    training_questions = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split('\t')
            if not len(parts) == 7: #id question correctAnswer answerA answerB answerC answerD
                raise Exception('Poorly formatted input line: \"'+line+'\"')
            elif not parts[0] == 'id':
                training_questions.append(Question(parts[0], parts[1], parts[2], parts[3:]))
    return training_questions

def process_validation_data(filename):
    validation_questions = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split('\t')
            if not len(parts) == 6: #id question answerA answerB answerC answerD
                raise Exception('Poorly formatted input line: \"'+line+'\"')
            elif not parts[0] == 'id':
                validation_questions.append(Question(parts[0], parts[1], "UNKNOWN", parts[2:]))
    return validation_questions

x = Solver('data/training_set.tsv', 'data/validation_set.tsv', 'data/derp.csv')
