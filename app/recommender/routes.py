from app import app
import pandas as pd
from flask import request, render_template
import pickle
import numpy as np
from app.recommender import recommender


@recommender.route('/recommend', methods=['POST', 'GET'])
def recommend():
    df = pd.read_csv('app//recommender//tag_gen.csv')
    if request.method == 'POST':
        user_courses = []
        course1 = request.form['course1']
        user_courses.append(course1)
        course2 = request.form['course2']
        user_courses.append(course2)
        course3 = request.form['course3']
        user_courses.append(course3)
        df['tags_str'] = [','.join(map(str, _)) for _ in df['Tags_fin']]
        course_tags_list = df[['Title', 'tags_str', 'Tags_fin']].copy()
        model = pickle.load(open('app//recommender//recommender_model', 'rb'))
        course_tags_vectors = model.docvecs.vectors_docs
        user_course_vector = np.zeros(shape=course_tags_vectors.shape[1])
        for course in user_courses:
            course_index = df[df["Title"] == course].index.values[0]
            user_course_vector += course_tags_vectors[course_index]
        user_course_vector /= len(user_courses)
        sims = model.docvecs.most_similar(positive=[user_course_vector], topn=30)
        nu = []
        for i, j in sims:
            print(i, j)
            course_sim = course_tags_list.loc[int(i), 'Title'].strip()
            if course_sim not in user_courses:
                nu.append(int(i))
                print(course_sim)
        return render_template('recommender.html', options=df, indices=nu)
    return render_template('recommender.html', options=df)
