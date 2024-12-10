# config.py

class Config:
    MODEL_NAME = "gpt-4o-2024-08-06"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.2
    IMAGE_MODEL = "dall-e-3"
    IMAGE_SIZE = "1024x1024"
    IMAGE_STYLE = "natural"
    CURRICULUM_OVERVIEW_ASSISTANT_NAME = "Curriculum Overview Assistant"
    CURRICULUM_OVERVIEW_ASSISTANT_INSTRUCTIONS = "You are a curriculum overview assistant."
    CURRICULUM_OVERVIEW_SCHEMA_NAME = "CurriculumOverview"
    CURRICULUM_UNIT_ASSISTANT_NAME = "Curriculum Unit Assistant"
    CURRICULUM_UNIT_ASSISTANT_INSTRUCTIONS = "You are a curriculum unit assistant."
    CURRICULUM_UNIT_SCHEMA_NAME = "CurriculumUnit"
