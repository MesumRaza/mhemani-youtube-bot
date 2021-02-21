from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
	return {"CUSTOM PLAYLIST API": "FAST API"}

@app.post("/api_youtube/")
def reply_user(payload:dict):
	#print(payload)
	
	
	data = {}
	data['user_id']=payload['user_id']
	data['bot_id']=payload['bot_id']
	data['message'] = 'https://www.youtube.com/watch?v=l0leUH4ZXvU&list=TLGGV687NVFVkE0yMTAyMjAyMQ'
	data['module_id']=payload['module_id']
	data['suggested_replies']=[]
	data['blocked_input']=True
	
	return data
