from flask import Flask, render_template, request, session, redirect, url_for, flash, abort, make_response, current_app, json
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message
from datetime import datetime, timedelta, date
from os import environ
# from celery import Celery
from flask_moment import Moment
from sqlalchemy import UniqueConstraint
from config import Config
from . import main
from .. import db
from ..models import User, Permission, Entry, Role, Post, Comment,PostLike,CommentLike
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from .forms import PostForm, CommentForm
from flask import current_app, render_template
from flask_mail import Message, Mail
# from ..celery_email import send_email_to_remind
from ..email_remind import send_email_to_remind_bill
import MySQLdb 


# Home Page
@main.route("/")
def home():
    return render_template('index.html')


# Community Page
@main.route('/community', methods=['GET', 'POST'])
def community():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.community'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
                page, per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items

    return render_template('auth/community_page.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.community')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.community')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp




# User profile page
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items


    # For Chart
    if current_user.is_authenticated:
        entries = Entry.query.filter_by(user_id=current_user.id,paidUnpaid='Paid').all()
        total_entries = Entry.query.filter_by(user_id=current_user.id,paidUnpaid='Paid').count()


        accommodation_entries=[]
        gifts_entries=[]
        insurance_entries=[]
        credit_entries=[]
        electricity_entries=[]
        tv_entries=[]
        education_entries=[]
        car_entries=[]
        twowheeler_entries=[]
        food_entries=[]
        pet_entries=[]
        sports_entries=[]
        shopping_entries=[]
        tax_entries=[]
        vacation_entries=[]
        investment_entries=[]
        savings_entries=[]
        child_entries=[]
        other_entries=[]
        medicare_entries=[]
        for entry in entries:
            if entry.billCategory=='Accomodation':
                accommodation_entries.append(entry.amount)
            if entry.billCategory=='Gifts':
                gifts_entries.append(entry.amount)
            if entry.billCategory=='Insurance':
                insurance_entries.append(entry.amount)
            if entry.billCategory=="Credit Cards":
                credit_entries.append(entry.amount)
            if entry.billCategory=='Electricity':
                electricity_entries.append(entry.amount)
            if entry.billCategory=='TV':
                tv_entries.append(entry.amount)
            if entry.billCategory=='Education':
                education_entries.append(entry.amount)
            if entry.billCategory=='Car':
                car_entries.append(entry.amount)
            if entry.billCategory=='Two wheeler':
                twowheeler_entries.append(entry.amount)
            if entry.billCategory=='Food':
                food_entries.append(entry.amount)
            if entry.billCategory=='Medicare':
                medicare_entries.append(entry.amount)
            if entry.billCategory=='Pets':
                pet_entries.append(entry.amount)
            if entry.billCategory=='Sports':
                sports_entries.append(entry.amount)
            if entry.billCategory=='Shopping':
                shopping_entries.append(entry.amount)
            if entry.billCategory=='Tax':
                tax_entries.append(entry.amount)
            if entry.billCategory=='Vacation':
                vacation_entries.append(entry.amount)
            if entry.billCategory=='Investment':
                investment_entries.append(entry.amount)
            if entry.billCategory=='Savings':
                savings_entries.append(entry.amount)
            if entry.billCategory=='Child Care':
                child_entries.append(entry.amount)
            if entry.billCategory=='Other':
                other_entries.append(entry.amount)    




        accommodation_sum=sum(accommodation_entries)
        gifts_sum=sum(gifts_entries)
        insurance_sum=sum(insurance_entries)
        credit_sum=sum(credit_entries)
        electricity_sum=sum(electricity_entries)
        tv_sum=sum(tv_entries)
        education_sum=sum(education_entries)
        car_sum=sum(car_entries)
        twowheeler_sum=sum(twowheeler_entries)
        food_sum=sum(food_entries)
        pet_sum=sum(pet_entries)
        sports_sum=sum(sports_entries)
        shopping_sum=sum(shopping_entries)
        tax_sum=sum(tax_entries)
        vacation_sum=sum(vacation_entries)
        investment_sum=sum(investment_entries)
        savings_sum=sum(savings_entries)
        child_sum=sum(child_entries)
        other_sum=sum(other_entries)
        medicare_sum=sum(medicare_entries)


        return render_template('auth/user.html', user=user, posts=posts,pagination=pagination,accommodation_sum=accommodation_sum,
        gifts_sum=gifts_sum,insurance_sum=insurance_sum,credit_sum=credit_sum,electricity_sum=electricity_sum,
        tv_sum=tv_sum, education_sum=education_sum,car_sum=car_sum,twowheeler_sum=twowheeler_sum,
        food_sum=food_sum,pet_sum=pet_sum,sports_sum=sports_sum,shopping_sum=shopping_sum,tax_sum=tax_sum,
        vacation_sum=vacation_sum,investment_sum=investment_sum,savings_sum=savings_sum,child_sum=child_sum,
        other_sum=other_sum,medicare_sum=medicare_sum,entries=entries,total_entries=total_entries)


    return render_template('auth/user.html')


