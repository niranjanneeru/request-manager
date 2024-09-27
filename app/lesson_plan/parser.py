import re

from langchain_core.output_parsers import BaseOutputParser


class LessonPlanParser(BaseOutputParser):
    def parse(self, lesson_plan_text: str):
        lesson_plan = {
            "expected_learning_outcomes": self.parse_section(lesson_plan_text, "1. Expected Learning Outcomes"),
            "expected_skill_development": self.parse_section(lesson_plan_text, "7. Expected Skill Development"),
            "learning_objectives": self.parse_section(lesson_plan_text, "2. Learning Objectives"),
            "key_topics_and_concepts": self.parse_section(lesson_plan_text, "3. Key Topics and Concepts"),
            "teaching_methods": self.parse_section(lesson_plan_text, "4. Teaching Methods"),
            "activities_or_exercises": self.parse_section(lesson_plan_text, "5. Activities or Exercises"),
            "assessment_methods": self.parse_section(lesson_plan_text, "6. Assessment Methods")
        }
        return lesson_plan

    def parse_section(self, text: str, section_name: str):
        # Regex to match each section based on the section name and numbering pattern
        pattern = re.compile(rf"{section_name}\n- (.*?)(?=\n\d\.|\Z)", re.DOTALL)
        match = pattern.search(text)
        if match:
            return [item.strip() for item in match.group(1).split('\n- ')]
        return []
