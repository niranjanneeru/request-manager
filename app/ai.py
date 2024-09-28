from langchain_together import Together


class AIModels:
    def assessment_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )

    def answering_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )

    def chat_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )

    def lesson_plan_model(self):
        return Together(
            model="mistralai/Mixtral-8x22B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=32000
        )

    def assessment_feedback_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )

    def document_properties_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )

    def enhance_comment_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )

    def review_model(self):
        return Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.7,
            top_k=50,
            max_tokens=1000
        )
