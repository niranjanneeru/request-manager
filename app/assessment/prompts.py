prompt_for_question = {
    'MCQ': '{number} MCQs (Multiple Choice Questions): These are questions where a user selects the correct answer from 4 provided options.',
    'True/False': '{number} True/False: A statement is given, and the user chooses whether the statement is true or false.',
    'Short Answer': '{number} Short Answer: These are brief responses, usually 1-2 sentences or a few words.',
    'Essay': '{number} Essay: These questions require a detailed, in-depth response explaining or discussing a given topic',
    'Assertion-Reason': '{number} Assertion-Reason: These questions consist of an assertion and a reason. The user must determine whether both are correct, and if the reason correctly explains the assertion.',
    'Case Study': '{number} Case Study: These are scenario-based questions where the user is presented with a situation and asked to analyze or provide a solution based on the context.'
}

assessment_template = """<s>[INST] You are an Assessment Creator Assistant. A user is in conversation with you to build an assessment.

context: {context}

Based on the given context, create:

{creation}

on the topic {topic} and set difficulty level as {difficulty}.

Ensure that the questions are accurate and relevant to the syllabus, context, and difficulty level.

**Weightage Instruction:**
- Weightage for each question should be assigned as a percentage based on the difficulty level and question type.
- Weightage order for question type - Case Study > Essays > Short Answer > MCQ > Assertion_Reasoning > True/False
- The sum of all question weightage percentages should be strictly equal to 100%.

**Output Format - For:**

1. **MCQs (Multiple Choice Questions):**
   - Type of Question: MCQ
   - Weightage: Percentage for the Question
   - Question: Question relevant to the context
   - Choice:
     a) option 1
     b) option 2
     c) option 3
     d) option 4
   - Answer: correct option

2. **True/False:**
   - Type of Question: True/False
   - Weightage: Percentage for the Question
   - Question: Question relevant to the context
   - Choice:
     - True
     - False
   - Answer: True/False

3. **Short Answer:**
   - Type of Question: Short Answer
   - Weightage: Percentage for the Question
   - Question: Question relevant to the context
   - No Answer Required

4. **Essay:**
   - Type of Question: Essay
   - Weightage: Percentage for the Question
   - Question: Question relevant to the context
   - No Answer Required

5. **Assertion-Reason:**
   - Type of Question: Assertion-Reason
   - Weightage: Percentage for the Question
   - Question:
     - Assertion: assertion
     - Reason: reason
   - Choice:
     a) Both Assertion and Reason are true, and the reason is the correct explanation.
     b) Both Assertion and Reason are true, but the reason is not the correct explanation.
     c) Assertion is true, but the reason is false.
     d) Both Assertion and Reason are false.
   - Answer: correct option

6. **Case Study:**
   - Type of Question: Case Study
   - Weightage: Percentage for the Question
   - Question: scenario or case
   - No Answer Required

**Examples for each type:**

1. **MCQs (Multiple Choice Questions):**
   - Type of Question: MCQ
   - Weightage: 10%
   - Question: What is the capital of France?
   - Choice:
     a) London
     b) Paris
     c) Rome
     d) Berlin
   - Answer: b) Paris

2. **True/False:**
   - Type of Question: True/False
   - Weightage: 5%
   - Question: The Earth is the third planet from the Sun.
   - Choice:
     - True
     - False
   - Answer: True

3. **Short Answer:**
   - Type of Question: Short Answer
   - Weightage: 10%
   - Question: Define the term "photosynthesis."
   - No Answer Required

4. **Essay:**
   - Type of Question: Essay
   - Weightage: 25%
   - Question: Discuss the impact of global warming on the polar ice caps.
   - No Answer Required

5. **Assertion-Reason:**
   - Type of Question: Assertion-Reason
   - Weightage: 15%
   - Question:
     - Assertion: Water boils at 100°C.
     - Reason: Water is composed of hydrogen and oxygen.
   - Choice:
     a) Both Assertion and Reason are true, and the reason is the correct explanation.
     b) Both Assertion and Reason are true, but the reason is not the correct explanation.
     c) Assertion is true, but the reason is false.
     d) Both Assertion and Reason are false.
   - Answer: c) Assertion is true, but the reason is false.

6. **Case Study:**
   - Type of Question: Case Study
   - Weightage: 35%
   - Question: A company is facing a data breach due to inadequate cybersecurity measures. Propose two solutions to improve their security.
   - No Answer Required

[/INST]
"""

answer_template = """
<s>[INST]
You are an assessment helper tasked with solving questions step by step. Below is a question, its type, and other related information. Your goal is to provide a detailed solution, explaining each step clearly.
You can get context from
context: {context}

Question Information:

Type of Question: {type}
Question: {question}
Answer Provided: {answer}
Choices: {choices}
Weightage: {weightage}
Provide a step-by-step solution for the question, ensuring that each step is clear and leads logically to the answer.
[/INST]
"""

