import re
from typing import Dict, Any, List

from langchain_core.output_parsers import BaseOutputParser


class AssessmentOutputParser(BaseOutputParser):
    def parse(self, output_text):
        print(output_text)
        return self.aggregate_parser(output_text)

    def parse_mcq(self, question_block: str):
        mcq_pattern = re.compile(
            r"- Type of Question: MCQ.*?Weightage: (\d+)%.*?Question: (.*?)Choice:(.*?)Answer: ([a-d])", re.DOTALL)
        match = mcq_pattern.search(question_block)
        if match:
            weightage = int(match.group(1))
            question = match.group(2).strip()
            choices = [choice.strip() for choice in re.findall(r"\b[a-d]\) (.+)", match.group(3))]
            answer = match.group(4).strip()
            return {
                "type": "MCQ",
                "weightage": weightage,
                "question": question,
                "choices": choices,
                "answer": answer
            }
        return None

    def parse_true_false(self, question_block: str):
        tf_pattern = re.compile(
            r"- Type of Question: True/False.*?Weightage: (\d+)%.*?Question: (.*?)Choice:(.*?)Answer: (True|False)",
            re.DOTALL)
        match = tf_pattern.search(question_block)
        if match:
            weightage = int(match.group(1))
            question = match.group(2).strip()
            choices = ["True", "False"]
            answer = match.group(4).strip()
            return {
                "type": "True/False",
                "weightage": weightage,
                "question": question,
                "choices": choices,
                "answer": answer
            }
        return None

    def parse_short_answer(self, question_block: str):
        sa_pattern = re.compile(
            r"- Type of Question: Short Answer.*?Weightage: (\d+)%.*?Question: (.*?)No Answer Required", re.DOTALL)
        match = sa_pattern.search(question_block)
        if match:
            weightage = int(match.group(1))
            question = match.group(2).strip()
            return {
                "type": "Short Answer",
                "weightage": weightage,
                "question": question
            }
        return None

    def parse_essay(self, question_block: str):
        essay_pattern = re.compile(r"- Type of Question: Essay.*?Weightage: (\d+)%.*?Question: (.*?)No Answer Required",
                                   re.DOTALL)
        match = essay_pattern.search(question_block)
        if match:
            weightage = int(match.group(1))
            question = match.group(2).strip()
            return {
                "type": "Essay",
                "weightage": weightage,
                "question": question
            }
        return None

    def parse_assertion_reason(self, question_block: str):
        ar_pattern = re.compile(
            r"- Type of Question: Assertion-Reason.*?Weightage: (\d+)%.*?Assertion: (.*?)Reason: (.*?)Choice:(.*?)Answer: ([a-d])",
            re.DOTALL)
        match = ar_pattern.search(question_block)
        if match:
            weightage = int(match.group(1))
            assertion = match.group(2).strip()
            reason = match.group(3).strip()
            choices = [choice.strip() for choice in re.findall(r"\b[a-d]\) (.+)", match.group(4))]
            answer = match.group(5).strip()
            return {
                "type": "Assertion-Reason",
                "weightage": weightage,
                "question": f"Assertion: {assertion}\n Reason: {reason}",
                "choices": choices,
                "answer": answer
            }
        return None

    def parse_case_study(self, question_block: str):
        cs_pattern = re.compile(
            r"- Type of Question: Case Study.*?Weightage: (\d+)%.*?Question: (.*?)No Answer Required", re.DOTALL)
        match = cs_pattern.search(question_block)
        if match:
            weightage = int(match.group(1))
            question = match.group(2).strip()
            return {
                "type": "Case Study",
                "weightage": weightage,
                "question": question
            }
        return None

    def aggregate_parser(self, content: str) -> List[Dict[str, Any]]:
        question_blocks = content.split("\n\n")

        parsed_questions = []

        for block in question_blocks:
            if "Type of Question: MCQ" in block:
                parsed_questions.append(self.parse_mcq(block))
            elif "Type of Question: True/False" in block:
                parsed_questions.append(self.parse_true_false(block))
            elif "Type of Question: Short Answer" in block:
                parsed_questions.append(self.parse_short_answer(block))
            elif "Type of Question: Essay" in block:
                parsed_questions.append(self.parse_essay(block))
            elif "Type of Question: Assertion-Reason" in block:
                parsed_questions.append(self.parse_assertion_reason(block))
            elif "Type of Question: Case Study" in block:
                parsed_questions.append(self.parse_case_study(block))

        return [q for q in parsed_questions if q is not None]  # Filter out None values
