from config import Config
from openai import OpenAI
from data.CurriculumOverview import CurriculumOverview
from data.CurriculumUnit import CurriculumUnit
from data.Lesson import Lesson


class CurriculumCreatorModel:
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,  # This is the default and can be omitted
        )
        self.conversation_history = []  # Stores context as a list of messages

        # Create an Assistant
        self.curriculum_assistant = self.client.beta.assistants.create(
            name="Curriculum",
            instructions="You are a curriculum assistant.",
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            response_format={
                'type': 'json_schema',
                'json_schema':
                    {
                        "name": "whocares",
                        "schema": CurriculumOverview.model_json_schema()
                    }
            },
        )

        self.curriculum_unit_assistant = self.client.beta.assistants.create(
            name="Curriculum Unit Assistant",
            instructions="You are a curriculum unit assistant.",
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            response_format={
                'type': 'json_schema',
                'json_schema':
                    {
                        "name": "whocares",
                        "schema": CurriculumUnit.model_json_schema()
                    }
            },
        )

        self.lesson_assistant = self.client.beta.assistants.create(
            name="Lesson Assistant",
            instructions="You are a lesson assistant.",
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            response_format={
                'type': 'json_schema',
                'json_schema':
                    {
                        "name": "whocares",
                        "schema": Lesson.model_json_schema()
                    }
            },
        )

        self.thread = self.client.beta.threads.create()

        self.message_history = []  # Stores a list of messages

    def add_message_to_history(self, role, content):
        """
        Add a message to the conversation history.

        Args:
            role (str): Role of the message sender ('system', 'user', 'assistant').
            content (str): The message content.
        """
        self.conversation_history.append({"role": role, "content": content})

    def generate_curriculum_overview(self, grade_level, subject, topic, num_units, num_lessons):

        prompt = f"""
            Create a curriculum overview, including units that include lessons and assignments,
            based on {subject} at the {grade_level} grade level and using {topic} as the content.
            Ensure that there are {num_units} units and that there are {num_lessons} lessons per unit.
            Ensure that the curriculum is self-contained, meaning that the readings
            are also generated and are not from a book or any external material.
            Ensure that the response is also strictly in JSON format and do not use any Markdown.
            Ensure that the units are titled with "Unit 1:...", "Unit 2:...",
            and so forth and the lessons with each unit are also titled "Lesson 1:...", Lesson 2:...", and so forth.
        """

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.curriculum_assistant.id,
        )

        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        # print(messages.data[0].content[0].text.value)
        return messages.data[0].content[0].text.value

    def generate_curriculum_unit(self, unit_overview, unit_lessons, unit_assignments):

        unit_lessons_str = '\n'.join(unit_lessons)
        unit_assignments_str = '\n'.join(unit_assignments)

        prompt = f"""
        Create an entire curriculum unit of lessons with the unit overview, lessons, and assignments provided below.
        Ensure that each lesson has at least three paragraphs and a quiz that has at least three questions.
        Ensure that the questions asked in the quiz are derived from the lesson and its paragraph.
        Ensure that the response and output is strictly in JSON format and do not use any Markdown.

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
