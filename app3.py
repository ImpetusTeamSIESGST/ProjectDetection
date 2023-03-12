import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Set up the navbar
st.set_page_config(page_title='Project prediction app', layout='wide')
nav = st.sidebar.radio("Navigation", ['Home', 'About'])

# Display the appropriate page based on the user's selection
if nav == 'Home':
    # Load the dataset
    projects_df = pd.read_excel('ASIANPAINT.xlsx')

    # Extract the candidate's skills
    skills = st.text_input("Enter your skills (separated by commas)")

    if st.button('Submit'):
        # Split the candidate's skills and create a TF-IDF vector
        candidate_skills = skills.split(',')
        tfidf = TfidfVectorizer()
        tfidf.fit(projects_df['Required_Skills'])
        candidate_skills_tfidf = tfidf.transform([' '.join(candidate_skills)])

        # Calculate the cosine similarity between the candidate's skills and the technology stack
        technology_stack_tfidf = tfidf.transform(projects_df['Required_Skills'])
        similarity_scores = cosine_similarity(technology_stack_tfidf, candidate_skills_tfidf)
        score_list = [similarity_scores[i][0] for i in range(len(similarity_scores))]

        # Sort the projects by similarity score and display the top matches
        sorted_indices = sorted(range(len(score_list)), key=lambda i: score_list[i], reverse=True)
        st.write('Recommended projects:')
        for i in sorted_indices:
            if score_list[i] > 0:
                project_title = projects_df.iloc[i]['Project_title']
                project_domain = projects_df.iloc[i]['Project_domain']
                project_link = f'https://www.google.com/search?q={project_title.replace(" ", "+")}+project+github'
                st.write(f'Objective: {project_domain}\nOutput: {project_title}')
                st.markdown(f'[View project]({project_link})')
                st.write('---')

elif nav == 'About':
    st.write('This app recommends projects based on the skills you enter. It uses a dataset of real-world projects and a machine learning algorithm to find the best matches.')
