import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import plotly.express as px
import base64

# Define a function to display the recommended projects
def show_project(recommended_project):
    st.write(f"**Objective:** {recommended_project['Project_domain']}")
    st.write(f"**Output:** {recommended_project['Project_title']}")
    st.write(f"**Type:** {recommended_project['Project_type']}")
    c=recommended_project['Project_domain']
    y= c.replace(" ", "+")
    d=recommended_project['Project_title']
    x = d.replace(" ", "+")
    st.markdown(f"[Show Project samples](https://www.google.com/search?q="+x+"+project+using+"+y+"+github)")

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
top_indices = similarity_scores.argsort()[0][::-1][:25]
top_projects = projects_df.iloc[top_indices]





# Show the recommended projects
if user_input:
    st.title("Recommended Projects")
    for i, project in top_projects.iterrows():
        show_project(project)
    recommended_projects_df = pd.DataFrame({
        "Objective": top_projects["Project_domain"],
        "Output": top_projects["Project_title"],
        "Type": top_projects["Project_type"]
    })
    
    # Add a button to download the recommended projects as a CSV file
    csv = recommended_projects_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="recommended_projects.csv">Download CSV File</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
else:
    st.title("Welcome to Project Predictor")
    st.write("Please enter your skills to get project recommendations.")
    

# Count of skills in dataset
count_df = pd.DataFrame({
    'skills': tfidf.get_feature_names_out(),
    'count': tfidf.transform(projects_df["Required_Skills"]).sum(axis=0).A1
})
count_df = count_df.sort_values('count', ascending=False)

# Show the skill count graph
st.title("Skills Count in Dataset")
fig = px.bar(count_df[:20], x='skills', y='count')
st.plotly_chart(fig)
