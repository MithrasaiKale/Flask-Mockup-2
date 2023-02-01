from flask import Flask, jsonify, request

from storage import all_movies, liked_movies, disliked_movies, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-movie")
def get_movie():
    movie_data={
     "title": all_movies[0][19],
     "poster_link" : all_movies[0][27],
     "release_date" : all_movies[0][13] or "N/A",
     "duration" : all_movies[0][15],
     "rating" : all_movies[0][20],
     "overview" : all_movies[0][9]
    }
    return jsonify({
        "data" : movie_data, "status" : "success"
    })

@app.route("/liked-movie", methods=["POST"])
def liked_movie():
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201


@app.route("/disliked-movie", methods=["POST"])
def disliked_movie():
    movie = all_movies[0]
    disliked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201


@app.route("/did-not-watch", methods=["POST"])
def did_not_watch():
    movie = all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-movies")
def popular_movies():
    movie_data=[]
    for i in output:
        d={
          "title": i[0],
          "poster_link" : i[1],
          "release_date" : i[2] or "N/A",
          "runtime" : i[3],
          "vote_average" : i[4],
          "overview" : i[5]
        }
        movie_data.append(d)
    return jsonify({
        "data" : movie_data, "status" : "success"
    }),200

@app.route("/recommended-movies")
def recommended_movies():
    all_recommended=[]
    for i in liked_movies:
        output = get_recommendations(i[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        d={
          "title": recommended[0],
          "poster_link" : recommended[1],
          "release_date" : recommended[2] or "N/A",
          "runtime" : recommended[3],
          "vote_average" : recommended[4],
          "overview" : recommended[5]
        }
        movie_data.append(d)
    return jsonify({
        "data" : movie_data, "status" : "success"
    }),200           
if __name__ == "__main__":
    app.run(debug=True)