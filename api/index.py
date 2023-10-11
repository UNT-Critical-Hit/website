#import requests
#print(requests.get("http://api.midnight.wtf:25713/campaigns\?auth\=1e071fa5-f022-44fc-b884-b5e36bc0c80a").content)

from flask import Flask, render_template, request, session, redirect
#from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from _utils.officers import parse_data
import sys
from zenora import APIClient
from config import TOKEN, CLIENT_SECRET, OAUTH_URL, REDIRECT_URL
from _utils.discord import get_campaigns, get_campaign
from _utils.form import submit_form

#submit_form()


# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)

def get_user():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        return bearer_client.users.get_current_user()
    else:
        return None

# PAGES
@app.route('/')
def page_index():
    return render_template('home.html', current_user=get_user())

@app.route("/login/")
def page_login():
    return redirect(OAUTH_URL)

@app.route("/logout/")
def page_logout():
    session.clear()
    return page_index()

@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, REDIRECT_URL).access_token
    
    session['token'] = access_token
    if 'url' in session:
        return redirect(session['url'])
    print(session)
    return redirect("/")

@app.route("/campaigns/")
def page_campaigns():
    campaigns = get_campaigns()
    return render_template('campaigns.html', campaigns=campaigns, current_user=get_user())

@app.route("/apply/<campaign_id>")
def page_apply(campaign_id):
    current_user = get_user()
    if not current_user:
        session['url'] = "/apply/" + str(campaign_id)
        return redirect('/login/')
    campaign = get_campaign(campaign_id)
    return render_template('apply.html', campaign=campaign, current_user=current_user)

@app.route('/about/')
def page_about():
    return render_template('about.html', current_user=get_user())

@app.route('/officers/')
def page_officers():
    f = open('officers.txt')
    data = f.read()
    f.close()
    officers = parse_data(data)
    return render_template('officers.html', officers=officers, current_user=get_user())

# TESTING
#'''
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 2020))
    app.run(debug=True, threaded=False, host='0.0.0.0', port=port)
#'''
