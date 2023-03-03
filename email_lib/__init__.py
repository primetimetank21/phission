# email: jhnwck2023@gmail.com
# pass:  password123EZ
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    creds = None
    # The file token.json stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./email_lib/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    try:
        gmail_service = build("gmail", "v1", credentials=creds)

        # pylint: disable=no-member
        results = gmail_service.users().messages().list(userId="me").execute()
        mail_list = results["messages"]
        for listing in mail_list:
            msg = (
                gmail_service.users()
                .messages()
                .get(userId="me", id=listing["id"], format="full")
                .execute()
            )
            if msg:
                with open(
                    f"example_email_{listing['id']}.json", "w", encoding="utf-8"
                ) as f:
                    json.dump(msg, f, indent=4)
            if msg["snippet"]:
                print(msg["snippet"])
            else:
                print(":/")
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
