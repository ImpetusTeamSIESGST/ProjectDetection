import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

st.set_page_config(layout="wide")

st.title("Project prediction app")

# Load the dataset
projects_df = pd.read_excel('ASIANPAINT.xlsx')

# Extract the candidate's skills
skills = st.text_input("Enter skills seperated by ( , )")
candidate_skills = skills
candidate_skills = candidate_skills.split(',')

# Create a TF-IDF vectorizer
tfidf = TfidfVectorizer()

# Fit the vectorizer on the technology stack column
tfidf.fit(projects_df['Required_Skills'])

# Transform the technology stack column
technology_stack_tfidf = tfidf.transform(projects_df['Required_Skills'])

# Transform the candidate's skills into a TF-IDF vector
candidate_skills_tfidf = tfidf.transform([' '.join(candidate_skills)])

# Calculate the cosine similarity between the candidate's skills and the technology stack
similarity_scores = cosine_similarity(technology_stack_tfidf, candidate_skills_tfidf)

score_list=[]
for i in range(len(similarity_scores)):
    score_list.append(similarity_scores[i][0])
    
    
sorted_list = sorted(score_list, reverse=True)
print(sorted_list)

indices = [i[0] for i in sorted(enumerate(score_list), key=lambda x:x[1], reverse=True)]




print(indices)

new_list = []
for i in range(len(sorted_list)):
    if sorted_list[i] != 0:
        if i > 0:
            new_list.append(indices[i-1])
            
        else:
            pass
        
print(new_list)



for i in range(len(new_list)):
    a=new_list[i]
    recommended_project = projects_df.loc[a, ['Project_domain', 'Project_title']]
    d=recommended_project['Project_title']
    x = d.replace(" ", "+")

# Print the recommended project
    st.write('Recommended Project:')
    st.write(f'Objective: {recommended_project["Project_domain"]}')
    st.write(f'Output: {recommended_project["Project_title"]}')
    st.markdown(f"[Link Text](https://www.google.com/search?q="+x+"+project+github)")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    
    
