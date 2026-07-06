
from flask import Flask, session as flaskSession, request, render_template
import model
from sqlalchemy.orm import Session
from datetime import date as dt_date
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET","POST"])
def index():
    with Session(model.engine) as session:
        today = dt_date.today()
        storedDate = flaskSession.get("clueDate")
        todaysTerm =  model.getTodaysTerm(session)
        allTerms= session.query(model.Term).all()

        if storedDate != str(today):
            clueNumber = 1
            flaskSession["clueNumber"] = 1
            flaskSession["clueDate"] = str(today)
        else:
            clueNumber = flaskSession.get("clueNumber", 1)

        cluesToShow = [getattr(todaysTerm, f"clue{n}") for n in range(1, clueNumber + 1)]

        if request.method == "POST":
            userGuess=request.form.get("guess")
            if userGuess==todaysTerm.term_name:
                return (f"Awesome! Today's word was {todaysTerm.term_name}")
            else:
                if clueNumber<4:
                    clueNumber+=1
                    flaskSession["clueNumber"]=clueNumber
                    cluesToShow = [getattr(todaysTerm, f"clue{n}") for n in range(1, clueNumber + 1)]
                    return render_template("index.html", allTerms= allTerms, clues=cluesToShow, clue_number= clueNumber)
                else:
                    return(f"Almost! Today's word was {todaysTerm.term_name}. Better luck tomorrow!")
        
        return render_template("index.html", allTerms= allTerms, clues=cluesToShow, clue_number=clueNumber, )
    


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
