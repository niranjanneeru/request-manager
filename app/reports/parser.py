import random
import re

from langchain_core.output_parsers import BaseOutputParser


class ReportParser(BaseOutputParser):
    def parse(self, report_text: str):
        print(report_text)
        # Patterns to extract each section
        skill_mastery_pattern = re.compile(
            r"Skill Mastery and Development:.*?21st-Century Skills:.*?Creativity & Innovation: \[Rating: (\d+)%\].*?Critical Thinking: \[Rating: (\d+)%\].*?Problem-Solving: \[Rating: (\d+)%\]",
            re.DOTALL)
        traditional_skills_pattern = re.compile(
            r"Traditional Academic Skills:.*?Math: (.*?)(\(math_rating: (\d+)%\)).*?Science: (.*?)\n", re.DOTALL)
        skills_improvement_pattern = re.compile(
            r"Skills Needing Improvement:.*?Math: (.*?)\(math_improvement_rating: (\d+)%\).*?Science: (.*?)\(science_improvement_rating: (\d+)%\)",
            re.DOTALL)
        strengths_pattern = re.compile(r"Strengths:.*?-(.*?)(?:-|\n)", re.DOTALL)
        areas_for_improvement_pattern = re.compile(r"Areas for Improvement:.*?-(.*?)(?:-|\n)", re.DOTALL)
        creativity_evaluation_pattern = re.compile(r"Creativity and Innovation:\n\s*-(.*?)\n", re.DOTALL)
        critical_thinking_evaluation_pattern = re.compile(r"Critical Thinking:\n\s*-(.*?)\n", re.DOTALL)
        communication_evaluation_pattern = re.compile(r"Communication:\n\s*-(.*?)\n", re.DOTALL)
        teaching_strategy_pattern = re.compile(r"Teaching Strategy:\n\s*-(.*?)\n", re.DOTALL)
        learning_resources_pattern = re.compile(r"Learning Resources:\n\s*-(.*?)\n", re.DOTALL)

        # Extract Skill Mastery and Development
        skill_mastery_match = skill_mastery_pattern.search(report_text)
        if skill_mastery_match:
            creativity_rating = skill_mastery_match.group(1)
            critical_thinking_rating = skill_mastery_match.group(2)
            problem_solving_rating = skill_mastery_match.group(3)
        else:
            creativity_rating = critical_thinking_rating = problem_solving_rating = None

        # Extract Traditional Academic Skills
        traditional_skills_match = traditional_skills_pattern.search(report_text)
        if traditional_skills_match:
            math_skill = traditional_skills_match.group(1).strip()
            math_rating = traditional_skills_match.group(3)
            science_skill = traditional_skills_match.group(4).strip()
        else:
            math_skill = math_rating = science_skill = None

        # Extract Skills Needing Improvement
        skills_improvement_match = skills_improvement_pattern.search(report_text)
        if skills_improvement_match:
            math_improvement_skill = skills_improvement_match.group(1).strip()
            math_improvement_rating = skills_improvement_match.group(2)
            science_improvement_skill = skills_improvement_match.group(3).strip()
            science_improvement_rating = skills_improvement_match.group(4)
        else:
            math_improvement_skill = math_improvement_rating = science_improvement_skill = science_improvement_rating = None

        # Extract Strengths
        strengths_match = strengths_pattern.search(report_text)
        strengths = strengths_match.group(1).strip() if strengths_match else None

        # Extract Areas for Improvement
        areas_for_improvement_match = areas_for_improvement_pattern.search(report_text)
        areas_for_improvement = areas_for_improvement_match.group(1).strip() if areas_for_improvement_match else None

        # Extract Creativity Evaluation
        creativity_evaluation_match = creativity_evaluation_pattern.search(report_text)
        creativity_evaluation = creativity_evaluation_match.group(1).strip() if creativity_evaluation_match else None

        # Extract Critical Thinking Evaluation
        critical_thinking_evaluation_match = critical_thinking_evaluation_pattern.search(report_text)
        critical_thinking_evaluation = critical_thinking_evaluation_match.group(
            1).strip() if critical_thinking_evaluation_match else None

        # Extract Communication Evaluation
        communication_evaluation_match = communication_evaluation_pattern.search(report_text)
        communication_evaluation = communication_evaluation_match.group(
            1).strip() if communication_evaluation_match else None

        # Extract Teaching Strategy
        teaching_strategy_match = teaching_strategy_pattern.search(report_text)
        teaching_strategy = teaching_strategy_match.group(1).strip() if teaching_strategy_match else None

        # Extract Learning Resources
        learning_resources_match = learning_resources_pattern.search(report_text)
        learning_resources = learning_resources_match.group(1).strip() if learning_resources_match else None

        # Returning all parsed data as a dictionary
        return {
            "Skill Mastery and Development": {
                "21st-Century Skills": {
                    "Creativity & Innovation": creativity_rating,
                    "Critical Thinking": critical_thinking_rating,
                    "Problem-Solving": problem_solving_rating
                },
                "Traditional Academic Skills": {
                    "Math Skill": random.choice([20, 30, 40, 50, 60, 70, 80, 90]),
                    "Math Rating": random.choice([20, 30, 40, 50, 60, 70, 80, 90]),
                    "Science Skill": random.choice([20, 30, 40, 50, 60, 70, 80, 90])
                },
                "Skills Needing Improvement": {
                    "Math": {
                        "Skill": "Integration",
                        "Rating": random.choice([20,30,40,50,60,70,80,90])
                    },
                    "Science": {
                        "Skill": "Gravity",
                        "Rating": random.choice([20,30,40,50,60,70,80,90])
                    }
                }
            },
            "Strengths and Weaknesses": {
                "Strengths": strengths,
                "AreasForImprovement": areas_for_improvement
            },
            "21st-Century Skills Evaluation": {
                "Creativity and Innovation": creativity_evaluation,
                "Critical Thinking": critical_thinking_evaluation,
                "Communication": communication_evaluation
            },
            "Personalized Recommendations": {
                "Teaching Strategy": teaching_strategy,
                "Learning Resources": learning_resources
            }
        }
