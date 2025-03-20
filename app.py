from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import requests
import json
import uvicorn

app = FastAPI()
security = HTTPBasic()

DEFAULT_HOSTNAME = "useast.services.cloud.techzone.ibm.com"

# Function to get bearer token
def get_bearer_token(username: str, password: str):
    token_url = f"https://{DEFAULT_HOSTNAME}:41545/v1.0/token"
    headers = {
        "tenantId": "bb15ceb8-d52c-45c1-82f4-8c2c05de763a",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'culture': 'en-US'
    }
    response = requests.post(token_url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve bearer token")

@app.post("/execute")
def execute_task(credentials: HTTPBasicCredentials = Depends(security), json_data: dict = {}):
    token = get_bearer_token(credentials.username, credentials.password)
    api_url = f"https://{DEFAULT_HOSTNAME}:41545/v2.0/workspace/bb15ceb8-d52c-45c1-82f4-8c2c05de763a/projects/auditdemo/bots/auditbot"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, headers=headers, json=json_data, verify=False)
    if response.status_code == 200:
        return {"message": "Successfully sent the second request", "response": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)