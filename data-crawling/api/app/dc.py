from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.auth import login_required

from app.model.user import User
from app.model.transaction import Transaction
from app.model.linkResult import LinkResult

from app import db

bp = Blueprint('dc', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('dc/index.html')

@bp.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=g.user.id).first()
    transaction = Transaction.query.filter(Transaction.user == g.user.id)
    datatransaction = formatTransaction(transaction)
    if len(datatransaction) == 0:
        profiles = singleDetailTransaction(user, datatransaction)
    else:
        profiles = singleDetailTransaction(user, datatransaction[-1])
    return render_template('dc/profile.html', profiles=profiles)

@bp.route('/help')
def help():
    return render_template('dc/help.html') 

@bp.route('/transaction', methods=('GET', 'POST'))
@login_required
def transaction():
    if request.method == 'POST':
        category = request.form.get('category')
        place = request.form.get('place')
        duration = request.form.get('duration')
        user = g.user.id
        

        error = None

        if not category:
            error = 'category is required.'

        if not place:
            error = 'place is required.'

        if error is not None:
            flash(error)
        else:
            transaction = Transaction(place=place, categori=category, user=user, month=duration)
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('dc.crawled'))

    return render_template('dc/transaction.html')


@bp.route('/crawled', methods=["GET"])
@login_required
def crawled():
    user = User.query.filter_by(id=g.user.id).first()
    transaction = Transaction.query.filter(Transaction.user == g.user.id)
    datatransaction = formatTransaction(transaction)
    profiles = singleDetailTransaction(user, datatransaction)
    return render_template('dc/crawled.html', profiles=profiles)


@bp.route('/result/<int:id>', methods=["GET"])
@login_required
def result(id):
    transaction = Transaction.query.filter(Transaction.user == g.user.id)
    idtransaction = formatResult(transaction)
    if id in idtransaction:
        x = Transaction.query.filter_by(id=id).first()

    link = LinkResult.query.filter_by(categori=x.categori, place=x.place).first()
    data = link.link
    return data

def formatResult(data):
    array = []
    for i in data:
        array.append(i.id)
    return array


def singleDetailTransaction(user, transaction):
    data = {
        'id' : user.id,
        'name' : user.name,
        'email' : user.email,
        'credit' : user.credit,
        'transaction' : transaction
    }
    return data

def singleTransaction(transaction):
    data = {
        'id': transaction.id,
        'categori': transaction.categori,
        'subs at': transaction.subs_at.strftime("%d/%m/%Y, %H:%M:%S"),
        'duration': f'{transaction.month} bulan',
        'place' : transaction.place,
    }
    return data

def formatTransaction(data):
    array = []
    for i in data:
        array.append(singleTransaction(i))
    return array

