from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
	return {"CUSTOM PLAYLIST API": "FAST API"}

@app.get("/api_youtube/")
def reply_user(payload:dict):
	#print(payload)
	
	
	data = {}
	data['user_id']=payload['user_id']
	data['bot_id']=payload['bot_id']
	data['module_id']=payload['module_id']
	data['message'] = listOfVideos
	data['suggested_replies']=[]
	data['blocked_input']=True
	
	json_data = json.dumps(data)
	
	return json_data
