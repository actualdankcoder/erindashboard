import requests
import os
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv() 

class OAuth:
    def __init__(self):
        self.client_id = os.getenv("CID")
        self.client_secret = os.getenv("CIS")
        self.scope = ["identify","guilds"]


        self.redirect_uri = "http://localhost:5000/callback"
        self.oauth_base="https://discord.com/api/oauth2"
        self.discord_login_url = self.generate_login_url()
        self.discord_token_url =self.oauth_base+"/token"
        self.discord_api_url = "https://discord.com/api"
        self.bot_invite_url = self.generate_bot_invite_url()

    def generate_login_url(self):
        return self.oauth_base+"/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(
        self.client_id, quote(self.redirect_uri), quote(" ".join(self.scope)))        

    def generate_bot_invite_url(self):
        return self.oauth_base+"/authorize?client_id={}&permissions=0&redirect_uri={}&scope=bot".format(
        self.client_id, quote(self.redirect_uri))    
    def getaccesstoken(self, code):
        data = {
            'client_id': self.client_id,
            'client_secret':  self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri':  self.redirect_uri,
            'scope': " ".join(self.scope)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token = requests.post(self.discord_token_url,
                              data=data, headers=headers)
        return token.json()


    def getuser(self, accesstoken):
        url = self.discord_api_url+"/users/@me"
        headers = {
            'Authorization': 'Bearer {}'.format(accesstoken)
        }
        user = requests.get(url, headers=headers)
        return user.json()


    def getuserguilds(self, accesstoken):
        url = self.discord_api_url+"/users/@me/guilds"
        headers = {
            'Authorization': 'Bearer {}'.format(accesstoken)
        }
        guilds = requests.get(url, headers=headers)
        return guilds.json()
