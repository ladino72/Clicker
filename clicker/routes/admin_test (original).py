import json
import os.path
import os
import flask
import copy
import time
import datetime
import pdfkit
from functools import wraps

from flask import Blueprint, render_template, request, make_response, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash

from clicker.extensions import db
from clicker.models import User
from clicker.models import Commands
from ..utils.prepare_test import testOperations

admin_test = Blueprint('admin_test', __name__)

test_Op = testOperations(quiz_dir='clicker/quizzes', final_quiz='clicker/temp/quiz_prob.txt')


def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if not current_user.admin:
                return render_template('unauthorized.html')
            return func(*args, **kwargs)
        return authorize
    return decorator

@admin_test.route('/enable_test', methods=['POST'])

def enable_test():
    if request.method == 'POST':
        set_enable_test_status(True)
        set_end_test_status(False)
        set_grade_already_status(True)
        #print("Enable_test_status", get_enable_test_status())
        #print("End_test_status", get_end_test_status())
        #print("Auth_see_sol_status", get_auth_see_sol_status())
        #print("Grade_already_status", get_grade_already_status())

        #-----------------------------------------------------------------
        #Create an empty file with name equals year+month+day-hour+min+sec
        file_to_save_grades = create_file()
        print(file_to_save_grades)
        #----------------------------------------------------------------

        # We need to reset sent_answers for every user in the User table.
        set_sent_answers_to_false()

        with open('clicker/comandos/test_config.json') as json_file:
            data = json.load(json_file)

        chk_state = request.form['ischecked']
        print("chk_state:", chk_state, "chk_state type:", type(bool(chk_state)))
        # Watch out! chk_state come from ajax and it is NOT a python boolean variable!: true is not equal to True

        if chk_state == 'true':
            enable_test = True
        else:
            enable_test = False

        #
        if bool(enable_test):
            data["enable_test"] = True
        else:
            data["enable_test"] = False

        data["end_test"] = False
        data["auth_see_sol"] = False
        data["grade_already"] = False

        if enable_test:
            data["enable_test"] = True
            with open('clicker/comandos/test_config.json', 'w') as outfile:
                json.dump(data, outfile)
            return jsonify({'message': "Now, the students can see the test!", 'enable': "Yes"})
        else:
            data["enable_test"] = False
            with open('clicker/comandos/test_config.json', 'w') as outfile:
                json.dump(data, outfile)
            return jsonify({'message': "The students can not see the test yet!", 'enable': "No"})

@admin_test.route('/auth_see_sol', methods=['GET', 'POST'])

def auth_see_sol():
    if request.method == 'POST':

        with open('clicker/comandos/test_config.json') as json_file:
            data = json.load(json_file)

        auth_see_sol = request.form.getlist("auth_see_sol")
        print("XXXXXXXXXXX", bool(auth_see_sol))

        if bool(auth_see_sol):
            data["auth_see_sol"] = True
        else:
            data["auth_see_sol"] = False

        with open('clicker/comandos/test_config.json', 'w') as outfile:
            json.dump(data, outfile)

        return "", 204
    #return render_template("command_console.html")


@admin_test.route('/end_test', methods=['POST'])

def end_test():
    if request.method == 'POST':

        with open('clicker/comandos/test_config.json') as json_file:
            data = json.load(json_file)

        chk_state = request.form['ischecked']
        print("chk_state:", chk_state, "chk_state type:", type(bool(chk_state)))
        # Watch out! chk_state come from ajax and it is NOT a python boolean variable!: true is not equal to True

        if chk_state == 'true':
            end_test = True
        else:
            end_test = False

        if end_test:
            data["end_test"] = True
            with open('clicker/comandos/test_config.json', 'w') as outfile:
                json.dump(data, outfile)
            return jsonify({'message': "You have finalized the test!", 'enable': "Yes"})
        else:
            data["end_test"] = False
            with open('clicker/comandos/test_config.json', 'w') as outfile:
                json.dump(data, outfile)
            return jsonify({'message': "You have not finalized the test yet!", 'enable': "No"})

