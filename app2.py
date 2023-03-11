import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Define a function to display the recommended projects
def show_project(recommended_project):
    st.write(f"**Objective:** {recommended_project['Project_domain']}")
    st.write(f"**Output:** {recommended_project['Project_title']}")
    d=recommended_project['Project_title']
    x = d.replace(" ", "+")
    st.markdown(f"[Similar Project](https://www.google.com/search?q="+x+"+project+github)")

    # st.write(f"**GitHub:** [{recommended_project['Project_title']}]({recommended_project['GitHub']})")
    st.write("-----")

# Load the project dataset
projects_df = pd.read_excel("ASIANPAINT.xlsx")

# Create a TF-IDF vectorizer and fit it to the project skills
tfidf = TfidfVectorizer()
tfidf.fit(projects_df["Required_Skills"])

# Set the app title and sidebar
st.set_page_config(page_title="Project Predictor", page_icon="🔮", layout="wide")
st.sidebar.title("Enter Your Skills")
st.sidebar.markdown("Please enter your skills separated by commas.")

# Get the user input and transform it into a TF-IDF vector
user_input = st.sidebar.text_input("", "")
user_skills_tfidf = tfidf.transform([user_input])

# Calculate the cosine similarity between the user skills and the project skills
similarity_scores = cosine_similarity(user_skills_tfidf, tfidf.transform(projects_df["Required_Skills"]))

# Sort the similarity scores and get the top 5 matching projects
top_indices = similarity_scores.argsort()[0][::-1][:20]
top_projects = projects_df.iloc[top_indices]

# Show the recommended projects
if user_input:
    st.title("Recommended Projects")
    for i, project in top_projects.iterrows():
        show_project(project)
else:
    st.title("Welcome to Project Predictor")
    st.write("Please enter your skills to get project recommendations.")
