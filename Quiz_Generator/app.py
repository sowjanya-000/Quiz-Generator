import os
from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from werkzeug.utils import secure_filename
from workers import pdf2text, txt2questions



UPLOAD_FOLDER = './pdf/'

#initialize
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@ app.route('/')
def index():
    """ landing page """
    return render_template('index.html')


@ app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """upload and conversion of file + other stuff """

    UPLOAD_STATUS = False
    questions = dict()

    # make local directory to store uploaded file
    if not os.path.isdir('./pdf'):
        os.mkdir('./pdf')

    if request.method == 'POST':
        try:
            # Retrieve file from request
            uploaded_file = request.files['file']
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                secure_filename(
                    uploaded_file.filename))
            file_exten = uploaded_file.filename.rsplit('.', 1)[1].lower()

            # Save uploaded file
            uploaded_file.save(file_path)
            # get content of file
            uploaded_content = pdf2text(file_path, file_exten)
            questions = txt2questions(uploaded_content)

            # File upload + convert success
            if uploaded_content is not None:
                UPLOAD_STATUS = True
        except Exception as e:
            print(e)
    return render_template(
        'quiz.html',
        uploaded=UPLOAD_STATUS,
        questions=questions,
        size=len(questions))


@app.route('/result', methods=['POST', 'GET'])
def result():
    correct_q = 0
    for k, v in request.form.items():
        correct_q += 1
    return render_template('result.html', total=5, correct=correct_q)


if __name__ == "__main__":
    app.run(debug=True)



#"""future goals of this inspired project that was made- to use large pre trained models or train our own dataset and make it more efficient
# in generating quiz ... instead of mixing different techniques , implying Open API or implying neural network can be done """