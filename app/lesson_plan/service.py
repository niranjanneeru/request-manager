from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.ai import AIModels
from app.cache import ChatHistoryCache
from app.lesson_plan.parser import LessonPlanParser
from app.lesson_plan.prompts import teacher_lesson_plan_template
from app.qdrant import QClient

cache = ChatHistoryCache()


class LessonPlan:
    def generate_lesson_plan(self, session_id, document_id, message):
        chat_history_cache_key = f"teacher_lesson_plan:{session_id}"
        chat_history = cache.get_chat_history(chat_history_cache_key)
        prompt = ChatPromptTemplate.from_template(teacher_lesson_plan_template)
        model = AIModels().lesson_plan_model()
        if document_id:
            retriever = QClient().fetch_retriever_by_document_id(document_id)
        else:
            retriever = QClient().fetch_retriever()

        def log_response(x):
            chat_history.append(f"User: {message}")
            chat_history.append(f"Assistant: {x}")
            return x

        chain = (
                {"context": retriever,
                 "message": RunnablePassthrough(),
                 # "chat_history": lambda x: '\n'.join(chat_history),
                 }
                | prompt
                | model
                | log_response
                | LessonPlanParser()
        )
        output = chain.invoke(message)
        cache.set_chat_history(chat_history_cache_key, chat_history)
        return output
