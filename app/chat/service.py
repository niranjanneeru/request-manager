import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.ai import AIModels
from app.cache import Cache
from app.chat.prompts import teacher_chat_template
from app.qdrant import QClient

cache = Cache()


class ChatService:
    def teacher_chat(self, session_id, message):
        chat_history = cache.get(f"chat_history:{session_id}")
        if chat_history:
            chat_history = json.loads(chat_history)
        else:
            chat_history = []
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
        cache.set(f"chat_history:{session_id}", json.dumps(chat_history))
        return output
