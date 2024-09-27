from flask import Blueprint, jsonify, request

from app.chat.service import ChatService

chat = Blueprint('chat', __name__)

chat_service = ChatService()


@chat.route('/teacher', methods=['POST'])
def teacher_chat():
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    response = chat_service.teacher_chat(session_id, message)

    return jsonify({"message": f"{response}"}), 200


@chat.route('/student', methods=['POST'])
def student_chat():
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    response = chat_service.student_chat(session_id, message)

    return jsonify({"message": f"{response}"}), 200
