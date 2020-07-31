import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Actor, Movie

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'admin', '5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        
        actor = Actor(name = "test", age = 25, gender = "male")
        actor.insert()
        movie = Movie(title = "test", release_date = "2020-10-10")
        movie.insert()
    def tearDown(self):
        pass
    
    if __name__ == "__main__":
    unittest.main()