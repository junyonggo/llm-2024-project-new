import streamlit as st
from config import Config
from openai import OpenAI

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

class ImageCreatorModel:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,  # This is the default and can be omitted
        )

    def generate_curriculum_image(self, grade_level, subject, topic):

        prompt = f"""
            Create an image based on {subject} and using {topic} as the image content.
            Ensure that the image is appropriate for students at the {grade_level} grade level.
            Ensure that any words displayed on the image are spelled correctly.
        """

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=Config.IMAGE_SIZE,
            style=Config.IMAGE_STYLE
        )

        img_url = response.data[0].url
        return img_url
    

    def generate_curriculum_unit_image(self, unit_overview, unit_lessons):

        unit_lessons_str = '\n'.join(unit_lessons)

        prompt = f"""
        Create an image for the curriculum unit of lessons with the unit overview and lessons provided below.
        Ensure that any words displayed on the image are spelled correctly.

        Unit Overview: {unit_overview}

        Unit Lessons:
        {unit_lessons_str}
        """


        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=Config.IMAGE_SIZE,
            style=Config.IMAGE_STYLE
        )

        img_url = response.data[0].url
        return img_url