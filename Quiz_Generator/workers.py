'''from PyPDF2 import PdfFileReader'''
from question_generation_main import QuestionGeneration

from gensim.models import Word2Vec

import pdfplumber

def pdf2text(file_path: str, file_exten: str) -> str:
    """ Converts a given file to text content """

    _content = ''

    # Identify file type and get its contents
    if file_exten == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                _content += page.extract_text()
            print('PDF operation done!')

    elif file_exten == 'txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
            _content = txt_file.read()
            print('TXT operation done!')

    return _content


def txt2questions(doc: str, n=5, o=4) -> dict:
    """ Get all questions and options """

    qGen = QuestionGeneration(n, o)
    q = qGen.generate_questions_dict(doc)
    for i in range(len(q)):
        temp = []
        for j in range(len(q[i + 1]['options'])):
            temp.append(q[i + 1]['options'][j + 1])
        # print(temp)
        q[i + 1]['options'] = temp
    return q

