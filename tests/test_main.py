import unittest
from unittest.mock import patch

from main import Poem, build_message, fetch_poem


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


class TestBuildMessage(unittest.TestCase):
    def test_headers_and_body(self):
        poem = Poem("A Title", "An Author", "4", "one\ntwo\n")
        msg = build_message(poem, "from@x", "to@y")

        self.assertEqual(msg["Subject"], "Your Daily Poem (4 lines)")
        self.assertEqual(msg["From"], "from@x")
        self.assertEqual(msg["To"], "to@y")
        self.assertIn("A Title", msg.get_payload())
        self.assertIn("An Author", msg.get_payload())
        self.assertIn("one\ntwo", msg.get_payload())


PAYLOAD = [
    {
        "title": "Sonnet",
        "author": "Anon",
        "linecount": "2",
        "lines": ["first line", "second line"],
    }
]


class TestFetchPoem(unittest.TestCase):
    """PoetryDB is stubbed: the test covers the shape this code expects from it,
    not the service being up."""

    def test_fields_are_extracted_and_lines_joined(self):
        with patch("main.requests.get", return_value=FakeResponse(PAYLOAD)):
            title, author, line_count, lines = fetch_poem()

        self.assertEqual(title, "Sonnet")
        self.assertEqual(author, "Anon")
        self.assertEqual(line_count, "2")
        self.assertEqual(lines, "first line\nsecond line\n")
