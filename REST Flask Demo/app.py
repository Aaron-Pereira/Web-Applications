# Run app -> python3.11 app.py

# Imports
from flask import Flask, request, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Test database
movies = [
    {"id": 1, "title": "Inception", "rank": 9},
    {"id": 2, "title": "Interstellar", "rank": 10}
]

# Movie class
class MovieList(Resource):
    # Return movies, sorted descending
    def get(self):
        return {"data": sorted(movies, key=lambda x: x['rank'], reverse=True)}, 200
    
    # Adds a new movie with unique id
    def post(self):
        new_movie = request.json
        new_movie["id"] = len(movies) + 1
        movies.append(new_movie)
        return {"message": "Movie added", "data": new_movie}, 201


class Movie(Resource):
    # Find movie by id, update it
    def put(self, id):
        movie = next((m for m in movies if m["id"] == id), None)
        if movie:
            movie.update(request.json)
            return {"message": "Movie updated", "data": movie}, 200
        return {"message": "Movie not found"}, 404
    
    # Find movie by id, delete it
    def delete(self, id):
        global movies
        movies = [m for m in movies if m["id"] != id]
        return {"message": "Movie deleted"}, 200

# API routes
# Listing and adding movies
api.add_resource(MovieList, "/movies")
# Updating and deleting movies
api.add_resource(Movie, "/movies/<int:id>")


@app.route('/')
def home():
    return render_template("index.html", movies=sorted(movies, key=lambda x: x['rank'], reverse=True))

if __name__ == "__main__":
    app.run(debug=True)
