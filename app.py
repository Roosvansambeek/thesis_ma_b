from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from database import load_courses_from_db, load_carousel_courses_from_db, load_favorite_courses_from_db, add_interests_to_db , add_login_to_db, check_credentials, update_interests, add_views_to_db, add_test_to_db, load_best_courses_with_favorite_from_db
from flask import request, redirect, url_for, flash
from datetime import datetime


#TFIDF
#fav
from TFIDF_algorithmfav import get_recommendations_fav_TFIDF,get_recommendations_fav_with_ratings_TFIDF

#int
from TFIDF_algorithminterests import get_course_recommendations_int_TFIDF, get_recommendations_interests_with_ratings_TFIDF


#BOW
#fave
from BOW_algorithmfav import get_recommendations_fav_BOW, get_recommendations_with_ratings_BOW

#int
from BOW_algorithminterests import get_course_recommendations_int_BOW, get_recommendations_with_ratings_BOW




app = Flask(__name__)


filters = {
    'Degree': ['Bachelor', 'Master', 'Pre-master'],
    'Block': [1, 2, 3, 4]
}


@app.route("/")
def landing():
    return render_template('signin.html')

app.secret_key = 'session_key'

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        student_number = request.form['student_number']
        session['student_number'] = student_number
        password = request.form['password']
        session['password'] = password
        level = request.form['level']
        education = request.form['education']

        add_login_to_db(student_number, password, level, education)

        return redirect('/state_interests.html')

    return render_template('signin.html')

@app.route("/state_interests.html")
def state_interests():
    return render_template('state_interests.html')

@app.route("/state_interests/stated.html", methods=['POST'])
def stated_interests():
    data = request.form
    student_number = session.get('student_number')  
    print(student_number)
    password = session.get('password') 
    print(password)
  
    if student_number and password:
        update_interests(student_number, password, data)

    previous_page = request.referrer
    return redirect(f'/home/{student_number}')



@app.route("/home/<student_number>", methods=['GET', 'POST'])
def home(student_number):
    # Access the student_number from the URL and the session
    student_number = student_number or session.get('student_number', default_value)
    print('student_number:', student_number)
    # Rest of your code
    carousel_courses = load_carousel_courses_from_db(student_number)
    num_carousel_courses = len(carousel_courses)
    fav_recommendations = get_recommendations_fav_with_ratings_TFIDF(student_number)
    interests_recommendations = get_recommendations_interests_with_ratings_TFIDF(student_number)

    data = request.form  # Moved the data assignment here

    if request.method == 'POST':
        rating = request.form.get('rating')
        course_code = request.form.get('course_code')

        if rating == 'on':
            # Update the database with 'off' status
            # Implement the code to update the database with 'off'
            add_test_to_db(request, student_number, course_code, 'on')
        else:
            # Update the database with 'on' status
            # Implement the code to update the database with 'on'
            add_test_to_db(request, student_number, course_code, 'off')

        # Update the checkboxes here after the change

        fav_recommendations = get_recommendations_fav_with_ratings_TFIDF(student_number)

        interests_recommendations = get_recommendations_interests_with_ratings_TFIDF(student_number)



    return render_template('home.html', student_number=student_number, carousel_courses=carousel_courses, num_carousel_courses=num_carousel_courses, fav_recommendations=fav_recommendations, interests_recommendations=interests_recommendations)



  
@app.route('/favourites/<student_number>')
def favorite_courses(student_number):
    # The student_number parameter should be included in the function signature
    favorite_courses = load_favorite_courses_from_db(student_number)
    return render_template('favourites.html', favorite_courses=favorite_courses, student_number=student_number)

      
@app.route("/courses/<student_number>")
def hello_world(student_number):
    courses = load_courses_from_db()
    return render_template('courses.html', courses=courses, filters=filters, student_number=student_number)


@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/api/courses")
def list_courses():
  courses = load_courses_from_db()
  return jsonify(courses)


@app.route("/course/<course_code>/<student_number>")
def show_course(student_number, course_code):
    # Load the course data
    courses = load_courses_from_db()
    course = [course for course in courses if course.get('course_code') == course_code]

    if not course:
        return "Not Found", 404

    print(student_number)
    print(course_code)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_views_to_db(student_number, course_code, timestamp, id)

    return render_template('coursepage.html', course=course[0])



if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)