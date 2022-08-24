# SkyPro_Homework_17

## This project works with SQLAlchemy, Flask, marshmallow

### API to search for movies with information about movies, directors and genres. API has the following endpoints:

* /movies - returns a list of all movies, divided by pages;
* /movies/id - returns detailed information about the movie.
* /directors/ - returns all directors,
* /directors/id - returns detailed information about the director,
* /genres/ - returns all genres,
* /genres/id - returns information about the genre listing the list of movies by genre,
* POST /movies/ - adds movies to the film library,
* PUT /movies/id - updates the movie,
* DELETE /movies/id - Deletes a movie.
* POST /directors/ - adds director to the library,
* PUT /directors/id - updates the director,
* DELETE /directors/id - Deletes a director.
* POST /genres/ - adds genre to the library,
* PUT /genres/id - updates the genre,
* DELETE /genres/id - Deletes a genre.

* a view returns movies with a specific director for a query like /movies/?director_id=1.
* a view returns movies with a specific genre for a query like /movies/?genre_id=1.
* a view returns movies with a specific director and genre for a query like /movies/?director_id=2&genre_id=4.


- Clone the project
- Add project requirements using the command 'pip install -r requirements.txt'
- Run app.py
- Use a browser to test HTTP-method GET 
- Use the Postman app to test HTTP-methods POST, PUT, DELETE
