from flask import Blueprint, request, jsonify

from app.reports.service import ReportService

reports = Blueprint('reports', __name__)

report_service = ReportService()


@reports.route('/comment-enhance', methods=["POST"])
def enhance_comment():
    data = request.json
    tone = data.get('tone')
    formality = data.get('formality')
    keywords = data.get('keywords')
    instructions = data.get('instructions')
    user_id = data.get('user_id')

    response = report_service.enhance_comment(tone, formality, keywords, instructions, user_id)
    return jsonify(response), 200

@reports.route('/generate', methods=["POST"])
def generate_report():
    data = request.json
    user_id = data.get('user_id')

    response = report_service.report_generation(user_id)
    return jsonify(response), 200
