
from flask import Flask
import model

app = Flask(__name__)

@app.route("/")
def index():
    specialty_list = []
    categories = model.session.query(model.Category).all()
    for category in categories:
        specialty_list.append(category.specialty)
    categories_string = ", ".join(specialty_list)
    return categories_string

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
