from fastapi import FastAPI, Request, Form
import json
from fuzzywuzzy import fuzz
import requests
import urllib.parse

app = FastAPI()

def parse_html(search_terms):
        
        encoded_search = urllib.parse.quote(search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        
        results = []
        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0) 
                res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                results.append(res)
        return results
		

@app.get("/api_youtube/")
def read_root():
	return {"CUSTOM PLAYLIST API": "FAST API"}

	
@app.post("/api_youtube/")
async def reply_user(user_id:str=Form(...),bot_id:str=Form(...),module_id:str=Form(...),channel:str=Form(...),incoming_message:str=Form(...),step_id:str=Form(...),*,request:Request):
	
	#print(request.url)
	print(await request.form())
	#print(request.headers)
		
	#user_id=payload.get('user_id')
	#bot_id=payload.get('bot_id')
	#module_id=payload.get('module_id')
	#channel=payload.get('channel')
	#incoming_message=payload.get('incoming_message')

	data = {}
	
	print(user_id)
	print(step_id)
	print(bot_id)
	print(module_id)
	print(channel)
	print(incoming_message)

	if user_id and bot_id and step_id and module_id and channel and not any(word in incoming_message.lower() for word in ['recommend', 'learn', 'suggest', 'share']):
		
		print("CheckPoint-1")

		search_term=incoming_message.lower().strip()

		results = parse_html('AI Artificial Intelligence in '+search_term+' "KarachiDotAI"')
		
		#print([x['title'] for x in results])

		filtered_results=[x for x in results if fuzz.partial_token_set_ratio(x['title'],search_term)>80]

		[print(x['title'],sep='\n') for x in filtered_results]

		videos=[x['url_suffix'].split('=')[1] for x in filtered_results]
			
		print("CheckPoint-2")
		
		if filtered_results:
			
			listOfVideos = "http://www.youtube.com/watch_videos?video_ids=" + ','.join(videos)
			final_url=requests.get(listOfVideos).url
			print(final_url)
			
			print("CheckPoint-3")

		data['user_id']=user_id
		data['bot_id']=bot_id
		data['module_id']=module_id
		data['step_id']=step_id		
		
		if filtered_results:
			
			data['message'] = 'Here is your Personalized Playlist'
			data['cards']=[
				{
				"type": "text",
				"value": "Click Start Learning!",
				"buttons": [
					{
						"type": "url",
						"value": final_url,
						"name": "Start Learning"
					}]}]
					
			print("CheckPoint-4")
			
		else:
			data['message'] = 'Sorry Cannot find Your Topic, Let\'s Restart Recommendation! Please enter your choice by Selecting from Below Cards or Enter your Search Keyword and We will find best videos from our Youtube Channel'
			data['suggested_replies']=['NLP','Ecommerce','Finance','Robotics']
			data['blocked_input']=False
			
			print("Failure-CheckPoint-1")
			
		return data
		
	else:
		print("Chat Initiated")
		data['user_id']=user_id
		data['bot_id']=bot_id
		data['module_id']=module_id
		data['message'] = 'Please enter your choice by Selecting from Below Cards or Enter your Search Keyword and We will find best videos from our Youtube Channel'
		data['suggested_replies']=['NLP','Ecommerce','Finance','Robotics']
		data['blocked_input']=False
				
		print(data)
		
		return data
	
	return data
