import requests
from requests.auth import HTTPBasicAuth
import json

def fetch_json(
    url: str,
    username: str = None,
    password: str = None,
    timeout_sec: int = 10
) -> dict:
    """
    Makes a GET request to a URL and returns:
    {
        "success": True/False,
        "status_code": 200,
        "data": {...}   # JSON if available
        "error": "error message"
    }
    """

    auth = HTTPBasicAuth(username, password) if username and password else None

    try:
        response = requests.get(url, auth=auth, timeout=timeout_sec)
        # print(f"{response.status_code} is the status code ")
        

        # Handle different status codes
        if response.status_code == 200:
            try:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "headers":response.headers,
                    "data": response.json(),
                    "error": None
                }
            except ValueError:  # JSON parsing failed
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "data": None,
                    "error": "Invalid JSON response"
                }

        elif response.status_code == 401:
            return {"success": False, "status_code": 401, "error": "Unauthorized access"}
        elif response.status_code == 404:
            return {"success": False, "status_code": 404, "error": "Resource not found"}
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Unexpected status code received"
            }

    except requests.Timeout:
        return {"success": False, "status_code": None, "error": "Request timed out"}
    except requests.ConnectionError:
        return {"success": False, "status_code": None, "error": "Connection error"}
    except Exception as e:
        return {"success": False, "status_code": None, "error": str(e)}    
data=fetch_json("https://jsonplaceholder.typicode.com/todos/1")
for key,value in (data.items()):
    
    if key=="headers":
        print("---------Headers------------")
        for k,v in (value.items()):
            
            print(f"{k} : {v}")
        print("-------------------------")
    else:
        print(f" {key} : {value} ")        