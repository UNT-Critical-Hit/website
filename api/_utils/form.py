import requests

def submit_form():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSfOJ8nRBveW8Y2U0rMDczUe6iHAJc9-644pcfn4bBKzc7-UXw/formResponse"
    data = {
    "entry.1483793162": "Hii",
    "entry.1659304556": "this"
    }
    r = requests.post(url, params = data)
    print("\n\nresponse:",r,"\n\n")