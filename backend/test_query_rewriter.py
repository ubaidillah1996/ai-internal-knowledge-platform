from app.services.query_rewriter import rewrite_query


def test_rewrite_pronoun_reference():

    history = """
user: Who approves annual leave?
assistant: Managers approve annual leave applications.
"""

    result = rewrite_query(

        question="Who approves it?",

        history=history

    )

    assert result.startswith("Who")

    assert "annual leave" in result.lower()

    assert "approv" in result.lower()


def test_rewrite_role_reference():

    history = """
user: Who approves annual leave?
assistant: Managers approve annual leave applications.
"""

    result = rewrite_query(

        question="What about their role?",

        history=history

    )

    assert result.startswith("What")

    assert "role" in result.lower()

    assert "manager" in result.lower()

    assert "annual leave" in result.lower()


def test_no_rewrite_for_direct_question():

    question = "Who approves annual leave?"

    result = rewrite_query(

        question=question,

        history=""

    )

    assert result == question