"""One-time sign-in for yt_upload.py. Run it on your own computer, not in the cloud.

    pip install google-auth-oauthlib
    python yt_auth.py client_secret.json

A browser opens. Sign in with the Google account that owns the YouTube channel. Google warns
"Google hasn't verified this app" because the app is yours: choose Advanced, then Go to (your app),
then Continue. The script then prints three values. Add each one in GitHub under the repo's
Settings > Secrets and variables > Actions > New repository secret, using these names:
YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Keep them private and don't commit them.
"""
import json, sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
CHANNEL_ID = "UCyF8bKnMvQV_AzTCPJDxCGw"

path = sys.argv[1] if len(sys.argv) > 1 else "client_secret.json"
flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
if not creds.refresh_token:
    sys.exit("Google sent no refresh token. Remove the app's access at myaccount.google.com/permissions and run this again.")

from googleapiclient.discovery import build
me = build("youtube", "v3", credentials=creds, cache_discovery=False).channels().list(part="snippet", mine=True).execute()
items = me.get("items", [])
name, cid = (items[0]["snippet"]["title"], items[0]["id"]) if items else ("(no channel)", "")
print(f"\nSigned in to channel: {name} ({cid})")
if cid != CHANNEL_ID:
    print(f"WARNING: that's not Myles AI stories ({CHANNEL_ID}). Run again and pick the right account or brand channel.")

client = json.load(open(path, encoding="utf-8"))
client = client.get("installed") or client.get("web")
print("\nAdd these three GitHub secrets (copy each value exactly):\n")
print("YT_CLIENT_ID     =", client["client_id"])
print("YT_CLIENT_SECRET =", client["client_secret"])
print("YT_REFRESH_TOKEN =", creds.refresh_token)
