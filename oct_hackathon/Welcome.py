import streamlit as st

# Set the page title and icon
st.set_page_config(page_title="Acorn Landing Page", page_icon="📝", layout="wide")

# Main landing page
st.title("Welcome to Acorn 📝")
st.markdown("""
### AI-Powered Cover Lesson Planner

Acorn helps cover teachers plan engaging and effective lessons with minimal effort. Using AI, we generate personalized lesson plans that can be easily delivered by teachers, even if they're unfamiliar with the subject.

### How It Works:
1. **Select a subject and key stage**: We have lesson plans for various subjects and key stages.
2. **Generate your lesson plan**: Based on your inputs, Acorn will create a lesson plan with learning points, keywords, activities, and videos.
3. **Engage students with interactive tasks**: Acorn ensures the lesson is engaging and meets the learning goals.

Click the button below to start generating your lesson plan.
""")

# Button to navigate to the lesson planner
if st.button("Get Started"):
    st.experimental_set_query_params(page="Lesson_Planner")  # Redirect to the lesson planner page
    st.write("Loading the Lesson Planner...")

# Footer
st.markdown("---")
st.write("Powered by Acorn © 2024")
