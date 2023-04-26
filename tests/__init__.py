import unittest
import requests

from main import *

class TestFoo(unittest.TestCase):
    def test_is_up(self):
        # how should this work? 
        # discord fetches a specific URL
        # it should return the correspondingly-formatted html
        # self.assertIn()
        assert requests.get("https://psky.app/").status_code == 200
        assert requests.get("https://staging.psky.app/").status_code == 200
    
    def test_url_from_kawarimidoll(self):
        url_with_did = "https://bsky.app/profile/did:plc:okalufxun5rpqzdrwf5bpu3d/post/3juagfzruqs2u"
        generate_html(url_with_did)
        # fails if error