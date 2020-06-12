import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','admin','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)

    def test_get_questions_error(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_questions_success(self):
        res = self.client().delete('/questions/17')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(Question.query.get(1), None)

    def test_delete_questions_error(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_questions_success(self):
        res = self.client().post('/questions', json={'question': 'test', 'answer': 'test', 'difficulty': 4, 'category': 1})

        self.assertEqual(res.status_code, 200)

    def test_create_questions_error(self):
        res = self.client().post('/questions/1', json={'question': 'test', 'answer': 'test', 'difficulty': 4, 'category': 1})

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')


    def test_search_questions_success(self):
        res = self.client().post('/questions/results', json={'searchTerm':'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 2)
    
    def test_search_questions_error(self):
        res = self.client().post('/questions/results')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_get_cate_questions_success(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 4)
        self.assertTrue(int(data['current_category']), 4)

    def test_get_cate_questions_error(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_quizzes_success(self):
        res = self.client().post('/quizzes', json={'previous_questions':[2, 4], 'quiz_category': {'id':1}})
        data = json.loads(res.data)
        question = data['question']
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(int(question['id']), [2,4])

    def test_get_quizzes_error(self):
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()