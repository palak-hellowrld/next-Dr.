"""
app.py

Flask routes for the Next Dr.? game.

Routes:
- "/" (GET, POST): main game route.
    - Tracks daily clue progress via flaskSession (clueNumber, clueDate),
      resetting clueNumber to 1 each new day.
    - On POST, checks the user's guess against today's term:
        - correct: result = "correct"
        - wrong, tries remaining: reveals next clue, no message shown
          (intentional -- no feedback on tries 1-3)
        - wrong, out of tries (4th guess): result = "wrong", modal shown
    - Also tracks visitors: reads/sets a "visitor_id" cookie (UUID),
      creates or updates a row in the Visitor table each request.
      Uses make_response() instead of a plain render_template() return
      specifically so .set_cookie() can be called before the response
      is sent.
"""



from flask import Flask, session as flaskSession, request, render_template, make_response
import model
from sqlalchemy.orm import Session
from datetime import date as dt_date, datetime
import os
import uuid

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET","POST"])
def index():
    with Session(model.engine) as session:
        visitorId = request.cookies.get("visitor_id")
        newCookie = False

        if not visitorId:
            visitorId = str(uuid.uuid4())
            newCookie = True

        visitor = session.query(model.Visitor).filter_by(id=visitorId).first()

        if request.method == "GET":
            if not visitor:
                visitor = model.Visitor(id=visitorId, visitCount=1)
                session.add(visitor)
            else:
                visitor.visitCount += 1
                visitor.last_seen = datetime.now()

            session.commit()

        today = dt_date.today()
        storedDate = flaskSession.get("clueDate")
        todaysTerm =  model.getTodaysTerm(session)
        allTerms= session.query(model.Term).all()
        gameOver= flaskSession.get("gameOver", False)

        if storedDate != str(today):
            clueNumber = 1
            flaskSession["clueNumber"] = 1
            flaskSession["clueDate"] = str(today)
            gameOver = False
            flaskSession["gameOver"] = False
        else:
            clueNumber = flaskSession.get("clueNumber", 1)

        cluesToShow = [getattr(todaysTerm, f"clue{n}") for n in range(1, clueNumber + 1)]
        result=None

        if gameOver == False:
            if request.method == "POST":
                userGuess=request.form.get("guess")
                if userGuess==todaysTerm.term_name:
                    result="correct"
                    gameOver=True
                    flaskSession["gameOver"]=True
                    flaskSession["result"]="correct"
                else:
                    if clueNumber<4:
                        clueNumber+=1
                        flaskSession["clueNumber"]=clueNumber
                        cluesToShow = [getattr(todaysTerm, f"clue{n}") for n in range(1, clueNumber + 1)]
                    else:
                        result="wrong"
                        gameOver=True
                        flaskSession["gameOver"]=True
                        flaskSession["result"]="wrong"
        else:
            result = flaskSession.get("result", None)
        
        response = make_response(render_template(
            "index.html",
            allTerms=allTerms,
            clues=cluesToShow,
            clueNumber=clueNumber,
            result=result,
            correctAnswer=todaysTerm.term_name if result in ("correct", "wrong") else None
        ))

        if newCookie:
            response.set_cookie("visitor_id", visitorId, max_age=60*60*24*365*2)

        return response
    


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
