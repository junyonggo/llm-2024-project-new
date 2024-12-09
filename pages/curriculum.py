import json
import streamlit as st
import streamlit_book as stb

# Check if required session state variables exist
if "curriculum_overview" not in st.session_state or "grade_level" not in st.session_state or "subject" not in st.session_state or "topic" not in st.session_state:
    st.error("Please go to the home page and create the curriculum overview first!")
    st.stop()

# Retrieve inputs
curriculum_model = st.session_state["curriculum_model"]
curriculum_overview = st.session_state["curriculum_overview"]
curriculum_units_overview = curriculum_overview["units"]
image_model = st.session_state["image_model"]

st.title("Curriculum")

units = []
unit_tabs = []

if "unit_tabs" not in st.session_state:

    for unit_overview in curriculum_units_overview:
        unit_tabs.append(unit_overview["title"])

    st.session_state["unit_tabs"] = unit_tabs

unit_tabs = st.session_state["unit_tabs"]
tabs = st.tabs(unit_tabs)

for unit, tab in zip(curriculum_units_overview, tabs):
    with tab:
        unit_container = st.container(border=True)
        unit_container.header(unit["title"])

        if unit["title"] not in st.session_state:
            with st.spinner('Creating the Unit...'):
                curriculum_unit_str = curriculum_model.generate_curriculum_unit(unit["overview"], unit["lessons"], unit["assignments"])
                curriculum_unit_img = image_model.generate_curriculum_unit_image(unit["overview"], unit["lessons"])
                st.session_state[unit["title"]] = {}
                st.session_state[unit["title"]]["content"] = json.loads(curriculum_unit_str)
                st.session_state[unit["title"]]["image"] = curriculum_unit_img

        curriculum_unit = st.session_state[unit["title"]]["content"]
        curriculum_unit_img = st.session_state[unit["title"]]["image"]

        unit_container.image(curriculum_unit_img, use_container_width=True)
        unit_container.write(unit["overview"])
        
        for lesson in curriculum_unit["lessons"]:
            lesson_expander = st.expander(lesson["title"])
            lesson_expander.subheader(lesson["title"])

            for paragraph in lesson["paragraphs"]:
                lesson_expander.write(paragraph)

            # Create the Quiz section
            lesson_expander.subheader("Quiz")

            for question in lesson["quiz"]:

                question_sentence = question["sentence"]
                question_possible_answers = question["possible_answers"]
                question_answer_idx = question_possible_answers.index(question["correct_answer"])

                with lesson_expander.container(border=True):
                    # Create a single choice question with the possible answers and the correct answer we have
                    stb.single_choice(question_sentence, question_possible_answers, question_answer_idx, "Correct!", "Incorrect - Please Try Again!")
