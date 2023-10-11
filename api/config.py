from urllib import parse

TOKEN = 'MTE2MTM3NDIyOTA5OTQ1NDYxNA.GDtB5v.axSuCRjho8YazKr0mt8GjQTjGG-qnd0pkhRPS4'
CLIENT_SECRET = 'XsMEKnlx1NbgoN4w1q-6uWUBHSbo4lxg'
REDIRECT_URL = "http://localhost:2020/oauth/callback"
OAUTH_URL = "https://discord.com/api/oauth2/authorize?client_id=1161374229099454614&redirect_uri="+parse.quote(REDIRECT_URL)+"&response_type=code&scope=identify"
