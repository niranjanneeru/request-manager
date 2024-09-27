from flask import Blueprint, jsonify, request

from app.lesson_plan.service import LessonPlan

lesson_plan = Blueprint('lesson-plan', __name__)

lesson_plan_service = LessonPlan()


@lesson_plan.route('/', methods=['POST'])
def generate_lesson_plan():
    data = request.json
    session_id = data.get('session_id')
    document_id = data.get('document_id')
    message = data.get('message')
    response = lesson_plan_service.generate_lesson_plan(session_id, document_id, message)
    return jsonify(response), 200
