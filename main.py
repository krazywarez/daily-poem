# Fetch a random poem from PoetryDB and mail it.
import smtplib
from email.mime.text import MIMEText
from typing import NamedTuple

import requests

POETRY_URL = "https://poetrydb.org/random"
SMTP_SERVER = "localhost"

# Fill these in before running.
SENDER_EMAIL = ""
RECIPIENT_EMAILS = ""


class Poem(NamedTuple):
    title: str
    author: str
    line_count: str
    lines: str


def fetch_poem(url=POETRY_URL):
    """Return a random poem."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    json_data = resp.json()
    poem = json_data[0]
    lines = ""
    for line in poem["lines"]:
        lines = lines + line + "\n"
    return Poem(poem["title"], poem["author"], poem["linecount"], lines)


def build_message(poem, sender, recipient):
    """Return a plaintext MIMEText message for one poem."""
    msg = MIMEText(poem.title + "\n" + poem.author + "\n\n" + poem.lines)
    msg["Subject"] = "Your Daily Poem (" + poem.line_count + " lines)"
    msg["From"] = sender
    msg["To"] = recipient
    return msg


def main():
    msg = build_message(fetch_poem(), SENDER_EMAIL, RECIPIENT_EMAILS)

    # Send via the local SMTP server, without the envelope header.
    s = smtplib.SMTP(SMTP_SERVER)
    s.sendmail(SENDER_EMAIL, [RECIPIENT_EMAILS], msg.as_string())
    s.quit()


if __name__ == "__main__":
    main()