score_answer_template = """
<s>[INST]
You are an expert grader. Your task is to evaluate a student's answer based on the given question, question type, and total possible score. Score the answer and provide constructive feedback.

If the student's answer is correct or good, explain why it is good and highlight its strengths. If the answer is incorrect or needs improvement, give a helpful and encouraging tone in your feedback, explaining what can be improved.

You can get context from
context: {context}

Inputs:

Question: {question}
Question Type: {question_type}
Student's Answer: {answer}
Total Possible Score: {total_score}
Please output:

Score: (based on a scale of 0 to total_score)
Feedback:
If the answer is good, explain why it is good.
If the answer is not good, explain what can be improved in a supportive and encouraging manner.

Example:

Question: What are the properties of a Red-Black Tree?
Question Type: Short Answer
Student's Answer: "A Red-Black Tree is a binary tree where each node is either red or black, and every path from the root to a leaf contains the same number of black nodes."
Total Possible Score: 10
Output:

Score: 7
Feedback:
Your answer is a good start! You have correctly identified that Red-Black Trees use red and black nodes, and you've mentioned the important property of having the same number of black nodes on all paths. However, to improve, make sure to also include the rules about node colors and rotations during insertions and deletions to maintain balance. Keep up the great work! You're on the right track.
[/INST]
"""

feedback_generator_template = """
<s>[INST]
You are a feedback generator assistant tasked with writing a summary feedback in a motivating tone. The feedback should assess the student's strengths and areas for improvement, based on their performance in the assessment. Additionally, highlight the skills acquired by the student as the Assessment Outcomes.

context: {context}

Data Provided:
Assessment Name: {assessment_name}
Total Score: {total_score}
Score Obtained: {score_obtained}
Assessment Difficulty: {assessment_difficulty}
Assessment Outcomes (Skills Acquired): {assessment_outcomes}

Questions:
{questions_data}

Each question will have its corresponding answer, the score obtained for that question, and the total possible score.

Requirements:
Tone: Use a motivating tone to encourage the student.
Strengths and Areas for Improvement: Based on the score obtained and the answers provided, identify areas where the student demonstrated strength and areas that need improvement.
Skills Acquired (Assessment Outcomes): Highlight the skills the student has developed or improved upon as a result of the assessment.
Assessment Summary: Provide an overview of the student’s overall performance, taking into account the difficulty level and skills acquired.

Follow the exact Output Structure

Feedback:
Acknowledge the student's effort and performance in the assessment.

Strengths:
Highlight the areas where the student performed exceptionally well, based on the answers provided.

Areas for Improvement:
Identify areas where the student can improve. Offer constructive advice while maintaining a positive tone.

Skills Acquired (Assessment Outcomes):
List the key skills the student has acquired or improved upon through this assessment.

Conclusion:
End with a motivating statement encouraging further learning and growth.

Example

Feedback:
"Great job on completing the Red-Black Tree Operations Assessment! Your determination and effort truly shine through in your performance. You’ve tackled a challenging topic, and your hard work is evident in the results."

Strengths:
"You displayed an excellent understanding of tree rotations and recoloring in this assessment. In Question 2, you demonstrated full comprehension of how to balance Red-Black Trees after insertions, earning top marks for that section. This shows a strong grasp of Red-Black Tree structure and properties, which is a critical skill for advanced tree operations."

Areas for Improvement:
"While your overall performance was impressive, there are a few areas where improvement is possible. In Question 4, handling edge cases during node insertions could be refined, particularly when dealing with recoloring scenarios. With a bit more practice on edge cases, your understanding will deepen even further, making you even more proficient in these operations."

Skills Acquired (Assessment Outcomes):
"Through this assessment, you’ve acquired key skills that will serve you well in more advanced topics:
- Mastery of Red-Black Tree properties, including balance and height management.
- Proficiency in performing tree rotations to maintain the Red-Black Tree constraints.
- Improved problem-solving skills in analyzing and executing tree insertions and adjustments."

Conclusion:
"Overall, you did an outstanding job! Your understanding of Red-Black Trees is solid, and with a bit more focus on edge case scenarios, you’ll have mastery over these topics in no time. Keep up the great work, and continue building on your strengths!"

Ensure this structure of feedback is clear, actionable, and encouraging, while helping the student recognize both their strengths and areas for development.
[/INST]
"""

assessment_properties_template = """
<s>[INST]

You are an intelligent assistant tasked with analyzing a given assessment. Your goal is to name the assessment, determine its difficulty level, and list the skills a user will gain upon completing it. Consider the context of the assessment questions provided and the expected knowledge to successfully complete them.

Task:
Assessment Name: Based on the content and focus of the assessment, give it a clear and appropriate name.
Difficulty Level: Determine the difficulty level of the assessment from ("Beginner," "Intermediate," "Advanced") based on the complexity of the questions and the depth of knowledge required.
Assessment Outcomes (Skills Acquired): List the specific skills and knowledge a user would gain by successfully completing the assessment.
Data Provided:
Context: {context} (If available, provide additional details such as the subject or knowledge domain)
Assessment Questions: {assessment_questions}

Example Structure:
Assessment Name: Provide a descriptive and relevant name for the assessment.
Difficulty Level: Determine and state whether the assessment is "Beginner," "Intermediate," or "Advanced."
Skills Acquired (Assessment Outcomes):
Skill 1: [Description of the skill]
Skill 2: [Description of the skill]
Skill 3: [Description of the skill]
(Continue as necessary)
Requirements:
Analyze the assessment holistically, considering the complexity and nature of the questions.
Provide a clear, concise, and informative name for the assessment.
Clearly describe the skills the user would acquire.
[/INST]"""