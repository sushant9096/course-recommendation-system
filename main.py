# <==== Importing Dependencies ====>
import re

import streamlit as st
import pandas as pd

# <==== Code starts here ====>
st.set_page_config(layout="wide")

courses_list = pd.read_hdf('./models/courses.hdf5', 'courses', 'r')
import h5py

with h5py.File('./models/courses.hdf5', 'r') as f:
    dset = f['similarity']
    similarity = dset


    def recommend_courses(course_name):
        index = None
        for ind in courses_list.index:
            if re.search(course_name, courses_list['course_name'][ind], re.IGNORECASE):
                index = ind
                break

        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        course_names = []
        company_names = []
        cos_similarity = []
        course_links = []
        course_rating = []
        # print(distances)
        for i in distances[1:21]:
            course_name = courses_list.iloc[i[0]]['course_name']
            company = courses_list.iloc[i[0]]['institution']
            course_link = courses_list.iloc[i[0]]['course_link']
            course_rating.append(courses_list.iloc[i[0]]['course_rating'])
            course_names.append(course_name)
            company_names.append(company)
            course_links.append(course_link)
            cos_similarity.append(i[1])
            # recommended_course_names.append(course(course_name, course_url))

        recommended_courses = pd.DataFrame({
            "Course": course_names,
            "Institution": company_names,
            "Course Link": course_links,
            "Course Rating": course_rating,
        })
        return recommended_courses


    st.markdown(
        f"""
             <style>
             .stApp {{
                 background-image: url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");
                 background-attachment: fixed;
                 background-size: cover;
             }}
             </style>
             """,
        unsafe_allow_html=True
    )
    st.markdown("<h2 style='text-align: center; color: blue;'>Course Recommendation System</h2>",
                unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align: center; color: black;'>Find courses according to your pathway from a dataset of over 1000 courses from coursera.com!</h4>",
        unsafe_allow_html=True)

    course_list = courses_list['course_name'].values
    selected_course = st.selectbox(
        'What is your learning pathway?',
        [
            'Software Engineering',
            'Data Science',
            'Machine Learning',
            'Digital Marketing'
        ]
    )
    # selected_course = st.selectbox(
    #     "Type or select a job you like :",
    #     courses_list
    # )

    if st.button('Show Recommended Courses'):
        st.write("Recommended Courses based on your pathway are :")
        recommended_course_names = recommend_courses(selected_course)
        st.dataframe(recommended_course_names, column_config={
            "Course Link": st.column_config.LinkColumn(),
            "Course Rating": st.column_config.NumberColumn(
            help="Number of course rating on coursera",
            format="%f ⭐",
        )
        }, hide_index=True)
        # st.text(recommended_course_names[0].name)
        # st.text(recommended_course_names[1])
        # st.text(recommended_course_names[2])
        # st.text(recommended_course_names[3])
        # st.text(recommended_course_names[4])
        # st.text(recommended_course_names[5])
        # st.text(" ")
        st.markdown(
            "<h6 style='text-align: center; color: red;'>Copyright reserved by Coursera and Respective Course Owners</h6>",
            unsafe_allow_html=True)

# <==== Code ends here ====>