# Post page
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    post_upvote=PostLike.query.filter_by(post_id=id).count()
    # comments=Comment.query.filter_by(post_id=id).all()
    # for i in comments:
    #     comment_id=i.id
    #     comment_upvote=CommentLike.query.filter_by(comment_id=comment_id).count()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)

    comments = pagination.items
    
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination,post_upvote=post_upvote,
                           )



# Edit Post page
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.submit.data:
                post.body = form.body.data
                db.session.add(post)
                db.session.commit()
                flash('The post has been updated.')
                return redirect(url_for('.post', id=post.id))
        elif form.delete.data:
                Post.query.filter_by(id=post.id).delete()
                db.session.commit()
                flash('The post has been Deleted.')
                return redirect(url_for('main.community'))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)





# @main.route('/total-upvote-post/<int:post_id>')
# @login_required
# def total_post_upvotes(post_id):
#     total_post_upvotes = PostLike.query.filter_by(id=post_id).count()
#     render_template('auth/community_page.html', total_post_upvotes= total_post_upvotes)


@main.route('/like-post/<int:post_id>/<action>')
@login_required
def like_post_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)



@main.route('/like-comment/<int:comment_id>/<action>')
@login_required
def like_comment_action(comment_id, action):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if action == 'like':
        current_user.like_comment(comment)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_comment(comment)
        db.session.commit()
    return redirect(request.referrer)




@main.route('/translate', methods=['POST'])
def translate():
   # parse args
   text = request.form.get('text')
   target = request.form.get('target')
 
   # url encode text
   long_list_of_words = text.split(' ')
   url_encoded_text = f"q={'%20'.join(long_list_of_words)}&target={target}"
   payload = url_encoded_text
 
   r = request.post(current_app.config['TRANSLATE_BASE_URL'], data=payload,
        headers=current_app.config['HEADERS'])
  
   return r.json()

