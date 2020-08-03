import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Movie, Actor, Role


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()
        if actors is None:
            return jsonify({
                'success': True,
                'actors': None
            })
        actors_format = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actors_format
        })


    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()
        if movies is None:
            return jsonify({
                'success': True,
                'movies': None
            })
        movie_format = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movie_format
        })


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'actor_id': actor_id
        })


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'movie_id': movie_id
        })


    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()
        if 'name' not in body or 'age' in body or 'gender' not in body:
            abort(422)
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'actor': actor.format()
        })


    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()
        if 'title' not in body or 'release_date' not in body:
            abort(422)
        title = body.get('title')
        release_date = body.get('release_date')
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def modify_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        body = request.get_json()
        if 'name' not in body or 'age' in body or 'gender' not in body:
            abort(422)

        try:
            actor.name = body.get('name')
            actor.age = body.get('age')
            actor.gender = body.get('gender')
            actor.update()
        except:
            abort(422)

        return jsonify({
            'sucess': True,
            'actor': actor.format()
        })


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def modify_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        body = request.get_json()
        if 'title' not in body or 'release_date' in body:
            abort(422)

        try:
            movie.title = body.get('title')
            movie.release_date = body.get('release_date')
            movie.update()
        except:
            abort(422)

        return jsonify({
            'sucess': True,
            'movie': movie.format()
        })


    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
    return app
