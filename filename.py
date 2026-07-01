import os
import git
from flask import Flask, render_template, request, redirect
from pyyoutube import Client
#from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

@app.route("/")
def home():
    url, state = client.get_authorize_url()
    return render_template("home.html", auth_url=url)

@app.route("/callback")
def callback():
    redirect_url = request.url
    access_token = client.generate_access_token(authorization_response=redirect_url)
    return render_template("callback.html", token=access_token)

@app.route("/rate", methods=["GET", "POST"])
def rate_video():
    if request.method == "POST":
        video_id = request.form.get("video_id")
        response = client.videos.rate(video_id, rating="like")
        rating = client.videos.get_rating(video_id=video_id)
        return render_template("rate.html", response=response, rating=rating)
    return render_template("rate_page.html")

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/CHANGE_TO_PYTHON_ANYWHERE_USERNAME/CHANGE_TO_GITHUB_REPO_NAME')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")