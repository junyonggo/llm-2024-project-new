import streamlit as st
from models.curriculum_model import CurriculumCreatorModel
from models.image_model import ImageCreatorModel

st.session_state["curriculum_model"] = CurriculumCreatorModel()
st.session_state["image_model"] = ImageCreatorModel()

home_page = st.Page("home.py", title="Home")
curriculum_overview_page = st.Page("pages/curriculum.py", title="Curriculum Overview")

pg = st.navigation([home_page, curriculum_overview_page], expanded=False)
st.set_page_config(page_title="Curriculum Creator", layout="wide", initial_sidebar_state="collapsed")

pg.run()

