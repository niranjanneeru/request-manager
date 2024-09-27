from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.ai import AIModels
from app.cache import ChatHistoryCache
from app.chat.prompts import teacher_chat_template, student_chat_template
from app.qdrant import QClient

cache = ChatHistoryCache()


class ChatService:
    def teacher_chat(self, session_id, message):
        chat_history_cache_key = f"teacher_chat_history:{session_id}"
        chat_history = cache.get_chat_history(chat_history_cache_key)
        prompt = ChatPromptTemplate.from_template(teacher_chat_template)
        model = AIModels().chat_model()
        chain = (
                {"context": QClient().fetch_retriever(),
                 "message": RunnablePassthrough(),
                 "chat_history": lambda x: '\n'.join(chat_history),
                 }
                | prompt
                | model
        )
        output = chain.invoke(message)
        chat_history.append(f"User: {message}")
        chat_history.append(f"Assistant: {output}")
        cache.set_chat_history(chat_history_cache_key, chat_history)
        return output

    def student_chat(self, session_id, message):
        chat_history_cache_key = f"student_chat_history:{session_id}"
        chat_history = cache.get_chat_history(chat_history_cache_key)
        prompt = ChatPromptTemplate.from_template(student_chat_template)
        model = AIModels().chat_model()
        chain = (
                {"context": QClient().fetch_retriever(),
                 "message": RunnablePassthrough(),
                 "chat_history": lambda x: '\n'.join(chat_history),
                 }
                | prompt
                | model
        )
        output = chain.invoke(message)
        chat_history.append(f"User: {message}")
        chat_history.append(f"Assistant: {output}")
        cache.set_chat_history(chat_history_cache_key, chat_history)
        return output
