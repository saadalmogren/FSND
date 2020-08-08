import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'admin', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        actor = Actor(name="test", age=25, gender="male")
        actor.insert()
        movie = Movie(title="test", release_date="2020-10-10")
        movie.insert()

    def tearDown(self):
        actors = Actor.query.all()
        for actor in actors:
            actor.delete()
        movies = Movie.query.all()
        for movie in movies:
            movie.delete()
        pass

    def test_get_actors_success(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(len(body['actors']), 1)

    def test_get_actors_error(self):
        res = self.client().get('/actors?page=100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_get_movies_success(self):
        res = self.client().get('/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(len(body['movies']), 1)

    def test_get_movies_error(self):
        res = self.client().get('/movies?page=100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_delete_actor_success(self):
        res = self.client().delete('/actors/7')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['actor_id'], 7)

    def test_delete_actor_error(self):
        res = self.client().delete('/actors/100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_delte_movie_success(self):
        res = self.client().delete('/movies/9')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['movie_id'], 9)

    def test_delete_movie_error(self):
        res = self.client().delete('/movies/100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_create_actor_success(self):
        res = self.client().post('/actors', json={
            'name': 'test',
            'age': 25,
            'gender': 'male'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['actor'])

    def test_create_actor_error(self):
        res = self.client().post('/actors', json={
            'name': 'test',
            'age': 25
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'UNPROCESSABLE ENTITY!')

    def test_create_movie_success(self):
        res = self.client().post('/movies', json={
            'title': 'test',
            'release_date': '2020-10-10',
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['movie'])

    def test_create_movie_error(self):
        res = self.client().post('/movies', json={
            'title': 'test'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'UNPROCESSABLE ENTITY!')

    def test_modify_actor_success(self):
        res = self.client().patch('/actors/15', json={
            'name': 'test2',
            'age': 26,
            'gender': 'male'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['actor'].get('name'), 'test2')
        self.assertEqual(body['actor'].get('age'), 26)

    def test_modify_actor_error(self):
        res = self.client().patch('/actors/100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')

    def test_modify_movie_success(self):
        res = self.client().patch('/movies/17', json={
            'title': 'test2',
            'release_date': '2021-10-10'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['movie'].get('title'), 'test2')
        self.assertEqual(body['movie'].get('release_date'),
                         'Sun, 10 Oct 2021 00:00:00 GMT')

    def test_modify_movie_error(self):
        res = self.client().patch('/movies/100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'RESOURCE NOT FOUND!')


if __name__ == "__main__":
    unittest.main()
