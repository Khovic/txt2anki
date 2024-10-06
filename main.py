import pypdf
import re

def extract_mcq(pdf_path, output_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(file)
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Split text into lines
                lines = text.split('\n')
                
                question_pattern = re.compile(r'^Question #:\d+')
                option_pattern = re.compile(r'^([A-D])\.$')
                answer_pattern = re.compile(r'^Answer:')
                explanation_pattern = re.compile(r'^Explanation')
                
                current_question = ""
                in_question = False
                current_option = None
                in_explanation = False
                
                for line in lines:
                    line = line.strip()
                    
                    # Skip irrelevant lines
                    if any(skip in line for skip in ["Pass Your Certification", "Practice Test", "Nutanix -"]):
                        continue
                    
                    if question_pattern.match(line):
                        # New question
                        if current_question:
                            output_file.write(current_question.strip() + '\n\n')
                        current_question = line + '\n'
                        in_question = True
                        current_option = None
                        in_explanation = False
                    elif option_match := option_pattern.match(line):
                        # Start of an option
                        if current_option:
                            current_question += current_option + '\n'
                        current_option = option_match.group(1) + '.'
                    elif current_option and line:
                        # Continuation of an option
                        current_option += ' ' + line
                    elif answer_pattern.match(line):
                        # Answer
                        if current_option:
                            current_question += current_option + '\n'
                            current_option = None
                        current_question += '\n' + line + '\n'
                    elif explanation_pattern.match(line):
                        # Start of explanation
                        if current_option:
                            current_question += current_option + '\n'
                            current_option = None
                        in_explanation = True
                        current_question += '\n' + line + '\n'
                    elif in_question:
                        # Continuation of question or explanation
                        current_question += line + '\n'
                
                # Write the last question
                if current_question:
                    if current_option:
                        current_question += current_option + '\n'
                    output_file.write(current_question.strip() + '\n\n')

    print(f"MCQs extracted and saved to {output_path}")

# Usage
pdf_path = 'input.pdf'
output_path = 'mcq_output.txt'
extract_mcq(pdf_path, output_path)