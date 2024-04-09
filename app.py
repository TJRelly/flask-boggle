from boggle import Boggle
from flask import Flask, render_template, session, request, flash, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "it's a secret, so shhhhh!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
game = Boggle()

@app.route("/")
def home_page():
    """Renders home page with game board"""
    session['board'] = game.make_board()
    return render_template("game.html", board=session['board'])

@app.route("/guess", methods=["POST"])
def make_guess():
    """
    Checks if guesses are on the board
    Returns JSON
    """
    guess = request.json["guess"]
    board = session['board']
    result = game.check_valid_word(board, guess)
    
    return jsonify({"result": result})
    
@app.route("/score", methods=["POST"])
def end_game():
    """
    Checks for high score and games played
    Returns JSON
    """
    score = request.json["score"]
    session["games_played"] = session.get("games_played", 0) + 1
    games_played = session["games_played"]
    
    if score > session.get("high_score", 0):
        session["high_score"] = score
        score = session["high_score"]
        return jsonify({"high_score": score, "games_played" : games_played})
    
    return jsonify({"high_score": session.get("high_score", 0), "games_played": games_played})