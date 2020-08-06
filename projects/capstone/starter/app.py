import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Movie, Actor, Role
from auth import AuthError, requires_auth

ITEMS_PER_PAGE = 10
def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]

    return items[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        actors_format = paginate(request, actors)

        if len(actors_format) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': actors_format
        })


    
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        movie_format = paginate(request, movies)
        if len(movie_format)==0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': movie_format
        })

    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id, payload):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'actor_id': actor_id
        })

    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id, payload):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'movie_id': movie_id
        })

    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if 'name' not in body or 'age' not in body or 'gender' not in body:
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
    @requires_auth('post:movies')
    def create_movie(payload):
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
    @requires_auth('patch:actors')
    def modify_actor(actor_id, payload):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        body = request.get_json()
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(422)

        try:
            actor.name = body.get('name')
            actor.age = body.get('age')
            actor.gender = body.get('gender')
            actor.update()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def modify_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        body = request.get_json()
        if 'title' not in body or 'release_date' not in body:
            abort(422)

        try:
            movie.title = body.get('title')
            movie.release_date = body.get('release_date')
            movie.update()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'RESOURCE NOT FOUND!'

        }),404
    @app.errorhandler(422)
    def unproccesable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'UNPROCESSABLE ENTITY!'

        }),422
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'METHOD NOT ALLOWED!'

        }),405
    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code
        
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
    return app
