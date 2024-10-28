# yourteamrepo/yourteamrepo/main_app.py
from flask import Flask, render_template
import requests
import json
import matplotlib.pyplot as plt
from google.colab import userdata

app = Flask(__name__)

@app.route('/')
def fetch_and_plot_github_events():
    token = userdata.get('ghtoken')
    url = 'https://api.github.com/events'
    headers = {'Authorization': 'Bearer ' + token}

    r = requests.get(url, headers=headers)
    print(r.status_code)

    if r.status_code == 200:
        r_json = json.loads(r.text)

        hooray_reactions = [event for event in r_json if event['type'] == 'WatchEvent' and event['payload']['action'] == 'started']

        hooray_count = len(hooray_reactions)
        print(f'Total "hooray" reactions: {hooray_count}')

        labels = ['Hooray', 'Other Events']
        sizes = [hooray_count, len(r_json) - hooray_count]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Distribution of "Hooray" Reactions')
        plt.savefig('static/plot.png')  # Save the plot as a static image
        plt.close()

        return render_template('index.html', plot_path='static/plot.png')
    else:
        return f'Error: {r.status_code}\n{r.text}'

if __name__ == '__main__':
    app.run(debug=True)

