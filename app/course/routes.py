from .models import Courses
from .forms import add_course_form
from app.auth.models import User
from app import app, db
from flask_login import login_required, current_user
from flask import render_template, request, url_for, redirect, flash, get_flashed_messages
from app.course import course
import pickle

@course.route('/course/<course_code>/students')
@login_required
def view_students(course_code):
    if current_user.user_role == 'Instructor':
        c = Courses.query.filter_by(course_code=course_code).first()
        students = c.students_enrolled.all()
        return render_template('view_students.html', students=students, course=c)
    return redirect(url_for('home.index'))

@course.route('/enroll_course/<course_code>')
@login_required
def enroll_course(course_code):
    if current_user.user_role == 'Student':
        c = Courses.query.filter_by(course_code=course_code).first()
        c.add_student(current_user)
        db.session.commit()
        flash('Enrolled Successfully', category='success')
        return redirect(url_for('course.view_course', course_code=course_code))
    else:
        return redirect(url_for('home.index'))

@course.route('/view_course/<course_code>')
@login_required
def view_course(course_code):
    c = Courses.query.filter_by(course_code=course_code).first()
    i = User.query.filter_by(id=c.Instructor_id).first()
    if c and i:
        return render_template('view_course.html', course=c, i=i)

@course.route('/edit_course_page/<username>/<course>', methods=['POST', 'GET'])
@login_required
def edit_course_page(username, course):
    if current_user.is_authenticated and current_user.user_role == 'Instructor':
        c = Courses.query.filter_by(course_code=course).first()
        if request.method == 'POST':
            c = Courses.query.filter_by(course_code=course).first()
            c.Course_Description = request.form['interests']
            c.resources_link = request.form['resources_link']
            db.session.commit()
            print(c.Course_Description)
            flash('Successfully Saved', category='success')
            return redirect(url_for('profile', username=current_user.username))
        return render_template('edit_course.html', course=c)
    else:
        return redirect(url_for('profile', username=current_user.username))


@course.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if (current_user.user_role == "Instructor"):
        form = add_course_form()
        if form.validate_on_submit():
            c = Courses(course_code=form.Course_Code.data, Course_name=form.Course_Name.data, Course_Description=form.Course_description.data, resources_link=form.resources_link.data, Instructor_id=current_user.id)
            db.session.add(c)
            db.session.commit()
            flash('Course Added Successfully', category='success')
            return redirect(url_for('auth.profile', username=current_user.username))
        return render_template('add_course.html', form=form)
    else:
        return redirect(url_for('auth.profile', username=current_user.username))


@course.route('/unenroll/<coursecode>')
@login_required
def remove(coursecode):
    c = Courses.query.filter_by(course_code=coursecode).first()
    if (c.is_student(current_user)):
        c.remove_student(current_user)
        db.session.commit()
        flash('Successfully Unenrolled', category='success')
        return redirect(url_for('profile', username=current_user.username))
    else:
        return redirect(url_for('profile', username=current_user.username))

@course.route('/courses')
@login_required
def courses():
    c = Courses.query.all()
    with open('app//course//AI.pickle', 'rb') as handle:
        ai_courses = pickle.load(handle)
    with open('app//course//appdev.pickle', 'rb') as handle:
        appdev_courses = pickle.load(handle)
    with open('app//course//webdev.pickle', 'rb') as handle:
        webdev_courses = pickle.load(handle)
    return render_template('courses.html', title='Courses', courses=c, ai=ai_courses, len_ai=len(ai_courses['Title']), web=webdev_courses, len_web=len(webdev_courses['Title']), app=appdev_courses, len_app=len(appdev_courses['Reviews']))
