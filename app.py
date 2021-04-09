from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
db=SQLAlchemy(app)

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    text = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.text}  - {self.author}"

@app.route('/')
def index():
    return f'Try /quotes'

@app.route('/quotes')
def get_quotes():
    quotes = Quotes.query.all()

    output = []
    for q in quotes:
        quotes_data= {'Author': q.author,'Quote:':q.text}
        output.append(quotes_data)
    return {"quotes":output}

@app.route('/quotes/<id>')
def get_quote(id):
    quote = Quotes.query.get_or_404(id)
    return {'Author':quote.author, "Quote": quote.text}

@app.route('/quotes', methods=['POST'])
def add_quote():
    q = Quotes(author=request.json['author'], text=request.json['text'])
    db.session.add(q)
    db.session.commit()
    return f"Succesfully added!"

@app.route('/quotes/<id>', methods=['DELETE'])
def delete_quote(id):
    q=Quotes.query.get(id)
    if q is None:
        return {"error":"not found"}
    db.session.delete(q)
    db.session.commit()
    return {"message": f"This quote:'{q.text}', was Deleted"}


if __name__ == "__main__":
    app.run(debug=True)