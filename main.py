import re

def clean_questions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_lines = []
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

if __name__ == '__main__':
    input_file = 'Nutanix-NCP-MCA.txt'   # Replace with your input file name
    output_file = 'output.txt' # Replace with your desired output file name
    clean_questions(input_file, output_file)
