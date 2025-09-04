import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

## Meus testes

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)
    
def test_create_multiple_choices():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    assert choice1.id != choice2.id

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_remove_choice():
    question = Question(title='q1')
    
    choice = question.add_choice('a', False)

    question.remove_choice_by_id(choice.id)

    assert len(question.choices) == 0

def test_remove_multiple_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', False)
    
    question.remove_all_choices()

    assert len(question.choices) == 0

def test_remove_invalid_choice():
    question = Question(title='q1')
    choice = question.add_choice('a', True)
    with pytest.raises(Exception):
        question.remove_choice_by_id(choice.id+1)

def test_set_correct_choice():
    question = Question(title='q1')
    
    choice = question.add_choice('a', False)
    
    question.set_correct_choices([choice.id])

    assert choice.is_correct

def test_set_multiple_correct_choices():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    
    question.set_correct_choices([choice1.id, choice2.id])

    assert choice1.is_correct
    assert choice2.is_correct

def test_set_correct_invalid_choice():
    question = Question(title='q1')
    choice = question.add_choice('a', True)
    with pytest.raises(Exception):
        question.set_correct_choices([choice.id+1])

def test_correct_more_than_max_selected_choices():
    question = Question(title='q1', max_selections = 1)
    choice1 = question.add_choice("a", True)
    choice2 = question.add_choice("b", True)
    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id])

@pytest.fixture
def question_with_choices():
    q = Question(title="Pergunta de teste", points=10, max_selections=2)
    q.add_choice("a", is_correct=True)
    q.add_choice("b", is_correct=False)
    q.add_choice("c", is_correct=True)
    return q

def test_fixture_creates_question_with_three_choices(question_with_choices):
    q = question_with_choices
    assert len(q.choices) == 3
    assert q.title == "Pergunta de teste"
    correct_choices = [c for c in q.choices if c.is_correct]
    assert len(correct_choices) == 2

def test_remove_choice_with_fixture(question_with_choices):
    q = question_with_choices
    q.remove
    selected_ids = [q.choices[0].id, q.choices[1].id]  # 1 correta, 1 incorreta
    correct_selected = q.correct_selected_choices(selected_ids)
    assert correct_selected == [q.choices[0].id]