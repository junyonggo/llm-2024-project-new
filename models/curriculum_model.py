import streamlit as st
from config import Config
from openai import OpenAI
from data.CurriculumOverview import CurriculumOverview
from data.CurriculumUnit import CurriculumUnit

# Pull our API key from the toml file
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


class CurriculumCreatorModel:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        # Create an empty thread to store the messages between the user and the assistants
        self.thread = self.client.beta.threads.create()

        # See if each assistant that we need exists. If it doesn't, create it.

        # Curriculum Overview Assistant
        curriculum_overview_assistant = self.find_assistant_by_name(
            Config.CURRICULUM_OVERVIEW_ASSISTANT_NAME)
        if curriculum_overview_assistant is None:
            self.curriculum_overview_assistant = self.create_assistant(
                Config.CURRICULUM_OVERVIEW_ASSISTANT_NAME, Config.CURRICULUM_OVERVIEW_ASSISTANT_INSTRUCTIONS, Config.CURRICULUM_OVERVIEW_SCHEMA_NAME, CurriculumOverview)
        else:
            self.curriculum_overview_assistant = curriculum_overview_assistant

        # Curriculum Unit Assistant
        curriculum_unit_assistant = self.find_assistant_by_name(
            Config.CURRICULUM_UNIT_ASSISTANT_NAME)
        if curriculum_unit_assistant is None:
            self.curriculum_unit_assistant = self.create_assistant(
                Config.CURRICULUM_UNIT_ASSISTANT_NAME, Config.CURRICULUM_UNIT_ASSISTANT_INSTRUCTIONS, Config.CURRICULUM_UNIT_SCHEMA_NAME, CurriculumUnit)
        else:
            self.curriculum_unit_assistant = curriculum_unit_assistant

    def create_assistant(self, assistant_name, assistant_instructions, assistant_schema_name, assistant_schema):
        """
        Create an assistant from OpenAI

        Parameters:
        ----------
        assistant_name : string
            The name of the assistant
        assistant_instructions : string
            The instructions for the assistant
        assistant_schema_name : string
            The name of the schema for the assistant
        assistant_schema: Class(BaseModel)
            A BaseModel of the assistant which specifies the attributes of the assistant's output

        Returns:
        -------
        assistant: assistant object
            The assistant object - more information can be found here: https://platform.openai.com/docs/api-reference/assistants/object
        """
        return self.client.beta.assistants.create(
            name=assistant_name,
            instructions=assistant_instructions,
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            response_format={
                'type': 'json_schema',
                'json_schema':
                    {
                        "name": assistant_schema_name,
                        "schema": assistant_schema.model_json_schema()
                    }
            },
        )

    def find_assistant_by_name(self, assistant_name=None):
        """
        Find an assistant from OpenAI by its name, if it exists

        Parameters:
        ----------
        assistant_name : string | None
            The name of the assistant

        Returns:
        -------
        assistant: assistant object | None
            The assistant object (if it exists) - more information can be found here: https://platform.openai.com/docs/api-reference/assistants/object
        """
        # If the name isn't specified, return
        if not assistant_name:
            return
        assistants = self.client.beta.assistants.list()
        # If we don't have any assistants, return
        if not assistants:
            return

        for assistant in assistants:
            if assistant.name == assistant_name:
                return assistant
        return

    def generate_curriculum_overview(self, grade_level, subject, topic, num_units, num_lessons):
        """
        Generate an overview of the curriculum

        Parameters:
        ----------
        grade_level : string
            The grade level as a string (e.g. Kindergarten, Fourth, Fifth, etc.)
        subject : string
            The subject for the curriculum (e.g. Math, English, etc)
        topic : string
            The subject for the curriculum (e.g. Sports, Arts, Dinosaurs, etc.)
        num_units: integer
            The number of units our curriculum should have
        num_lessons: integer
            The number of lessons each unit should have

        Returns:
        -------
        string
            A JSON representation in string format of our curriculum - see the CurriculumOverview class for the schema structure
        """

        prompt = f"""
            Create a curriculum overview, including units that include lessons and assignments,
            based on {subject} at the {grade_level} grade level and using {topic} as the content.
            Ensure that there are {num_units} units and that there are {num_lessons} lessons per unit.
            Ensure that the curriculum is self-contained, meaning that the readings
            are also generated and are not from a book or any external material.
            Ensure that the units are titled with "Unit 1:...", "Unit 2:...",
            and so forth and the lessons with each unit are also titled "Lesson 1:...", Lesson 2:...", and so forth.
            Ensure that the response is also strictly in JSON format and does not use any Markdown.
        """

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.curriculum_overview_assistant.id,
        )

        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

        return messages.data[0].content[0].text.value

    def generate_curriculum_unit(self, unit_overview, unit_lessons, unit_assignments):
        """
        Generate the entire curriculum unit, including lessons and questions, based on the unit overview

        Parameters:
        ----------
        unit_overview : string
            An overview of the curriculum unit, describing what is covered based on the topic and subject
        unit_lessons: list[string]
            A list of strings containing the lesson overviews in the unit
        unit_assignments: list[string]
            A list of strings containing the assignments in the unit

        Returns:
        -------
        string
            A JSON representation in string format of our curriculum unit - see the CurriculumUnit class for the schema structure
        """

        unit_lessons_str = '\n'.join(unit_lessons)
        unit_assignments_str = '\n'.join(unit_assignments)

        prompt = f"""
        Create an entire curriculum unit of lessons with the unit overview, lessons, and assignments provided below.
        Ensure that each lesson has at least three paragraphs and a quiz that has at least three questions.
        Ensure that each paragraph has at least 4-5 sentences and that the paragraph is relevant to the lesson.
        Ensure that the questions asked in the quiz are derived from the lesson and its paragraph.
        Ensure that the response and output are strictly in JSON format and do not use any Markdown.

        Unit Overview: {unit_overview}

        Unit Lessons:
        {unit_lessons_str}

        Unit Assignments:
        {unit_assignments_str}
        """

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.curriculum_unit_assistant.id,
        )

        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

        return messages.data[0].content[0].text.value
