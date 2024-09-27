prompt_for_question = {
    'MCQ' : '{number} MCQs (Multiple Choice Questions): These are questions where a user selects the correct answer from 4 provided options.',
    'True/False' : '{number} True/False: A statement is given, and the user chooses whether the statement is true or false.',
    'Short Answer' : '{number} Short Answer: These are brief responses, usually 1-2 sentences or a few words.',
    'Essay' : '{number} Essay: These questions require a detailed, in-depth response explaining or discussing a given topic',
    'Assertion-Reason' : '{number} Assertion-Reason: These questions consist of an assertion and a reason. The user must determine whether both are correct, and if the reason correctly explains the assertion.',
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