# Edit Comment page
@main.route('/edit-comment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user != comment.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        if form.submit.data:
                comment.body = form.body.data
                db.session.add(comment)
                db.session.commit()
                flash('The Answer has been updated.')
                return redirect(url_for('.post', id=comment.post_id))
        elif form.delete.data:
                Comment.query.filter_by(id=comment.id).delete()
                db.session.commit()
                flash('The Answer has been Deleted.')
                return redirect(url_for('.post', id=comment.post_id))
    
    form.body.data = comment.body
    return render_template('edit_comment.html', form=form)



# Will make Admin Dashboard
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"



# For Comment Moderation
@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',page=request.args.get('page', 1, type=int)))


# Bill Remnder Add Page
@main.route("/add", methods=['GET', 'POST'])
def add():
    if(request.method == "GET"):
        return render_template('add.html')

    elif(request.method == "POST"):
        # username = current_user.username
        user_id = current_user.id
        billName = request.form.get('bill_name')
        billCategory = request.form.get('bill_category')
        notificationReminder = int(request.form.get('notification_reminder'))
        amount = request.form.get('amount')
        dueDate = request.form.get('due_date')
        answer = request.form.get('answer')
        repeatDays = request.form.get('repeat_days')
        repeatTime = request.form.get('repeat_time')
        note = request.form.get('note')
        date_of_add = datetime.now()
        paidUnpaid = 'Unpaid'

        session['bill_name'] = billName
        session['bill_category'] = billCategory
        session['amount'] = amount
        session['due_date'] = dueDate
        session['notification_reminder'] = notificationReminder
        session['note'] = note
        session['date_of_add'] = date_of_add

        entries = Entry(user_id=user_id, billName=billName, billCategory=billCategory, amount=amount, dueDate=dueDate,
                        notificationReminder=notificationReminder, answer=answer, repeatDays=repeatDays, repeatTime=repeatTime,
                        note=note, dateOfAdd=date_of_add, paidUnpaid=paidUnpaid)
        if request.form.get('submit') == 'Send':
            db.session.add(entries)
            db.session.commit()
        elif request.form.get('submit') == 'Discard':
            pass

        print(repeatTime)
        print(repeatDays)
        # if repeatTime=='day':
        #     app.conf.beat_schedule = {
        #     'add-repeat-emails':{'task':'tasks.repeatEmail',
        #     'schedule': crontab(hour=0,minute=0,day='*',month='*'),
        #    }}
        # if repeatTime=='week':
        #     app.conf.beat_schedule = {
        #     'add-repeat-emails':{'task':'tasks.repeatEmail',
        #     'schedule': crontab(hour=0,minute=0,day='*',month='*'),
        #    }}
        # if repeatTime=='month':
        #     app.conf.beat_schedule = {
        #     'add-repeat-emails':{'task':'tasks.repeatEmail',
        #     'schedule': crontab(hour=0,minute=0,day=1,month='*'),
        #    }}
        # if repeatTime=='week':
        #     app.conf.beat_schedule = {
        #     'add-repeat-emails':{'task':'tasks.repeatEmail',
        #     'schedule': crontab(hour=8760*repeatDays),
        #    }}

        how_many_days_before_notification = timedelta(
            days=notificationReminder, hours=13, minutes=50)
        date_of_reminder = datetime.strptime(
            dueDate, '%Y-%m-%d') - how_many_days_before_notification
        print(date_of_reminder)
        waiting_time = (date_of_reminder-date_of_add).total_seconds()
        print(waiting_time)

        if request.form.get('submit') == 'Send':
            # send_email_to_remind.apply_async(countdown=2,args=[current_user.email,
            # 'Reminding Your Bill','auth/email/change_email'])

            # send_email_to_remind(current_user.email,'Reminding Your Bill','auth/email/emailToRemind',user=current_user)
            send_email_to_remind_bill(current_user.email,'Reminding Your Bill','auth/email/emailToRemind',user=current_user)



            flash('An email will be sent to you at {} to remind your {} bill of {} Rupees'.format(date_of_reminder,
                                                                                                  billName, amount))
            return redirect(url_for('main.home'))

        elif request.form.get('submit') == 'Discard':
            flash('Changes Not Saved')
            return redirect(url_for('main.home'))
        else:
            pass
    return render_template('add.html')

# Show Reminders Page
@main.route("/show_reminders", methods=['GET', 'POST'])
def show_reminders():
    if current_user.is_authenticated:
        entry=Entry.query.filter_by(user_id=current_user.id).all()
        total_unpaid=Entry.query.filter_by(user_id=current_user.id,paidUnpaid='Unpaid').count()
        total_paid=Entry.query.filter_by(user_id=current_user.id,paidUnpaid='Paid').count()
    
        return render_template('show_reminders.html',entry=entry,total_unpaid=total_unpaid,total_paid=total_paid)
    return render_template('show_reminders.html')


# Chart Page
@main.route("/chart", methods=['GET', 'POST'])
def chart():
    entries = Entry.query.filter_by(user_id=current_user.id,paidUnpaid='Paid').all()


    accommodation_entries=[]
    gifts_entries=[]
    insurance_entries=[]
    credit_entries=[]
    electricity_entries=[]
    tv_entries=[]
    education_entries=[]
    car_entries=[]
    twowheeler_entries=[]
    food_entries=[]
    pet_entries=[]
    sports_entries=[]
    shopping_entries=[]
    tax_entries=[]
    vacation_entries=[]
    investment_entries=[]
    savings_entries=[]
    child_entries=[]
    other_entries=[]
    medicare_entries=[]
    for entry in entries:
        if entry.billCategory=='Accomodation':
            accommodation_entries.append(entry.amount)
        if entry.billCategory=='Gifts':
            gifts_entries.append(entry.amount)
        if entry.billCategory=='Insurance':
            insurance_entries.append(entry.amount)
        if entry.billCategory=="Credit Cards":
            credit_entries.append(entry.amount)
        if entry.billCategory=='Electricity':
            electricity_entries.append(entry.amount)
        if entry.billCategory=='TV':
            tv_entries.append(entry.amount)
        if entry.billCategory=='Education':
            education_entries.append(entry.amount)
        if entry.billCategory=='Car':
            car_entries.append(entry.amount)
        if entry.billCategory=='Two wheeler':
            twowheeler_entries.append(entry.amount)
        if entry.billCategory=='Food':
            food_entries.append(entry.amount)
        if entry.billCategory=='Medicare':
            medicare_entries.append(entry.amount)
        if entry.billCategory=='Pets':
            pet_entries.append(entry.amount)
        if entry.billCategory=='Sports':
            sports_entries.append(entry.amount)
        if entry.billCategory=='Shopping':
            shopping_entries.append(entry.amount)
        if entry.billCategory=='Tax':
            tax_entries.append(entry.amount)
        if entry.billCategory=='Vacation':
            vacation_entries.append(entry.amount)
        if entry.billCategory=='Investment':
            investment_entries.append(entry.amount)
        if entry.billCategory=='Savings':
            savings_entries.append(entry.amount)
        if entry.billCategory=='Child Care':
            child_entries.append(entry.amount)
        if entry.billCategory=='Other':
            other_entries.append(entry.amount)    




    accommodation_sum=sum(accommodation_entries)
    gifts_sum=sum(gifts_entries)
    insurance_sum=sum(insurance_entries)
    credit_sum=sum(credit_entries)
    electricity_sum=sum(electricity_entries)
    tv_sum=sum(tv_entries)
    education_sum=sum(education_entries)
    car_sum=sum(car_entries)
    twowheeler_sum=sum(twowheeler_entries)
    food_sum=sum(food_entries)
    pet_sum=sum(pet_entries)
    sports_sum=sum(sports_entries)
    shopping_sum=sum(shopping_entries)
    tax_sum=sum(tax_entries)
    vacation_sum=sum(vacation_entries)
    investment_sum=sum(investment_entries)
    savings_sum=sum(savings_entries)
    child_sum=sum(child_entries)
    other_sum=sum(other_entries)
    medicare_sum=sum(medicare_entries)

    return render_template('chart.html',accommodation_sum=accommodation_sum,
    gifts_sum=gifts_sum,insurance_sum=insurance_sum,credit_sum=credit_sum,electricity_sum=electricity_sum,
    tv_sum=tv_sum, education_sum=education_sum,car_sum=car_sum,twowheeler_sum=twowheeler_sum,
    food_sum=food_sum,pet_sum=pet_sum,sports_sum=sports_sum,shopping_sum=shopping_sum,tax_sum=tax_sum,
    vacation_sum=vacation_sum,investment_sum=investment_sum,savings_sum=savings_sum,child_sum=child_sum,
    other_sum=other_sum,medicare_sum=medicare_sum)


# # Money Manager Page
# @main.route("/money_manager", methods=['GET', 'POST'])
# def money_manager():
#     # money=MoneyManager.query.filter_by(user_id=current_user.id)
#     # income=money.income
#     # expense=money.expense
#     return render_template('money_manager.html')

# # Money Manager Page
# @main.route("/calculate", methods=['GET', 'POST'])
# def calculate():
#     return render_template('calculator.html')




# Errr Handler Page
@main.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html'), 404)
    return resp
@main.errorhandler(500)
def not_found(error):
    resp = make_response(render_template('500.html'), 500)
    return resp
@main.errorhandler(403)
def not_found(error):
    resp = make_response(render_template('403.html'), 403)
    return resp



# Cookie
@main.route('/cookie')
def cookie():
    res = make_response("<h1>cookie is set</h1>")
    res.set_cookie('name', 'content')
    return res


# To Follow
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))

# To UnFollow
@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.home'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.home'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

# Terms and conditions Page
@main.route("/terms")
def terms():
    return render_template('terms.html')

# Frequently asked questions Page
@main.route("/faq")
def faq():
    return render_template('faq.html')

# HelpGuide Page
@main.route("/guide")
def guide():
    return render_template('guide.html')
