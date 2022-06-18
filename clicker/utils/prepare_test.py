import os
import json
import copy
import random
from functools import reduce
import csv


class testOperations:
    def __init__(self, quizzes=None, quiz_names=None, quiz_dir=None, final_quiz=None):
        if quizzes is None:
            quizzes = {}
        if quiz_names is None:
            quiz_names = {}
        if quiz_names is None:
            quiz_names = str
        if final_quiz is None:
            final_quiz = str

        self.quizzes = quizzes
        self.quiz_dir = quiz_dir
        self.quiz_names = quiz_names
        self.final_quiz = final_quiz
        self.chosen_prob = []
        self.id = str
        self.quiz_questions = []
        self.ordered_quiz_questions = []

        self.quiz = {}
        self.answers_list = []
        self.number_correct = int
        self.sent_zero = False

        self.bar_labels = []
        self.num_students = int
        self.bar_values = []

    def get_quizzes(self):
        for quiz in os.listdir(self.quiz_dir):
            print('Loading', quiz)
            self.quizzes[quiz] = json.loads(open(os.path.join(self.quiz_dir, quiz)).read())
        return self.quizzes

    def get_quiz_names(self):
        self.get_quizzes()
        self.quiz_names = zip(self.quizzes.keys(), list(map(lambda q: q['name'], self.quizzes.values())))
        return self.quiz_names

    def get_selected_problems(self, sel_probs, id):
        self.id = id
        quizn = copy.deepcopy(self.get_quizzes()[id])
        quiz_sel = quizn["questions"]
        self.chosen_prob = [quiz_sel[x] for x in range(len(quiz_sel)) for y in range(len(sel_probs)) if
                            sel_probs[y] == str(quiz_sel[x]["id"])]
        return self.chosen_prob

    def get_ordered_quiz(self):
        data = self.open_saved_quiz()
        quiz_ = {"questions": data}
        questions = list(enumerate(quiz_["questions"]))
        random.shuffle(questions)
        quiz_["questions"] = list(map(lambda t: t[1], questions))
        self.quiz_questions = quiz_["questions"]

        ordering = list(map(lambda t: t[0], questions))
        self.ordered_quiz_questions = ordering

        return self.id

    def save_quiz(self):
        # Save chosen_prob in a json file
        with open(self.final_quiz, 'w') as json_file:
            json.dump(self.chosen_prob, json_file)

    def open_saved_quiz(self):
        with open(self.final_quiz) as json_file:
            data = json.load(json_file)
        return data

    def ilen(self, iterable):
        return reduce(lambda sum, element: sum + 1, iterable, 0)

    def test_grade(self, ordering, req_form_items):
        data = self.open_saved_quiz()
        quiz = {"questions": data}
        quiz['questions'] = sorted(quiz['questions'], key=lambda q: ordering.index(quiz['questions'].index(q)))
        print("--------quiz['questions']-----------")
        print(quiz['questions'])
        self.quiz = quiz
        print("OOOOOOOOOOrequest_form_itemsOOOOOOOOOOO")
        print("type of request_form_items", type(req_form_items))
        for i, j in req_form_items:
            print(i, j)

        print("OOOOOOend of equest_form_items OOOOOOOOOOOOOOO")

        answers = dict(
            (int(k), quiz['questions'][int(k)]['options'][int(v)]) for k, v in req_form_items if k != 'ord')
        print("------------Answers-------------")
        print(answers)
        print("----correct answers dictionary------")

        correct_answer = {key: True for (key, value) in answers.items() if answers[key][1]}
        if correct_answer:
            print(correct_answer)

        idproblem = dict(
            (int(k), quiz['questions'][int(k)]['id']) for k, v in req_form_items if k != 'ord')
        print("------------Idproblem-------------")
        print(idproblem)
        # commom_keys is a set
        common_keys = correct_answer.keys() & idproblem.keys()
        print("------Id of solved problems")
        solved_prob_id = []
        if common_keys:
            for x in common_keys:
                print("problem id solved:", idproblem[x])
                solved_prob_id.append(idproblem[x])
        else:
            print("No problem solved correctly")
        if not len(answers.keys()):
            # "return flask.redirect(flask.url_for('quiz', id=id))
            self.sent_zero = True
            print("You did not check any answer!")

        for k in range(len(ordering)):
            if k not in answers:
                answers[k] = [None, False]
        print("--------Answer_list-----------")
        answers_list = [answers[k] for k in sorted(answers.keys())]
        print(answers_list)
        self.answers_list = answers_list

        number_correct = self.ilen(filter(lambda t: t[1], answers_list))
        self.number_correct = number_correct
        return "Done"

    def extract_prob_id(self):
        # This fucntion extract the problems id presented to the student and the results are stored in a list named
        # id_prob

        data = self.open_saved_quiz()

        id_selected_prob = [j["id"] for j in data]
        return id_selected_prob

    def header_to_stats_file(self):
        # stat_prob = dict((x, 0) for x in idproblem.values())
        stat_prob = dict((x, 0) for x in self.extract_prob_id())
        stat_prob["student_name"] = "student name"
        print("csv header:", stat_prob)
        with open('estad.csv', mode='w') as csv_file:
            fieldnames = stat_prob
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def real_test_grade(self, ordering, req_form_items, data, name):

        self.quiz = data
        answers = dict(
            (int(k), data['questions'][int(k)]['options'][int(v)]) for k, v in req_form_items)
        print("------------Answers-------------")
        print(answers)
        print("----correct answers dictionary------")

        correct_answer = {key: True for (key, value) in answers.items() if answers[key][1]}
        if correct_answer:
            print(correct_answer)

        idproblem = dict(
            (int(k), data['questions'][int(k)]['id']) for k, v in req_form_items)
        print("------------Idproblem-------------")
        print(idproblem)
        # commom_keys is a set
        common_keys = correct_answer.keys() & idproblem.keys()
        print("------Id of solved problems")
        solved_prob_id = []
        if common_keys:
            for x in common_keys:
                print("problem id solved:", idproblem[x])
                solved_prob_id.append(idproblem[x])
        else:
            print("No problem solved correctly")
        if not len(answers.keys()):
            # "return flask.redirect(flask.url_for('quiz', id=id))
            self.sent_zero = True
            print("You did not check any answer!")

        for k in range(len(ordering)):
            if k not in answers:
                answers[k] = [None, False]
        print("--------Answer_list-----------")
        answers_list = [answers[k] for k in sorted(answers.keys())]
        print(answers_list)
        self.answers_list = answers_list

        number_correct = self.ilen(filter(lambda t: t[1], answers_list))
        self.number_correct = number_correct

        stat_prob = dict((str(x), 0) for x in self.extract_prob_id())
        stat_prob["student_name"] = name
        print("csv header:", stat_prob)

        for x in solved_prob_id:
            stat_prob[str(x)] = 1

        with open('estad.csv', mode='a') as csv_file:
            fieldnames = stat_prob
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writerow({"0": "1", "11": "1", "student_name": "Peter Sagan"})
            writer.writerow(stat_prob)


        return "Done"

    def do_stats(self):

        with open('estad.csv', "r") as f:
            reader = csv.reader(f, delimiter=",")
            data = list(reader)
            self.num_students = len(data) - 1  # The header line is not counted
            print("Number of students", self.num_students)

        if self.num_students > 0:
            reader = csv.DictReader(open('estad.csv'))
            print("reader")
            # Watchout! raw is an An OrderedDict
            for raw in reader:
                print(raw)
            results = {}
            for x in self.extract_prob_id():
                reader = csv.DictReader(open('estad.csv'))
                a = 0
                for raw in reader:
                    for key, value in raw.items():
                        if key == str(x):
                            a = a + int(value)
                results[str(x)] = a
                print("# students responded problem with ID ", x, " are ", a)
            print("results:", results)

            self.bar_labels = ["Code:{}".format(i) for i in results.keys()]
            self.bar_values = [int(i) / self.num_students * 100 for i in results.values()]

            #print("--------------->self:bar_values",self.bar_values)
            # print("-------------->self:bar_values", self.bar_labels)


        if self.num_students == 0:
            return "No students in the file!"

