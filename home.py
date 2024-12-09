import json
import streamlit as st
import constants as const

curriculum_model = st.session_state["curriculum_model"]
image_model = st.session_state["image_model"]

# Add title
st.title("Curriculum Creator")

# Form
with st.form("home_form"):
    st.subheader("Create Your Curriculum Overview!")

    grade_level = st.selectbox(
        "Grade Level",
        const.GRADE_LEVEL_TUPLE,
        index=None,
        placeholder="Select Grade Level...",
    )
    subject = st.text_input("Subject", placeholder=const.SUBJECT_PLACEHOLDER)
    topic = st.text_input("Topic", placeholder=const.TOPIC_PLACEHOLDER)
    num_units = st.number_input("Number of Units", min_value=1, max_value=10, value=5, step=1)
    num_lessons = st.number_input("Number of Lessons per Unit", min_value=1, max_value=10, value=3, step=1)
    submitted = st.form_submit_button("Create Curriculum Overview", type="primary")

    if submitted:
        if subject and topic and grade_level:
            st.session_state["grade_level"] = grade_level
            st.session_state["subject"] = subject
            st.session_state["topic"] = topic

            with st.spinner('Creating the Curriculum Overview...'):
                curriculum_overview_str = curriculum_model.generate_curriculum_overview(grade_level, subject, topic, num_units, num_lessons)
                st.session_state["curriculum_overview"] = json.loads(curriculum_overview_str)

                curriculum_overview_img = image_model.generate_curriculum_image(grade_level, subject, topic)
                st.session_state["curriculum_overview_img"] = curriculum_overview_img

            st.success("The curriculum overview has been created below!")
        else:
            st.error("Please fill out all fields.")


if "curriculum_overview" in st.session_state:
    curriculum_overview = st.session_state["curriculum_overview"]

    container = st.container(border=True)

    container.title(curriculum_overview["title"])

    if "curriculum_overview_img" in st.session_state:
        curriculum_overview_img= st.session_state["curriculum_overview_img"]
        container.image(curriculum_overview_img, use_container_width=True)

    container.write(curriculum_overview["overview"])

    for unit in curriculum_overview["units"]:
        
        unit_container = container.expander(unit["title"])

        unit_container.header(unit["title"])
        unit_container.write(unit["overview"])

        unit_container.subheader("Lessons")
        for lesson in unit["lessons"]:
            unit_container.write(lesson)

        unit_container.subheader("Assignments")
        for assignment in unit["assignments"]:
            unit_container.write(assignment)
    
    with container.form("curriculum_form"):
        curriculum_created = st.form_submit_button("Generate Entire Curriculum", type="primary")

        if curriculum_created:
            st.switch_page("pages/curriculum.py")