@admin_test.route('/command_console', methods=['GET'])
def command_console():
    with open('clicker/comandos/test_config.json') as json_file:
        data = json.load(json_file)

    data["enable_test"] = False
    data["end_test"] = False
    data["auth_see_sol"] = False
    data["grade_already"] = False

    with open('clicker/comandos/test_config.json', 'w') as outfile:
        json.dump(data, outfile)

    return render_template("command_console.html")


@admin_test.route('/subject_list', methods=['GET'])

def subject_list():
    if request.method == 'GET':
        return render_template('subject_list.html', quiz_names=test_Op.get_quiz_names())


@admin_test.route('/selected_subject/<id>')

def selected_subject(id):
    if id not in test_Op.get_quizzes():
        return flask.abort(404)
    quiz_ = copy.deepcopy(test_Op.get_quizzes()[id])
    return render_template('selector.html', id=id, quiz=quiz_)


@admin_test.route('/selector/<id>', methods=['GET', 'POST'])
def selector(id):
    if request.method == 'POST':
        selected_problems = request.form.getlist("prob")
        print("Selected problems:", selected_problems)
        chosen_prob = test_Op.get_selected_problems(selected_problems, id)

        # save selected problems
        test_Op.save_quiz()
        print("subject ID:", test_Op.id)

        # Here we need to reset sent_answers for every user in the User table.
        set_sent_answers_to_false()


        # return "<h1>" + json.dumps(selected_selected) + "</h1>"
        return render_template("selected.html", id=id, quiz=chosen_prob)

    return render_template("selector.html")


@admin_test.route('/view_test', methods=['GET', 'POST'])
@login_required
def view_test():
    # Next three lines are to find the current directory and its content
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))

    id = test_Op.get_ordered_quiz()
    if type(id) is not str:
        return render_template("NoAuthToSeePage.html")

    quiz_ = test_Op.quiz_questions
    ordering = test_Op.ordered_quiz_questions
    print("ID:", id)
    print("quiz_", quiz_)
    print("ordering", ordering)
    # -------------------------------------------------------
    user = User.query.filter_by(id=current_user.id).first()
    user.json_field = {'quiz_': quiz_, 'ordering': ordering, 'id': id}
    db.session.commit()
    user = User.query.filter_by(id=current_user.id).first()
    print("Info comming from database json_field", user.json_field['quiz_'][0]['options'])
    print("Info comming from database options", user.options)
    # ---------------------------------------------------

    # Watch out! The current directory is Clicker

    with open('clicker/comandos/test_config.json') as json_file:
        data = json.load(json_file)

    if data["enable_test"]:
        return render_template("test.html", id=id, quiz=quiz_, quiz_ordering=json.dumps(ordering))
    else:
        return render_template("index.html")


@admin_test.route('/check_test/<id>', methods=['POST'])
def check_test(id):
    if request.method == 'POST':

        with open('clicker/comandos/test_config.json') as json_file:
            data = json.load(json_file)

        if not data['end_test']:

            user = User.query.filter_by(id=current_user.id).first()

            if not user.sent_answers:
                user.sent_answers = True

                ordering = json.loads(request.form['ord'])
                req_form_items = request.form.items()
                test_Op.test_grade(ordering, req_form_items)
                sent_zero = test_Op.sent_zero
                if sent_zero:
                    render_template("test.html")

                print("------>>>>", "Type current_user", type(current_user), current_user.name, "your options")

                print("**********:", req_form_items)
                options = {k: v for k, v in request.form.items() if k != 'ord'}

                for i, j in options.items():
                    print(i, j)

                user.options = options
                db.session.commit()

                # ''''''''options from database''''''''''''''''''''''
                user = User.query.filter_by(id=current_user.id).first()
                for i, j in user.options.items():
                    print(i, j)
                # **********request.form.items()
                for i, j in request.form.items():
                    print(i, j)
                print("8888888888888888888888888---------")
                return render_template('wait_auth_sol.html')
            else:
                return render_template('impatient_see_sol.html')

        else:
            return render_template("expire_time.html")


