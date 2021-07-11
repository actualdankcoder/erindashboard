from quart import Quart, redirect, url_for, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv() 
import dankbindings
app = Quart(__name__)

app.secret_key = os.getenv("SECRETKEY").encode("utf-8")

OAuthBridge=dankbindings.OAuth()
@app.before_serving
async def set_client():
    await OAuthBridge.create_client()
@app.route("/login/")
async def login():
    return redirect(OAuthBridge.discord_login_url)

@app.route("/callback/")
async def callback():
    code=request.args.get("code")
    tok=await OAuthBridge.getaccesstoken(code)
    print(tok)
    user=await OAuthBridge.getuser(tok["access_token"])
    return f"""
    <img src='{user.avatar_url()}'/>
    <br/>
    {user.name}#{user.discriminator}
    
    """
if __name__ == "__main__":
    app.run()
