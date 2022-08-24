from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import Movie, Director, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route('/')
@movies_ns.route('/page/<int:page>')
class MoviesView(Resource):
    def get(self, page=1):
        """
        Return all movies, 5 per page.
        * Return movies by director_id, # /movies?director_id=2
        ** Return movies by genre_id, # /movies?genre_id=4
        *** Return movies by director_id and movie_id, # ../movies?director_id=2&genre_id=4
        """
        movies_query = db.session.query(Movie)  # нереализованный объект запроса

        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        movies = movies_query.paginate(page, per_page=5, error_out=False)

        return movies_schema.dump(movies.items), 200

    def post(self):
        """
        Add movie
        """
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

        return None, 201


@movies_ns.route('/<int:pk>')
class MovieView(Resource):
    def get(self, pk: int):
        """
        Return movie by id
        """
        try:
            movie = db.session.query(Movie).filter(Movie.id == pk).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, pk):
        """
        Update or replace the movie by id
        """
        updated_rows = db.session.query(Movie).filter(Movie.id == pk).update(request.json)
        if updated_rows != 1:
            return None, 400
        db.session.commit()

        return None, 204

    def delete(self, pk: int):
        """
        Delete movie by pk
        """
        deleted_rows = db.session.query(Movie).filter(Movie.id == pk).delete()
        if deleted_rows != 1:
            return None, 400

        db.session.commit()
        return None, 200


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        """
        Return all directors
        """
        directors_query = db.session.query(Director).all()
        return directors_schema.dump(directors_query), 200

    def post(self):
        """
        Add movie
        """
        req_json = request.json
        new_director = Director(**req_json)

        with db.session.begin():
            db.session.add(new_director)

        return None, 201


@directors_ns.route('/<int:pk>')
class DirectorView(Resource):
    def get(self, pk: int):
        """
        Return director by id
        """
        try:
            director = db.session.query(Director).filter(Director.id == pk).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, pk):
        """
        Update or replace the director by id
        """
        updated_rows = db.session.query(Director).filter(Director.id == pk).update(request.json)
        if updated_rows != 1:
            return None, 400
        db.session.commit()

        return None, 204

    def delete(self, pk: int):
        """
        Delete director by pk
        """
        deleted_rows = db.session.query(Director).filter(Director.id == pk).delete()
        if deleted_rows != 1:
            return None, 400

        db.session.commit()
        return None, 200


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        """
        Return all genres
        """
        genres_query = db.session.query(Genre).all()
        return genres_schema.dump(genres_query), 200

    def post(self):
        """
        Add movie
        """
        req_json = request.json
        new_genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(new_genre)

        return None, 201


@genres_ns.route('/<int:pk>')
class GenreView(Resource):
    def get(self, pk: int):
        """
        Return genre by id
        """
        try:
            genre = db.session.query(Genre).filter(Genre.id == pk).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, pk):
        """
        Update or replace genre by id
        """
        updated_rows = db.session.query(Genre).filter(Genre.id == pk).update(request.json)
        if updated_rows != 1:
            return None, 400
        db.session.commit()

        return None, 204

    def delete(self, pk: int):
        """
        Delete genre by pk
        """
        deleted_rows = db.session.query(Genre).filter(Genre.id == pk).delete()
        if deleted_rows != 1:
            return None, 400

        db.session.commit()
        return None, 200


if __name__ == '__main__':
    app.run(debug=True)