@admin_test.route('/view_test_sol', methods=['GET'])
@login_required
def view_test_sol():
    with open('clicker/comandos/test_config.json') as json_file:
        data = json.load(json_file)

    user = User.query.filter_by(id=current_user.id).first()
    if current_user.is_active and current_user.sent_answers and data["auth_see_sol"] and data["end_test"] and \
            data["grade_already"] and current_user.id == user.id:
        quiz = user.results['quiz']
        answers_list = user.results['answers_list']
        number_correct = user.results['number_correct']
        print("quix:", quiz)
        print("answer_list", answers_list)
        print("Number_correct", number_correct)

        return render_template("answers_score.html", quiz=quiz, question_answer=zip(quiz['questions'], answers_list),
                               correct=number_correct, total=len(answers_list))
    else:
        return render_template("wait_wait_sol.html")


@admin_test.route('/grade', methods=['GET', 'POST'])
# @role_required("admin")
def grade():
    # Just grade students that sent answers

    with open('clicker/comandos/test_config.json') as json_file:
        data = json.load(json_file)

    if data["auth_see_sol"]:
        #return "<h1>" + "Prior to going on please disable the Show answers check box" + '</h1>'
        return jsonify({'message': "Prior to going on please disable the Show answers check box"})

    elif not data["end_test"]:
        #return "<h1>" + "Prior to grading please enable the End test check box" + '</h1>'
        return jsonify({'message': "Prior to grading please enable the End test check box"})

    else:
        user = User.query.filter_by(sent_answers=True).all()
        if user:
            # set heading to cvs statistics file
            test_Op.header_to_stats_file()

            for i in user:
                quiz = {"questions": i.json_field["quiz_"]}
                ordering = i.json_field["ordering"]
                req_form = i.options.items()
                print("quiz_", quiz)
                print("req_form", req_form)
                print("ordering_", ordering)
                test_Op.real_test_grade(ordering, req_form, quiz, i.name)

                quiz1 = test_Op.quiz
                answers_list = test_Op.answers_list
                number_correct = test_Op.number_correct
                results = {'quiz': quiz1, 'answers_list': answers_list, 'number_correct': number_correct}
                i.results = results
                i.score = number_correct
            db.session.commit()

            data["grade_already"] = True
            with open('clicker/comandos/test_config.json', 'w') as outfile:
                json.dump(data, outfile)

            return jsonify({'message': "Grading was done!", "enable": "enable_btns"})
            #return "<h1>" + "Grading was done!" + '</h1>'


        #return "<h1>" + "Nothing to grade" + '</h1>'
        return jsonify({'message': "Nothing to grade"})


@admin_test.route('/show_statistics', methods=['GET'])

def show_statistics():

    with open('clicker/comandos/test_config.json') as json_file:
        data = json.load(json_file)

    if data["grade_already"]:

        test_Op.do_stats()
        num_students = test_Op.num_students
        bar_labels = test_Op.bar_labels
        bar_values = test_Op.bar_values

        print("--------------->self:bar_values", bar_values)
        print("-------------->self:bar_values", bar_labels)

        binx = []
        user = User.query.filter_by(sent_answers=1).first()

        total_bin = len(user.options)
        biny = list(range(0, total_bin + 1, 1))
        for k in biny:
            binx.append(User.query.filter(db.and_(User.sent_answers == 1, User.score == k)).count())

        print("++++++++++++BIN:", biny, binx)

        print("y_max", max(binx))
        return render_template('chart.html',
                                           title1='STUDENT PERCENTAGE THAT ANSWERED CORRECTLY A QUESTION',
                                           title2='GRADE DISTRIBUTION, TEST IS WORTH '+str(len(binx)-1) +' POINTS AND EACH QUESTION IS WORTH 1 POINT',
                                           max1=100, max2=max(binx), labels1=bar_labels, labels2=biny,
                                           subtitle=num_students,
                                           values1=bar_values, values2=binx)
    else:

        return '<h1>' + "Please grade first" + "</h1>"

