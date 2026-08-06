from app.services.llm import generate_answer


answer = generate_answer(

    question=
    "How many annual leave days do employees receive?",


    context=
    """
Employees receive 18 days annual leave per year.
Leave applications must be approved by managers.
"""

)


print(answer)