from fastapi import FastAPI
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
def reply_user(user_id:int,bot_id:int,module_id:int,message:str):
	
	print(user_id)
	print(bot_id)
	print(module_id)
	print(message)
	
	search_term=message

	results = parse_html('AI Artificial Intelligence in '+search_term+' "KarachiDotAI"')

	filtered_results=[x for x in results if fuzz.partial_token_set_ratio(x['title'],search_term)>90]

	[print(x['title'],sep='\n') for x in filtered_results]

	videos=[x['url_suffix'].split('=')[1] for x in filtered_results]

		
	if filtered_results:
		
		listOfVideos = "http://www.youtube.com/watch_videos?video_ids=" + ','.join(videos)
		final_url=requests.get(listOfVideos).url
	
	
	data = {}
	data['user_id']=user_id
	data['bot_id']=bot_id
	data['module_id']=module_id
	data['message'] = final_url if filtered_results else 'No Content Found'
	data['suggested_replies']=[]
	data['blocked_input']=True
	
	return data
