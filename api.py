from quart import Quart, redirect, url_for, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv() 
import dankbindings
app = Quart(__name__)

app.secret_key = os.getenv("SECRETKEY").encode("utf-8")

OAuthBridge=dankbindings.OAuth()

@app.route("/login/")
async def login():
    return redirect(OAuthBridge.discord_login_url)

@app.route("/callback/")
async def callback():
    code=request.args.get("code")
    tok=OAuthBridge.getaccesstoken(code)
    return jsonify(OAuthBridge.getuser(tok["access_token"]))
if __name__ == "__main__":
    app.run()
