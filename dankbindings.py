#import requests
import os
import discord
import aiohttp
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv() 

class OAuth:
    def __init__(self):
        # User Provided Data
        self.client_id = os.getenv("CID")
        self.client_secret = os.getenv("CIS")
        self.scope = ["identify","guilds"]

        # Generated Data
        self.redirect_uri = "http://localhost:5000/callback"
        self.oauth_base="https://discord.com/api/oauth2"
        self.discord_login_url = self.generate_login_url()
        self.discord_token_url =self.oauth_base+"/token"
        self.discord_api_url = "https://discord.com/api"
        self.bot_invite_url = self.generate_bot_invite_url()
        self.client=None
    async def create_client(self):
        self.client = aiohttp.ClientSession()
    def generate_login_url(self):
        # Generate a login url, used during authorization
        return self.oauth_base+"/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(
        self.client_id, quote(self.redirect_uri), quote(" ".join(self.scope)))        

    def generate_bot_invite_url(self):
        # Generate a bot invite url, used in the guild selection page
        return self.oauth_base+"/authorize?client_id={}&permissions=0&redirect_uri={}&scope=bot".format(
        self.client_id, quote(self.redirect_uri))    

    async def getaccesstoken(self, code):
        # Get a user access token required to make api calls with discord
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
        token = await self.client.post(self.discord_token_url,
                              data=data, headers=headers)
        return await token.json()
    async def refreshtoken(self, refresh_token):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = await self.client.post('%s/oauth2/token' % self.discord_api_url, data=data, headers=headers)
        return await r.json()

    async def getuser(self, accesstoken):
        # Fetch user using an access token
        url = self.discord_api_url+"/users/@me"
        headers = {
            'Authorization': 'Bearer {}'.format(accesstoken)
        }
        payload = await self.client.get(url, headers=headers)
        data=await payload.json()
        user=User(
            name=data["username"],
            userid=data["id"],
            discriminator=data["discriminator"],
            avatar=data["avatar"]
        )
        return user
    async def getuserguilds(self, accesstoken):
        # Fetch user guilds using an access token
        url = self.discord_api_url+"/users/@me/guilds"
        headers = {
            'Authorization': 'Bearer {}'.format(accesstoken)
        }
        payload = await self.client.get(url, headers=headers)
        data=await payload.json()
        guilds=[
            Guild(
                name=i["name"],
                guildid=i["id"],
                features=i["features"],
                icon=i["icon"],
                owner=i["owner"],
                permissions=i["permissions"]
            ) for i in data
        ]
        return guilds


# Abstract Classes
class User:
    def __init__(self, name, discriminator, userid, avatar):
        self.name=name
        self.discriminator=int(discriminator)
        self.id=int(userid)
        self.avatar_hash=avatar
    def __repr__(self):
        return f"{self.name}#{self.discriminator}"
    def __str__(self):
        return f"{self.name}#{self.discriminator}"
    def avatar_url(self, size=256):
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.png?size={size}"

class Guild:
    def __init__(self, name, guildid, features, icon, owner, permissions):
        self.name=name
        self.id=int(guildid)
        self.features=features
        self.icon_hash=icon
        self.is_owner=owner
        self.permissions=discord.Permissions(permissions=int(permissions))
    def __repr__(self):
        return f"{self.name}"
    def __str__(self):
        return f"{self.name}"
    def icon_url(self, size=256):
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon_hash}.png?size={size}"

class TokenSession:
    # planned to be an implementation of encrypted flask sessions 
    # but stored server side and they'll be used for
    # making calls to the discord API
    pass