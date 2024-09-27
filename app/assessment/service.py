from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.ai import AIModels
from app.assessment.parser import AssessmentOutputParser
from app.assessment.prompts import prompt_for_question, assessment_template, answer_template
from app.qdrant import QClient


class AssessmentService:
    def generate_assessment(self, topic, difficulty, question_distribution, document_id):
        question_pattern = '\n'.join(
            [prompt_for_question[r].format(number=v) for r, v in question_distribution.items()])
        prompt = ChatPromptTemplate.from_template(assessment_template)
        model = AIModels().assessment_model()

        if document_id:
            retriever = QClient().fetch_retriever_by_document_id(document_id)
        else:
            retriever = QClient().fetch_retriever()

        chain = (
                {"context": retriever,
                 "topic": RunnablePassthrough(),
                 "difficulty": lambda x: difficulty,
                 'creation': lambda x: question_pattern,
                 }
                | prompt
                | model
                | AssessmentOutputParser()
        )

        output = chain.invoke(topic)

        return output

    def answer_question(self, question, question_type, weightage, answer="", choices=None):
        if choices is None:
            choices = []
        prompt = ChatPromptTemplate.from_template(answer_template)
        model = AIModels().answering_model()

        chain = (
                {"context": QClient().fetch_retriever(),
                 "question": RunnablePassthrough(),
                 "type": lambda x: question_type,
                 'weightage': lambda x: weightage,
                 "answer": lambda x: answer,
                 'choices': lambda x: choices,
                 }
                | prompt
                | model
        )

        output = chain.invoke(question)

        return output
