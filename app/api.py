import requests

from config import Config


def get_assessments(user_id):
    url = f"{Config.BASE_URL}/ums/api/student-assessment/list/{user_id}"
    response = requests.request("POST", url)
    assessments = response.json()['studentAssessments']
    assessment_report = []
    for assessment in assessments:
        assessment_report.append(
            f"Name:{assessment['assessment']['name']}, Score:{assessment['score']}, Difficulty: {assessment['assessment']['level']}, Average Score: {assessment['assessment']['avgScore']}, Outcomes:{assessment['assessment']['outcomes']}")
    return assessment_report
