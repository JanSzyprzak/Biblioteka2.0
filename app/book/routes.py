from flask import render_template, request, url_for, redirect
from flask import render_template
from sqlalchemy import update
from app.book import bp
from app.models.book import Book
from app.models.author import Author
from app.main.forms import BookForm
from app.extensions import db


@bp.route('<int:book_id>/', methods=["GET", "POST"])
def book_details(book_id):
    authors = Author.query.all()

    book_to_update = Book.query.get(book_id)
    form = BookForm()
    if request.method == 'POST':
        title=request.form['title']     
        author=request.form['author'] 
        description=request.form['description']
        number_of_pages=request.form['number_of_pages']
        read=form.read.data
        borrowed=form.borrowed.data

        book_to_update.title = title
        book_to_update.description = description
        book_to_update.number_of_pages = number_of_pages
        book_to_update.read = read
        book_to_update.borrowed = borrowed

        for author in authors:
            if author.name == request.form['author']:
                author_object = author    
            else:
                author_object = Author(name=request.form['author']) 
        
        db.session.add(book_to_update)
        book_to_update.authors.append(author_object)
        db.session.commit()



        return redirect(url_for('main.index'))



    return render_template('book/book.html', form=form, book_id=book_id)




