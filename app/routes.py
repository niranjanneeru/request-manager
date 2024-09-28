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

    response = KnowledgeBase().add_to_kb(pdf_filename, document_id)

    try:
        os.remove(pdf_filename)
    except Exception as e:
        pass

    return jsonify(response), 200


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


@api.route('/score', methods=['POST'])
def score_answer():
    data = request.json

    question = data.get('question')
    question_type = data.get('type')
    answer = data.get('answer')
    total_score = data.get('total_score')
    document_id = data.get('document_id', None)

    response = assessment_service.score_answer(question, question_type, total_score, answer, document_id)

    return jsonify(response), 200


@api.route('/feedback', methods=['POST'])
def assessment_feedback():
    data = request.json

    assessment_name = data.get('assessment_name')
    score_obtained = data.get('score_obtained')
    assessment_difficulty = data.get('assessment_difficulty')
    total_score = data.get('total_score')
    assessment_outcomes = data.get('assessment_outcomes')
    questions_data = data.get('questions_data')
    document_id = data.get('document_id', None)

    response = assessment_service.feedback_generator(assessment_name, total_score, score_obtained,
                                                     assessment_difficulty, assessment_outcomes, document_id,
                                                     questions_data)

    return jsonify(response), 200


@api.route('assessment/properties', methods=['POST'])
def assessment_properties():
    data = request.json

    questions_data = data.get('questions_data')
    document_id = data.get('document_id', None)

    response = assessment_service.assessment_properties(questions_data, document_id)

    return jsonify(response), 200
