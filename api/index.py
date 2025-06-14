from flask import Flask, render_template, request, session, redirect
from firebase_admin import credentials, firestore, initialize_app
from _utils.officers import parse_data
from zenora import APIClient
import zenora.exceptions
from _utils.discord import get_campaigns, get_campaign, get_user, get_campaigns_by_id, update_user
from _utils.form import submit_player, submit_dm, send_new_campaign, send_new_application
from _utils.db import logged_in, submit_report
from _utils.messages import get_apply_message, get_create_message
from urllib import parse
from markupsafe import Markup
from _utils.misc import get_campaign_by_id
from _utils.CampaignActionRequest import CampaignActionRequest

# env variables
# For testing purposes, you can set these variables in a testing.env file or directly in your environment
import os
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'testing.env'))
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
FIREBASE_CRED = {}
for key in ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id", 
            "auth_uri", "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url", 
            "universe_domain"]:
    FIREBASE_CRED[key] = os.environ.get("FIREBASE_" + key.upper())
TOKEN = os.environ.get('TOKEN')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
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
        except Exception as ex:
            submit_report(db, "get_current_user", "zenora: {0}".format(str(ex)))
            return False, render_template('message.html', current_user=None, header="Oh no!", message="An unknown error occured on login.")
        current_user = bearer_client.users.get_current_user()
        logged_in(current_user.id, db)
        return True, current_user
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

@app.route('/user_profile/')
def page_user_profile():
    if 'username' in session:
        res, current_user = get_current_user()
        if not res:
            session['url'] = '/user_profile/'
            redirect('/login/')
        user, error = get_user(current_user.id, db, current_user)
        if error:
            return page_message(error)
        return page('user_profile.html', {'user': user})
    else:
        session['url'] = '/user_profile/'
        return redirect('/login/')

@app.route('/user_dashboard/')
def page_user_dashboard():
    if 'username' in session:
        res, current_user = get_current_user()
        if not res:
            session['url'] = '/user_dashboard/'
            redirect('/login/')
        user, error = get_user(current_user.id, db, current_user)
        if not user:
            return page_message(error)
        campaigns_player, error = get_campaigns_by_id(db, current_user, user.campaigns_player)
        if error:
            return page_message(error)
        campaigns_dm, error = get_campaigns_by_id(db, current_user, user.campaigns_dm)
        if error:
            return page_message(error)
        return page('user_dashboard.html', {'user_campaigns': campaigns_player, 'dm_campaigns': campaigns_dm})
    else:
        session['url'] = '/user_dashboard/'
        return redirect('/login/')

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
    print(get_current_user())
    res, current_user = get_current_user()
    if res:
        session['username'] = current_user.username
    if 'url' in session:
        return redirect(session['url'])

    return redirect("/")

@app.route("/campaigns/")
def page_campaigns():
    current_user = None
    if 'username' in session:
        res, current_user = get_current_user()
        if not res:
            session['url'] = '/user_profile/'
            redirect('/login/')
        user, error = get_user(current_user.id, db, current_user)
        if error:
            return page_message(error)
    else:
        user = None
    campaigns, error = get_campaigns(db, current_user)
    if not campaigns:
        return page_message(error)

    return page('campaigns.html', {'campaigns':campaigns, 'user': user})

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
    
    # check if profile is filled out
    if not user.first_name:
        return page('user_profile.html', {'user': user, 'message': 'Please fill out your user profile before applying for a campaign.'})

    reason = user.can_join()
    if not reason:
        campaign, error = get_campaign(campaign_id, db, current_user)
        if not campaign:
            return page_message(error)
        return page('apply.html', {'campaign':campaign, 'user': user})
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
    
    # check if profile is filled out
    if not user.first_name:
        return page('user_profile.html', {'user': user, 'message': 'Please fill out your user profile before creating a campaign.'})

    reason = user.can_create(db)
    if not reason:
        print(user)
        return page('create.html', {'user': user})
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

@app.route("/user_profile/", methods=["POST"])
def post_user_profile():
    if 'username' in session:
        res, current_user = get_current_user()
        if not res:
            session['url'] = '/user_profile/'
            redirect('/login/')
        user, error = get_user(current_user.id, db, current_user)
        if error:
            return page_message(error)
        
        # get info from submission
        submission = request.form
        user.id = current_user.id
        user.first_name = submission['name_first']
        user.last_name = submission['name_last']
        if submission['unt_student'] == "Yes":
            user.unt_student = True
            user.unt_email = submission['unt_email']
        else:
            user.unt_student = False
            user.unt_email = ""

        if update_user(user.id, db, user): # if successfully posted
            return page('user_profile.html', {'user': user, 'message': 'Your user profile has been updated.'})
        else:
            return page_message(message = "Something went wrong while trying to update your user profile.")
    else:
        session['url'] = '/user_profile/'
        return redirect('/login/')

@app.route('/about/')
def page_about():
    return page('about.html')

@app.route('/officers/')
def page_officers():
    f = open('officers.txt')
    data = f.read()
    f.close()
    officers = parse_data(data)
    return page('officers.html', {'officers': officers})

# TESTING
#'''
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 2020))
    app.run(debug=True, threaded=False, host='0.0.0.0', port=port)
#'''
