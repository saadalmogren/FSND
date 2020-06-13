import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# returns a paginiated list


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]

    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins.
   Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        format = {}
        for cate in categories:
            format[f'{cate.id}'] = cate.type
        return jsonify({
            'categories': format
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen
   for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate(request, questions)

        categories = Category.query.all()
        format = {}
        for cate in categories:
            format[f'{cate.id}'] = cate.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': format,
            'current_category': format['1']

        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
   the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True
        })
    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_diffucilty = int(body.get('difficulty', None))

        try:
            question = Question(new_question, new_answer,
                                new_category, new_diffucilty)
            question.insert()

            return jsonify({
                'success': True
            })
        except BaseException:
            abort(422)
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/results', methods=['POST'])
    def search_questions():
        body = request.get_json()
        if body is None:
            abort(422)
        term = body.get('searchTerm','')
        questions = Question.query.filter(Question.question.ilike(f'%{term}%'))

        format = [quest.format() for quest in questions]

        return jsonify({
            'questions': format,
            'total_questions': len(format),
            'current_category': 1

        })
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:cate_id>/questions')
    def get_cate_questions(cate_id):

        category = Category.query.get(cate_id)

        if category is None:
            abort(404)

        questions = Question.query.filter_by(category=cate_id)
        format = [quest.format() for quest in questions]

        return jsonify({
            'questions': format,
            'total_questions': len(format),
            'current_category': cate_id
        })

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.

  **func.random() was taken from
   https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
  '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        current_category = body.get('quiz_category')
        cate_id = int(current_category['id'])

        next_question = Question.query.order_by(func.random())
        # if the category is not all
        if cate_id != 0:
            next_question = next_question.filter(Question.category == cate_id)
            # if there is no previous question
            if len(previous_questions) != 0:
                next_question = next_question.filter(
                    ~Question.id.in_(previous_questions))
        # no next question to be displayed
        if next_question.first() is None:
            return jsonify({
                'question': next_question.first()
            })

        return jsonify({
            'question': next_question.first().format()
        })
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    return app
