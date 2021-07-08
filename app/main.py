from flask import Blueprint, render_template, session, request, flash, redirect, abort
from hashids import Hashids
from .models import Url, User
from . import db
from datetime import datetime

main = Blueprint('main', __name__, static_folder='static', template_folder='templates')
hashids = Hashids(min_length="3", salt="hfkwrhrgscmznmzxfasdqpoasnhytask")

@main.route("/", methods=['GET', 'POST'])
def index() :
    if request.method=='POST' :
        original_url = request.form.get('original_url')
        slug = request.form.get('slug')
        slug_wrong = False
        for i in slug :
            if not(i.isalnum() or i=='-') :
                slug_wrong=True
                break
        if slug_wrong :
            flash("Wrong custom back-half. Only upper-case and lower-case letters, numbers and dashes(-) are allowed.", "danger")
            return redirect("/")
        slug_dup = Url.query.filter_by(slug=slug).first()
        if slug_dup is not None :
            message = "Short URL is not available. "+ request.host_url+slug+" already taken."
            flash(message, "danger")
            return redirect("/")
        if 'user' in session :
            user = User.query.filter_by(id=session['user']).first()
            entry = Url(original_url=original_url, created=datetime.now(), user=user)
        else :
            entry = Url(original_url=original_url, created=datetime.now())
        db.session.add(entry)
        db.session.commit()
        if slug=="" :
            hash_id = hashids.encode(entry.id)
            entry.slug = hash_id
        else :
            entry.slug = slug
        short_url = request.host_url+entry.slug
        db.session.commit()
        return render_template("main/index.html", short_url=short_url)
    return render_template("main/index.html")

@main.route("/about", methods=['GET'])
def about() :
    return render_template("main/about.html")

@main.route("/<string:slug>", methods=['GET'])
def view_url(slug) :
    url=Url.query.filter_by(slug=slug).first()
    if url is None :
        abort(404)
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@main.route("/statistics")
def statistics() :
    if 'user' in session :
        user = User.query.filter_by(id=session['user']).first()
        urls = Url.query.filter_by(user=user).all()
        return render_template("main/statistics.html", urls=urls)
    flash("Please login to continue", "warning")
    return redirect("/login")

@main.route("/edit/<string:slug>", methods=['GET', 'POST'])
def edit(slug) :
    if 'user' in session :
        url = Url.query.filter_by(slug=slug).first()
        if url is None :
            abort(404)
        if request.method=='POST' :
            original_url=request.form.get('original_url')
            url.original_url=original_url
            url.clicks=0
            url.created=datetime.now()
            db.session.commit()
            return redirect("/statistics")
        return render_template("main/edit.html", url=url)
    flash("Please Login to continue", "warning")
    return redirect("/login")

@main.route("/delete/<string:slug>", methods=['POST'])
def delete(slug) :
    if 'user' in session :
        url = Url.query.filter_by(slug=slug).first()
        if url is None :
            abort(404)
        db.session.delete(url)
        db.session.commit()
        return redirect("/statistics")
    flash("Please login to continue", "warning")
    return redirect("/login")
