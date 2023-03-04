import base64
from urlextract import URLExtract


def parse(msg) -> str:
    headers = msg["payload"]["headers"]

    # Get relevant headers
    for header in headers:
        name, value = header["name"], header["value"]
        if name == "From":
            from_header = value
        elif name == "To":
            to_header = value
        elif name == "Date":
            date_header = value

    # Get message (in utf-8 ascii text)
    parts = msg["payload"]["parts"]
    text_base64 = ""
    for part in parts:
        if part["mimeType"] == "text/plain":
            text_base64 += part["body"]["data"]
    plain_text = base64.urlsafe_b64decode(text_base64).decode("utf-8")
    plain_text = plain_text.replace("\r", " ")

    # Get urls in plain_text
    extractor = URLExtract()
    urls = extractor.find_urls(plain_text)

    return (from_header, to_header, date_header, plain_text, urls)
