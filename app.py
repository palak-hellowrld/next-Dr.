
from flask import Flask, session as flaskSession, request
import model
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    with Session(model.engine) as session:
        todaysTerm =  model.getTodaysTerm(session)
    
        clueNumber=flaskSession.get("clueNumber", 1)

        if request.method == "POST":
            userGuess=request.form.get("guess")
            if userGuess==todaysTerm.term_name:
                return (f"Awesome! Today's word was {todaysTerm.term_name}")
            else:
                if clueNumber<4:
                    clueNumber+=1
                    flaskSession["clueNumber"]=clueNumber
                    return f"Clue {clueNumber}: , {getattr(todaysTerm, f'clue{clueNumber}')}"
                else:
                    return(f"Almost! Today's word was {todaysTerm.term_name}. Better luck tomorrow!")
        
        return (f"Clue {clueNumber}: {getattr(todaysTerm, f'clue{clueNumber}')}")
            

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
