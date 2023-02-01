# client.py
import os
import requests
import sys

# First commandline argument is domain name
domain=sys.argv[1]

# Second commandline argument is port number
port=sys.argv[2]

def get_secret_message():
    response = requests.get("https://"+domain+":"+port, verify="ca-public-key.pem")
    print(f"The secret message is {response.text}")
    print(response.headers)

if __name__ == "__main__":
    get_secret_message()