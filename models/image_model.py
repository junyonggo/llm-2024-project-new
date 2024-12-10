import streamlit as st
from config import Config
from openai import OpenAI

# Pull our API key from the toml file
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

class ImageCreatorModel:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def generate_curriculum_image(self, grade_level, subject, topic):
        """
        Generate the curriculum image

        Parameters:
        ----------
        grade_level : string
            The grade level as a string (e.g. Kindergarten, Fourth, Fifth, etc.)
        subject : string
            The subject for the curriculum (e.g. Math, English, etc)
        topic : string
            The subject for the curriculum (e.g. Sports, Arts, Dinosaurs, etc.)

        Returns:
        -------
        img_url: string
            The URL of the generated image - more information can be found here: https://platform.openai.com/docs/api-reference/images
        """

        prompt = f"""
            Create an image based on {subject} and using {topic} as the image content.
            Ensure that the image is appropriate for students at the {grade_level} grade level.
            Ensure that any words displayed on the image are spelled correctly.
        """

        response = self.client.images.generate(
            model=Config.IMAGE_MODEL,
            prompt=prompt,
            size=Config.IMAGE_SIZE,
            style=Config.IMAGE_STYLE
        )

        img_url = response.data[0].url
        return img_url
    

    def generate_curriculum_unit_image(self, unit_overview, unit_lessons):

        """
        Generate the image for the curriculum unit

        Parameters:
        ----------
        unit_overview : string
            An overview of the curriculum unit, describing what is covered based on the topic and subject
        unit_lessons: list[string]
            A list of strings containing the lesson overviews in the unit

        Returns:
        -------
        img_url: string
            The URL of the generated image - more information can be found here: https://platform.openai.com/docs/api-reference/images
        """

        unit_lessons_str = '\n'.join(unit_lessons)

        prompt = f"""
        Create an image for the curriculum unit of lessons with the unit overview and lessons provided below.
        Ensure that any words displayed on the image are spelled correctly.

        Unit Overview: {unit_overview}

        Unit Lessons:
        {unit_lessons_str}
        """


        response = self.client.images.generate(
            model=Config.IMAGE_MODEL,
            prompt=prompt,
            size=Config.IMAGE_SIZE,
            style=Config.IMAGE_STYLE
        )

        img_url = response.data[0].url
        return img_url