from flask import Flask, render_template, request
from models import db, LifestyleLog
from recommendations import generate_recommendation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifestyle.db'
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    if request.method == "POST":
        sleep = int(request.form["sleep"])
        exercise = int(request.form["exercise"])
        mood = request.form["mood"]

        log = LifestyleLog(sleep=sleep, exercise=exercise, mood=mood)
        db.session.add(log)
        db.session.commit()

        recommendation = generate_recommendation(sleep, exercise, mood)

    return render_template("index.html", recommendation=recommendation)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
