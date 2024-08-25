from flask import Flask, request, render_template
from transformers import pipeline
from bs4 import BeautifulSoup
import urllib.request

app = Flask(__name__)

# Initialize the question-answering pipeline
question_answer = pipeline("question-answering")


def get_website_text(url):
    html = urllib.request.urlopen(url)
    htmlParse = BeautifulSoup(html, 'html.parser')
    for para in htmlParse.find_all("p"):
        return para.get_text()


@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        url = request.form.get('url')
        question = request.form.get('question')

        # Get the context from the website
        context = get_website_text(url)

        if context and question:
            # Use the question-answering pipeline
            result = question_answer(question=question, context=context)
            answer = result['answer']

    return render_template('index.html', answer=answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