@admin_test.route('/help', methods=['POST'])
def help():
    return "<h1>" + "Ayuda" + "</h1>"


def set_sent_answers_to_false():
    # Here we need to reset sent_answers for every user in the User table.
    user = User.query.all()
    if user:
        for u in user:
            print("Users:", u.sent_answers)
            u.sent_answers = False
        db.session.commit()

def create_file():

    filename = time.strftime("%Y%m%d-%H%M" + ".txt")
    print("file name:", filename)
    with open(filename, 'w') as outfile:
        outfile.write("")
    return filename

@admin_test.route('/pdf', methods=['GET'])
def pdf():
    rendered = render_template('pdf_test.html', name="Luis Ladino")
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application-pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

@admin_test.route('/save_results_pdf', methods=['GET'])
def save_results_pdf():

    with open('clicker/comandos/test_config.json') as json_file:
        data = json.load(json_file)

    if not data["grade_already"]:
        return "<h1>" + "Prior to going on please grade the Test" + '</h1>'
    else:
        user = User.query.filter_by(sent_answers=True).all()
        if user:
            name_grade = {}
            user_1 = User.query.filter_by(sent_answers=True).first()
            total_questions = len(user_1.results['quiz']['questions'])

            for i in user:
                # The next 4 lines of code transform Luis Alejandro Ladino Gaspar into Ladino Gaspar Luis Alejandro
                full_name = i.name.split()
                last_names = full_name[-2:]
                first_names = full_name[:-2 or None]
                full_name = last_names + first_names
                name_grade[' '.join(full_name)] = i.results['number_correct']

                # name_grade[i.name] = i.results['number_correct']
                # print("Results:", i.name, i.results['number_correct'], len(i.results['quiz']['questions']))

            rendered = render_template('save_grades_pdf.html',
                                       name_grade=name_grade, total_questions=total_questions,
                                       date=datetime.datetime.now().strftime("%c"))

            css = ['clicker/static/assets/bootstrap/css/bootstrap.min.css', 'clicker/static/assets/css/styles.min.css']

            pdf = pdfkit.from_string(rendered, False,  css=css)

            response = make_response(pdf)
            response.headers['Content-Type'] = 'application-pdf'
            response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
            return response

        return "<h1>" + "Data were NOT saved!" + '</h1>'

@admin_test.route('/new_test', methods=['POST'])

def new_test():
    if request.method == 'POST':

        chk_state = request.form['ischecked']
        print("chk_state:", chk_state, "chk_state type:", type(bool(chk_state)))
        # Watch out! chk_state come from ajax and it is NOT a python boolean variable!: true is not equal to True

        if chk_state == 'true':
            new_test = True
        else:
            new_test = False

        print("new_test status:", new_test)

        if new_test:
            return jsonify({'message': "A new test has started. Please go to the Testbank and set up the test",
                            'enable': "Yes"})
        else:
            return jsonify({'message': "No test has started!", 'enable': "No"})


def get_end_test_status():
    command = Commands.query.filter_by(id=1).first()
    return command.end_test


def get_enable_test_status():
    command = Commands.query.filter_by(id=1).first()
    return command.enable_test


def get_auth_see_sol_status():
    command = Commands.query.filter_by(id=1).first()
    return command.auth_see_sol


def get_grade_already_status():
    command = Commands.query.filter_by(id=1).first()
    return command.grade_already


def set_end_test_status(value):
    command = Commands.query.filter_by(id=1).first()
    command.end_test = value
    db.session.commit()


def set_enable_test_status(value):
    command = Commands.query.filter_by(id=1).first()
    command.enable_test = value
    db.session.commit()

def set_auth_see_sol_status(value):
    command = Commands.query.filter_by(id=1).first()
    command.auth_see_sol = value
    db.session.commit()

def set_grade_already_status(value):
    command = Commands.query.filter_by(id=1).first()
    command.grade_already = value
    db.session.commit()

