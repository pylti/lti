from requests import Request
from .launch_params import LaunchParams
from .tool_base import ToolBase
import requests
import json
from requests_oauthlib import OAuth1
from requests_oauthlib.oauth1_auth import SIGNATURE_TYPE_AUTH_HEADER

class ToolProxy(ToolBase):
    def load_tc_profile(self):
        response = requests.get(self.launch_params['tc_profile_url'])

        self.tc_profile = json.loads(response.text)

    @property
    def tool_consumer_profile_url(self):
        return self.launch_params['tc_profile_url']

    def find_registration_url(self):
        for service in self.tc_profile["service_offered"]:
            if "application/vnd.ims.lti.v2.toolproxy+json" in service["format"] and "POST" in service["action"]:
                return service["endpoint"]

    def register_proxy(self, profile):
        register_url = self.find_registration_url()

        r = Request("POST", register_url, data=profile, headers={'Content-Type':'application/vnd.ims.lis.v2.result+json'}).prepare()
        sign = OAuth1(self.launch_params['reg_key'], self.launch_params['reg_password'],
                      signature_type=SIGNATURE_TYPE_AUTH_HEADER)
        return sign(r)


