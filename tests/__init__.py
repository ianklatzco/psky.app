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
    
    def test_is_profile_url(self):
        url = "https://staging.bsky.app/profile/klatz.co"
        url2 = "https://staging.bsky.app/profile/klatz.co/"
        url3 = "https://staging.bsky.app/profile/klatz.co/post/lol"
        assert is_just_profile_url(url) == True
        assert is_just_profile_url(url2) == True
        assert is_just_profile_url(url3) == False
    
    def test_generate_profile_html(self):
        url = "https://staging.bsky.app/profile/klatz.co"
        generate_html(url)

    def test_quoteskeet(self):
        # quotebloot
        # https://github.com/ianklatzco/psky.app/issues/4
        # thanks steveklabnik!
        url = "https://psky.app/profile/did:plc:3danwc67lo7obz2fmdg6jxcr/post/3jup6ppmuef2g"
        ee = generate_html(url)
        print(ee)

        # first step: detect if it's a quotebloot
        is_quotebloot(url)
