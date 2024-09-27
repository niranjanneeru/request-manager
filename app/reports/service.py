from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.ai import AIModels
from app.api import get_assessments
from app.reports.parser import ReportParser
from app.reports.prompts import enhance_comment_prompt, review_template, report_template


class ReportService:
    def enhance_comment(self, tone, formality, keywords, instructions, user_id):
        prompt = ChatPromptTemplate.from_template(enhance_comment_prompt)
        model = AIModels().enhance_comment_model()
        assessments = get_assessments(user_id)
        chain = (
                {
                    "tone": lambda x: tone,
                    "formality": lambda x: formality,
                    "keywords": lambda x: keywords or [],
                    "instructions": RunnablePassthrough,
                    "assessment_data": lambda x: '\n'.join(assessments)
                }
                | prompt
                | model
        )
        output = chain.invoke(lambda x: instructions or "No Instructions")
        return output

    def generate_review(self, person, user_id):
        prompt = ChatPromptTemplate.from_template(review_template)
        model = AIModels().review_model()
        assessments = get_assessments(user_id)
        chain = (
                {
                    "person": RunnablePassthrough,
                    "assessment_data": lambda x: '\n'.join(assessments)
                }
                | prompt
                | model
        )
        output = chain.invoke(lambda x: person)
        return output

    def report_generation(self, user_id):
        assessments = get_assessments(user_id)
        prompt = ChatPromptTemplate.from_template(report_template)
        model = AIModels().review_model()
        chain = (
                {
                    "message": RunnablePassthrough,
                    "assessment": lambda x: '\n'.join(assessments)
                }
                | prompt
                | model
                | ReportParser()
        )
        output = chain.invoke(lambda x: None or "Generate Report")
        return output
