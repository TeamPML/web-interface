from flask import Flask, request, render_template
import github
import requests

from github_secrets import MY_TOKEN

app = Flask(__name__)

url = 'http://178.170.193.12:8501/v1/models/title_desc:predict'

g = github.Github(login_or_token=MY_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def run_app():
    if request.method == 'POST':
        link = request.form['link']
        splits = link.split('/')
        repository = g.get_repo(splits[3] + '/' + splits[4])
        issue = repository.get_issue(int(splits[6]))
        text = issue.title + issue.body
        params = {'instances': [text]}
        x = requests.post(url, json=params)
        prediction = x.json()['predictions'][0][0]
        return render_template('index.html', link=link, text=text, predictions=pred_logit(prediction))
    else:
        return render_template('index.html')


@app.route('/text', methods=['GET', 'POST'])
def predict_text():
    if request.method == 'POST':
        input_text = request.form['input_text']
        params = {'instances': [input_text]}
        x = requests.post(url, json=params)
        prediction = x.json()['predictions'][0][0]
        return render_template('text.html', input_text=input_text, predictions=pred_logit(prediction))
    else:
        return render_template('text.html')




def pred_logit(pred):
    wordy = "security-related" if pred > 0 else "not security-related"
    return f"{wordy};\n logit: {pred}"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
	
