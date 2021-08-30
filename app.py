from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import datetime
import os

# engine int for once deployed
# engine = create_engine('sqlite:///' +os.path.join, 'db.sqlite')
# connection = engine.connect()

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db
db = SQLAlchemy(app)
# migrate
migrate = Migrate(app, db)
# init ma
ma = Marshmallow(app)
# metadata
metadata = MetaData()

@app.route('/')
def get():
    return jsonify({'howdy':'hello'})


# Product Class/Model
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text(100))
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    edition = db.Column(db.Text(100))
    body = db.Column(db.Text(100000))
    date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, author, title, description, edition, body):
        self.author = author
        self.title = title
        self.description = description
        self.edition = edition
        self.body = body
    def __repr__(self):
        return f"<Articles {self.name}>"

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'title','description', 'edition', 'body', 'date')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

# create article
@app.route('/add', methods=['POST'])
def add_article():
    author = request.json['author']
    title = request.json['title']
    description = request.json['description']
    edition = request.json['edition']
    body = request.json['body']

    articles = Articles(author, title, description, edition, body)

    db.session.add(articles)
    db.session.commit()

    return article_schema.jsonify(articles)

# get all articles
@app.route("/articles", methods = ['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

# get specific articles
@app.route("/articles/<id>/", methods = ['GET'])
def get_specific_article(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

# update specific article
@app.route("/update/<id>/", methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    author = request.json['author']
    title = request.json['title']
    description = request.json['description']
    edition = request.json['edition']
    body = request.json['body']

    article.author = author
    article.title = title
    article.description = description
    article.edition = edition
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)

# delete specific artile
@app.route("/delete/<id>/", methods = ['DELETE'])
def article_delete(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
