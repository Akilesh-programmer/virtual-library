from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()

all_books = []


def update_data():
    books = Book.query.all()
    for book in books:
        id = book.id
        name = book.title
        author = book.author
        rating = book.rating

        dict = {
            "id": id,
            "title": name,
            "author": author,
            "rating": rating
        }

        all_books.append(dict)


update_data()

print(all_books)


@app.route('/')
def home():
    global all_books
    all_books = []
    update_data()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["Post", "Get"])
def add():
    global all_books
    if request.method == "POST":
        book_name = request.form.get('book_name', False)
        author_name = request.form.get('book_author', False)
        book_rating = request.form.get('rating', False)

        dict = {
            "title": str(book_name),
            "author": str(author_name),
            "rating": float(book_rating),
        }

        all_books.append(dict)

        new_book = Book(title=book_name, author=author_name,
                        rating=book_rating)
        db.session.add(new_book)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        all_books = []
        update_data()

    return render_template("add.html")


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_page(id):
    global all_books
    id = int(id)
    current_book_data = None
    for book in all_books:
        if id == book['id']:
            current_book_data = book
    print(current_book_data)

    if request.method == 'POST':
        new_rating = request.form.get("new_rating")
        new_rating = float(new_rating)

        book_to_update = Book.query.get(current_book_data['id'])
        book_to_update.rating = new_rating
        try:
            db.session.commit()
        except:
            db.session.rollback()

        all_books = []
        update_data()

    return render_template("edit.html", data=current_book_data)


@app.route('/delete/<id>',  methods=['POST', 'GET'])
def delete_page(id):
    print(id)
    global all_books

    id = int(id)

    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    try:
        db.session.commit()
    except:
        db.session.rollback()

    all_books = []
    update_data()

    return "<h1>Successfully deleted, you can close this page."


if __name__ == "__main__":
    app.run(debug=True)

# We will need to store the data of the books some where. For that we are going to learn about SQLite. The code for that learning
    # will be there in a spearate folder in this day-62 folder.
