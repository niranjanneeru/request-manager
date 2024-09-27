import os

import requests
from flask import Blueprint, jsonify, request

from app.assessment.service import AssessmentService
from app.kb import KnowledgeBase

api = Blueprint('api', __name__)

assessment_service = AssessmentService()


@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200


@api.route('/add-kb', methods=['POST'])
def add_to_knowledge_base():
    data = request.json

    if not data or 'pdf_url' not in data:
        return jsonify({"error": "No PDF URL provided"}), 400

    pdf_url = data['pdf_url']
    document_id = data['document_id']

    response = requests.get(pdf_url)
    if response.status_code != 200:
        return jsonify({"error": f"Failed to download PDF. Status code: {response.status_code}"}), 400

    pdf_filename = os.path.join("/tmp", "downloaded.pdf")
    with open(pdf_filename, 'wb') as f:
        f.write(response.content)

    KnowledgeBase().add_to_kb(pdf_filename, document_id)

    os.remove(pdf_filename)

    return jsonify({"message": "PDF processed and stored successfully!"}), 200


@api.route('/generate-assessment', methods=['POST'])
def generate_assessment():
    data = request.json

    topic = data.get('topic')
    difficulty = data.get('difficulty')
    question_distribution = data.get('question_distribution')
    document_id = data.get('document_id', None)

    if not topic or not difficulty or not question_distribution:
        return jsonify({"error": "Missing required parameters: topic, difficulty, or question_distribution"}), 400

    response = assessment_service.generate_assessment(topic, difficulty, question_distribution, document_id)

    return jsonify(response), 200

@api.route('/answer', methods=['POST'])
def answer_question():
    data = request.json

    question = data.get('question')
    question_type = data.get('type')
    weightage = data.get('weightage')
    answer = data.get('answer')
    choices = data.get('choices')

    response = assessment_service.answer_question(question, question_type, weightage, answer, choices)

    return jsonify(response), 200