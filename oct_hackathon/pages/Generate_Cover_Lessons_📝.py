import requests
import streamlit as st
from dotenv import load_dotenv
import os
import openai
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OAK_API_KEY")
# print(api_key)

st.set_page_config(
    page_title="Acorn", page_icon="📝"
)
st.title("Acorn 📝")
subject_to_subject_dict = {
    "English": "english",
    "Geography": "geography",
    "History": "history",
    "Maths": "maths",
    "Science": "science",
    "Music": "music",
    "Biology": "biology",
    "Chemistry": "chemistry",
    "Combined Science": "combined-science",
    "Physics": "physics"
}

subject = st.selectbox("Select a subject", ["english", "geography", "history", "maths", "science", "music", "biology", "chemistry", "combined-science", "physics"])
keyStage = st.selectbox("Select a key stage", ['ks1', 'ks2', 'ks3', 'ks4'])

# Set the URL and headers
url = f'https://open-api.thenational.academy/api/v0/key-stages/{keyStage}/subject/{subject}/lessons?offset=0&limit=100'
headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

try:
    response = requests.get(url, headers=headers)
    # response.raise_for_status()
    data = response.json()
    # Extract lesson titles and slugs from nested structure
    lesson_map = {}
    for unit in data:  # Loop over the outer unit list
        for lesson in unit['lessons']:  # Loop over each lesson in the 'lessons' list
            lesson_map[lesson['lessonTitle']] = lesson['lessonSlug']  # Map lessonTitle to lessonSlug
    # Display the lessons in the selectbox (human-readable titles)
    # Display lessons in selectbox
    if lesson_map:
        selected_lesson_title = st.selectbox("Select a lesson", list(lesson_map.keys()))
        selected_lesson_slug = lesson_map[selected_lesson_title]  # Retrieve the slug


        # Set the URL and headers
        url_2 = f'https://open-api.thenational.academy/api/v0/lessons/{selected_lesson_slug}/summary'
        headers_2 = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        try:
            response_2 = requests.get(url_2, headers=headers_2)
            data_2 = response_2.json()

            st.markdown('## Key Learning Points:')
            key_learning_points = {}
            selected_learning_points = []  # To store the selected key learning points
            for i, learning_point in enumerate(data_2['keyLearningPoints']):
                is_selected = st.checkbox(learning_point['keyLearningPoint'], value=True)
                key_learning_points[i] = is_selected
                if is_selected:
                    selected_learning_points.append(learning_point['keyLearningPoint'])

            st.markdown('## Keywords:')
            selected_keywords = {}
            selected_keyword_list = []  # To store the selected keywords with descriptions
            for i, keyword_data in enumerate(data_2['lessonKeywords']):
                is_selected = st.checkbox(f"**Keyword**: {keyword_data['keyword']}\n**Description**: {keyword_data['description']}", value=True)
                selected_keywords[i] = is_selected
                if is_selected:
                    selected_keyword_list.append(f"{keyword_data['keyword']}: {keyword_data['description']}")

            # Format keywords for prompt
            keywords = "\n".join(selected_keyword_list)  # Join selected keywords as a string

            #     # Misconceptions and Common Mistakes Section
            # st.markdown('## Misconceptions and Common Mistakes:')
            # misconceptions = []
            # for misconception in data_2['misconceptionsAndCommonMistakes']:
            #     st.write(f"**Misconception**: {misconception['misconception']}")
            #     st.write(f"**Response**: {misconception['response']}")
            #     misconceptions.append(f"Misconception: {misconception['misconception']}\nResponse: {misconception['response']}")
            
            # misconceptions_text = "\n".join(misconceptions)

            # Pupil Lesson Outcome
            st.markdown('## Pupil Lesson Outcome:')
            pupil_outcome = data_2['pupilLessonOutcome']
            st.write(pupil_outcome)

            prior_knowledge = st.text_area("Prior knowledge", "")

            # Class profile section (below prior knowledge)
            st.markdown("### Class Profile")
            st.write("Indicate the number of students with specific needs:")

            autism = st.slider("Number of students with Autism", 0, 30, 0)
            dyslexia = st.slider("Number of students with Dyslexia", 0, 30, 0)
            adhd = st.slider("Number of students with ADHD", 0, 30, 0)
            eal = st.slider("Number of students with EAL (English as an Additional Language)", 0, 30, 0)

            # Display class profile summary
            st.markdown("### Class Profile Summary")
            st.write(f"Autism: {autism}")
            st.write(f"Dyslexia: {dyslexia}")
            st.write(f"ADHD: {adhd}")
            st.write(f"EAL: {eal}")
#add resources i need to make
            #openai request
            prompt = f"""
            You are a teacher planning a cover lesson for a teacher who may have little to no familiarity with the subject area.
            The cover teacher has been assigned to cover the {subject} lesson titled {selected_lesson_title}.
            The lesson is intended for students in {keyStage}.
            The following is what your class knows so far related to this lesson:
            {prior_knowledge}

            Make sure to include the following key learning points:
            {key_learning_points}

            The following are the keywords that should be included in the lesson:
            {keywords}

            The pupil lesson outcome is as follows:
            {pupil_outcome}

            There are specific needs in this class that the cover teacher should be aware of:
            - **{autism} students out of 30 with Autism**: Make sure instructions are clear and concise, minimise distractions, and allow for visual aids where necessary. Provide opportunities for predictable routines and avoid sudden changes.
            - **{dyslexia} students out of 30 with Dyslexia**: Use simple language and provide materials in multiple formats (e.g., videos, visuals) to support reading difficulties. Use tools like colored overlays and ensure extra time for written activities.
            - **{adhd} students out of 30 with ADHD**: Keep tasks short and engaging, and incorporate movement-based or hands-on activities. Use clear expectations and redirect attention as needed.
            - **{eal} students out of 30 with English as an Additional Language (EAL)**: Provide visual aids, translated resources if possible, and use simple language. Pair students with peers who can offer additional support.
            Do not make these separate adaptations but take them into account when choosing the activities.

            Please create a lesson plan that:
            - Starts with a 5 minute starter game that assesses key words and prior knowledge.
            - Research activities and follow up documentation should be included.
            - Include video exploration (with Youtube search title) after an introduction but limit it to 15 minutes with a worksheet they can follow along with it.
            - Does not require any expertise in the subject area and can be easily delivered by a cover teacher with minimal preparation.
            - Incorporates engaging and interactive tasks or group activities that allow students to work through the material independently or collaboratively.
            - Ensures that all key learning points are met through the use of video content, structured activities, and clear instructions that do not rely on the teacher's subject knowledge.
            - The cover teacher should not be required to demonstrate or model any concepts. Any activities that involve modelling should be clearly explained through a video or worksheet that students can follow independently.
            - Provide a list of considerations at the end of the end of the lesson plan.

            Based on the information provided, write a lesson plan for the cover lesson, ensuring that it is simple, accessible, and effective for both the teacher and students.
            """ 

            generate_button_clicked = st.button("Generate Lesson Plan")
            if generate_button_clicked:
                openai.api_key = os.getenv("OPENAI_API_KEY")
                client = OpenAI()
                try:
                    response = client.chat.completions.create(
                        model='gpt-4o',
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                        timeout=15,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )

                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Failed to generate lesson plan: {e}")
        
        except:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    else:
        st.error("No lessons found.")
except:

    print(f"Failed to retrieve data. Status code: {response.status_code}")

# The following are common misconceptions and mistakes that should be addressed:
# {misconceptions}