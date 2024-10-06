import re
import genanki

def clean_questions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    skip_phrases = [
        r'Pass Your Certification With .* Guarantee',
        r'\d+ of \d+',
        r'Practice Test',
        r'Nutanix - NCP-MCA',
        r'References:',
        r'Section \d+ - .*',
        r'Objective \d+\.\d+ - .*',
        r'Module \d+ - .*',
        r'Lesson \d+\.\d+ - .*',
        r'\| Nutanix Community'
    ]

    # Compile regex patterns for efficiency
    skip_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in skip_phrases]

    question_block = []
    questions = []
    for line in lines:
        line = line.strip()

        # Skip empty lines and lines that match skip patterns
        if not line or any(pattern.search(line) for pattern in skip_patterns):
            continue

        # Detect the start of a new question
        if re.match(r'Question #:\d+', line):
            if question_block:
                questions.append('\n'.join(question_block))
                question_block = []
        question_block.append(line)

    # Add the last question block if any
    if question_block:
        questions.append('\n'.join(question_block))

    # Write cleaned questions to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for question in questions:
            f.write(question + '\n\n' + '-'*80 + '\n\n')

def create_anki_deck(output_file, anki_deck_file):
    import genanki

    # Read the output file
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content into question blocks using the separator
    question_blocks = content.strip().split('\n\n' + '-'*80 + '\n\n')

    # Define the Anki model
    my_model = genanki.Model(
        model_id=1607392319,
        name='Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    # Create a new Anki deck
    my_deck = genanki.Deck(
        deck_id=2059400110,
        name='Nutanix NCP-MCA')

    # Process each question block
    for block in question_blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue

        # Initialize variables
        question_num = ''
        question_text = ''
        choices = []
        answer = ''
        explanation = ''

        i = 0
        # Extract question number
        if re.match(r'Question #:\d+', lines[i]):
            question_num = lines[i]
            i += 1

        # Extract question text
        while i < len(lines) and not re.match(r'[A-D]\.', lines[i]):
            question_text += lines[i] + ' '
            i += 1

        # Extract choices
        while i < len(lines) and re.match(r'[A-D]\.', lines[i]):
            choices.append(lines[i])
            i += 1

        # Extract answer
        while i < len(lines):
            if lines[i].startswith('Answer:'):
                answer_line = lines[i]
                answer = lines[i].replace('Answer:', '').strip()
                i += 1
                break
            i += 1

        # Extract explanation
        explanation_lines = []
        while i < len(lines):
            explanation_lines.append(lines[i])
            i += 1
        explanation = ' '.join(explanation_lines)

        # Construct the question and answer fields
        # For the question field, include question text and choices
        question_field = f"{question_text.strip()}<br><br>{'<br>'.join(choices)}"
        # For the answer field, include the correct answer and the explanation
        answer_field = f"Answer: {answer}<br><br>{explanation.strip()}"

        # Create a new note
        note = genanki.Note(
            model=my_model,
            fields=[question_field, answer_field]
        )
        # Add the note to the deck
        my_deck.add_note(note)

    # Generate the .apkg file
    genanki.Package(my_deck).write_to_file(anki_deck_file)
    print(f"Anki deck created: {anki_deck_file}")

if __name__ == '__main__':
    input_file = 'Nutanix-NCP-MCA.txt'   # Replace with your input file name
    output_file = 'output.txt'           # Replace with your desired output file name
    anki_deck_file = 'Nutanix_NCP-MCA.apkg'  # Desired Anki deck file name

    clean_questions(input_file, output_file)
    create_anki_deck(output_file, anki_deck_file)
