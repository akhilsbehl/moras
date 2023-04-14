from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

from kanalib import AnalyticsUtils
from kanalib import ANALYTICS
from kanalib import CHOICES
from kanalib import get_final_scores
from kanalib import get_random_kana_romaji_pair
from kanalib import validate_input_against_answer

app = Flask(__name__, static_folder='static')
app.secret_key = "supersecretkey"

PAIR = {"kana": "", "answer": ""}


@app.route("/")
def index():
    return render_template("index.html", choices=CHOICES)


@app.route("/practice/<ktype>")
def practice(ktype):
    global PAIR
    PAIR["kana"], PAIR["answer"] = get_random_kana_romaji_pair(ktype)
    return render_template("practice.html", ktype=ktype, kana=PAIR["kana"])


@app.route("/check_answer", methods=["POST"])
def check_answer():
    ktype = request.form["ktype"]
    kana, answer = PAIR["kana"], PAIR["answer"]
    user_input = request.form["user_input"]
    correct = validate_input_against_answer(user_input, answer)
    ANALYTICS.update_analytics_data(ktype, kana, correct)
    score = ANALYTICS.get_score("This", ktype)
    print(score)
    flash(f"Score: {score[2]:.1f}% ({score[1]}/{score[0]})")
    return redirect(url_for("practice", ktype=ktype))


@app.route("/finish_session/<ktype>")
def finish_session(ktype):
    final_scores = get_final_scores(ktype)
    global ANALYTICS
    ANALYTICS.save_analytics_data()
    # Actually reset
    ANALYTICS = AnalyticsUtils()
    return render_template(
        "final_scores.html",
        ktype=ktype,
        final_scores=final_scores,
    )


@app.route("/download_practice_data", methods=["GET"])
def download_practice_data():
    try:
        return send_from_directory(
            directory=".", path="analytics.csv", as_attachment=True
        )
    except FileNotFoundError:
        return redirect(url_for("index", _external=True, _scheme="https"))


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/visualize_analytics")
def visualize_analytics():
    return render_template("visualize.html")


if __name__ == "__main__":
    app.run(debug=True)
