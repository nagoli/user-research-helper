from typing import List, Tuple
import os
import tempfile

def parse_questions(file_path: str) -> List[Tuple[str, str]]:
    """
    Parse the questions file and return a list of tuples (id, question).
    Questions must be separated by empty lines and non-null.
    IDs are automatically generated from Q0 to Qn.
    
    Args:
        file_path: Path to the questions.txt file
    
    Returns:
        List[Tuple[str, str]]: List of tuples (id, question)
    """
    questions = []
    current_question_lines = []
    question_counter = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # If empty line and we have collected question lines
            if not line and current_question_lines:
                # Join the lines and clean up the question text
                question_text = ' '.join(current_question_lines).strip()
                if question_text:  # Only add non-empty questions
                    questions.append((f"Q{question_counter}", question_text))
                    question_counter += 1
                current_question_lines = []
            
            # If non-empty line, add to current question
            elif line:
                # If line starts with bullet point, format it properly
                if line.startswith('•'):
                    line = '- ' + line.lstrip('•').strip()
                current_question_lines.append(line)
    
    # Handle the last question if exists
    if current_question_lines:
        question_text = ' '.join(current_question_lines).strip()
        if question_text:  # Only add non-empty questions
            questions.append((f"Q{question_counter}", question_text))
    
    return questions


def test_parse_questions():
    """Test the parse_questions function with various scenarios"""
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        # Test case 1: Basic questions separated by empty lines
        temp_file.write("""Question 1 text here

Question 2 text here

Question 3 with
multiple lines
of text

Question 4 with bullets:
• First bullet
• Second bullet
""")
        temp_file.flush()
        
        # Test basic parsing
        questions = parse_questions(temp_file.name)
        assert len(questions) == 4, f"Expected 4 questions, got {len(questions)}"
        assert questions[0] == ("Q0", "Question 1 text here"), "First question not parsed correctly"
        assert questions[1] == ("Q1", "Question 2 text here"), "Second question not parsed correctly"
        assert questions[2] == ("Q2", "Question 3 with multiple lines of text"), "Multi-line question not parsed correctly"
        assert questions[3][0] == "Q3", "Fourth question ID not correct"
        assert "- First bullet" in questions[3][1], "Bullet points not converted correctly"
        
        # Clean up
        temp_file.close()
        os.unlink(temp_file.name)
    
    # Test case 2: Edge cases
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        temp_file.write("""

Empty lines at start

Empty lines between


Question with empty lines

Last question without empty line at end""")
        temp_file.flush()
        
        questions = parse_questions(temp_file.name)
        assert len(questions) == 4, f"Expected 4 questions, got {len(questions)}"
        assert questions[0] == ("Q0", "Empty lines at start"), "First question with empty lines not parsed correctly"
        assert questions[-1] == ("Q3", "Last question without empty line at end"), "Last question not parsed correctly"
        
        # Clean up
        temp_file.close()
        os.unlink(temp_file.name)

if __name__ == "__main__":
    # Run tests
    test_parse_questions()
    print("All tests passed!")
    
    # Example usage with actual questions file
    if os.path.exists("data/questions.txt"):
        questions = parse_questions("data/questions.txt")
        print("\nParsed questions from questions.txt:")
        for qid, text in questions:
            print(f"\n{qid}:")
            print(text)
