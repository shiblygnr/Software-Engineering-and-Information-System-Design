from flask import request, Flask
import requests
app = Flask(__name__)

def main():
    email = input("Email: ")
    res = requests.get("localhost:5000/api/enrolled/shiblygnr@gmail.com", params={"email": email})
    print(res)

if __name__ == "__main__":
    main()
