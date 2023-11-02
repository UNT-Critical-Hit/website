from flask import Flask, render_template, request, session, redirect
from firebase_admin import credentials, firestore, initialize_app
from _utils.officers import parse_data
from zenora import APIClient
import zenora.exceptions
from _utils.config import TOKEN, CLIENT_SECRET
from _utils.discord import get_campaigns, get_campaign, get_user
from _utils.form import submit_player, submit_dm, send_new_campaign, send_new_application
from _utils.db import logged_in, submit_report
from _utils.messages import get_apply_message, get_create_message
from urllib import parse
from markupsafe import Markup

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
fs_app = initialize_app(cred)
db = firestore.client()

def get_current_user():
    if 'token' in session:
        try:
            bearer_client = APIClient(session.get('token'), bearer=True)
        except zenora.exceptions.BadTokenError:
            submit_report(db, "get_current_user", "zenora.exceptions.BadTokenError: Invalid token has been passed")
            return False, render_template('message.html', current_user=None, header="Oh no!", message="Your token has expired. Please log in again.")
        user = bearer_client.users.get_current_user()
        logged_in(user.id, db)
        return True, user
    else:
        return True, None

# PAGES
def page(template, kargs = {}): # used to not have to include all of the default parameters
    res, current_user = get_current_user()
    if not res:
        return current_user
    return render_template(template, current_user=current_user, **kargs)

@app.route('/')
def page_index():
    return page('home.html')

@app.route("/login/")
def page_login():
    redirect_uri = request.base_url.replace('login/','oauth/callback')
    oauth_url = "https://discord.com/api/oauth2/authorize?client_id=1161374229099454614&redirect_uri="+parse.quote(redirect_uri)+"&response_type=code&scope=identify%20guilds%20guilds.members.read"
    return redirect(oauth_url)

@app.route("/logout/")
def page_logout():
    session.clear()
    return page_index()
    
@app.route("/message/")
def page_message(message = "", header = "Oh no!"):
    return page('message.html', {'header': header, 'message': Markup(message)})

@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    redirect_uri = request.base_url
    access_token = client.oauth.get_access_token(code, redirect_uri).access_token
    
    session['token'] = access_token
    if 'url' in session:
        return redirect(session['url'])

    return redirect("/")

@app.route("/campaigns/")
def page_campaigns():
    res, current_user = get_current_user()
    if not res:
        return current_user
    campaigns, error = get_campaigns(db, current_user)
    if not campaigns:
        return page_message(error)

    return page('campaigns.html', {'campaigns':campaigns})

@app.route("/apply/<campaign_id>")
def page_apply(campaign_id):
    res, current_user = get_current_user()
    if not res:
        return current_user
    if not current_user:
        session['url'] = "/apply/" + str(campaign_id)
        return redirect('/login/')
    user, error = get_user(current_user.id, db, current_user)
    if not user:
        return page_message(error)
    reason = user.can_join()
    if not reason:
        campaign, error = get_campaign(campaign_id, db, current_user)
        if not campaign:
            return page_message(error)
        return page('apply.html', {'campaign':campaign})
    else:
        return page_message(message = "You don't have permission to perform this action. " + reason)
    
@app.route("/apply/<campaign_id>", methods=["POST"])
def post_apply(campaign_id):
    res, current_user = get_current_user()
    if not res:
        return current_user
    if not current_user:
        session['url'] = "/apply/" + str(campaign_id)
        return redirect('/login/')
    user, error = get_user(current_user.id, db, current_user)
    if not user:
        return page_message(error)
    reason = user.can_join()
    if not reason:
        campaign, error = get_campaign(campaign_id, db, current_user)
        if not campaign:
            return page_message(error)
        if not send_new_application(request.form, user, campaign, db):
            return page_message(message = "An unknown error occurred while submitting your application.")
        submit_player(request.form, user, campaign, db)
        header, message = get_apply_message(campaign)
        return page_message(message = message, header = header)
    else:
        return page_message(message = "You don't have permission to perform this action. " + reason)
    
@app.route("/create/")
def page_create():
    res, current_user = get_current_user()
    if not res:
        return current_user
    if not current_user:
        session['url'] = "/create/"
        return redirect('/login/')
    user, error = get_user(current_user.id, db, current_user)
    if not user:
        return page_message(error)
    reason = user.can_create(db)
    if not reason:
        return page('create.html')
    else:
        return page_message(message = "You don't have permission to perform this action. " + reason)
    
@app.route("/create/", methods=["POST"])
def post_create():
    res, current_user = get_current_user()
    if not res:
        return current_user
    if not current_user:
        session['url'] = "/create/"
        return redirect('/login/')
    user, error = get_user(current_user.id, db, current_user)
    if not user:
        return page_message(error)
    reason = user.can_create(db)
    if not reason:
        if not send_new_campaign(request.form, user, db):
            return page_message(message = "An error has occurred while submitting your application.")
        submit_dm(request.form, user, db)
        header, message = get_create_message()
        return page_message(header = header, message = message)
    else:
        return page_message(message = "You don't have permission to perform this action. " + reason)

@app.route('/about/')
def page_about():
    return page('about.html')

@app.route('/officers/')
def page_officers():
    f = open('officers.txt')
    data = f.read()
    f.close()
    officers = parse_data(data)
    return page('officers.html', {'officers':officers})

# TESTING
#'''
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 2020))
    app.run(debug=True, threaded=False, host='0.0.0.0', port=port)
#'''
