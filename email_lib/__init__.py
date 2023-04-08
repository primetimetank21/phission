# email: jhnwck2023@gmail.com
# pass:  password123EZ

# type: ignore
# Pylint disables (temp?)
# pylint: disable=no-member,broad-exception-caught,import-error

# Modules
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .get_email_message import parse


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_creds() -> Credentials:
    creds = None
    try:
        # The file token.json stores the user"s access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error with creds.refresh(Request()): {e}")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./email_lib/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w", encoding="utf-8") as token:
                token.write(creds.to_json())
    except Exception as e:
        print(f"Error: {e}")
        creds = None

    return creds


def build_gmail_service(creds: Credentials) -> build:
    return build("gmail", "v1", credentials=creds)


def get_all_messages() -> list:
    creds = get_creds()
    if not creds:
        print("Invalid credentials")
        return

    try:
        gmail_service = build_gmail_service(creds)

        results = gmail_service.users().messages().list(userId="me").execute()
        mail_list = results["messages"]
        msg_list = []

        for listing in mail_list:
            msg = (
                gmail_service.users()
                .messages()
                .get(userId="me", id=listing["id"], format="full")
                .execute()
            )

            (
                from_header,
                to_header,
                date_header,
                subject_header,
                plain_text,
                urls,
            ) = parse(msg)
            msg_dict = {
                "From": from_header,
                "To": to_header,
                "Date": date_header,
                "Subject": subject_header,
                "Plain_Text": plain_text,
                "URLs": urls,
            }

            msg_list.append(msg_dict)

    except HttpError as error:
        print(f"An error occurred: {error}")
        msg_list = []

    return msg_list


if __name__ == "__main__":
    get_all_messages()
