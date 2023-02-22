import requests
import json

class Character:
	def __init__(self, token, id):
		self.session = requests.Session()
		self.token = token
		self.id = id
		self.user: str
		self.name: str
		self.history: str		
		self.setup(self.id)

	def req(self, url, data):
		return self.session.post(url = f"https://beta.character.ai/chat/{url}/", data = data, headers = {
			"Authorization": "Token " + self.token,
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
		})

	def setup(self, id):
		res = self.req("character/info", {"external_id": id})
		data = res.json()
		self.id = id
		self.user = data["character"]["participant"]["user"]["username"]
		self.name = data["character"]["participant"]["user"]["first_name"]
		self.resume()
		return data["character"]["greeting"]

	def create(self):
		res = self.req("history/create", {"character_external_id": self.id})
		data = res.json()
		self.history = data["external_id"]
		return "Chat reset"
		
	def resume(self):
		res = self.req("history/continue", {"character_external_id": self.id})
		data = res.json()
		
		if "external_id" in data:
			self.history = data["external_id"]
		else:
			self.create()

	def stream(self, text):
		res = self.req("streaming", {"character_external_id": self.id, "tgt": self.user, "history_external_id": self.history, "text": text})				
		for line in res.iter_lines():
			if line:
				data = json.loads(line)
					
				if data["is_final_chunk"]:
					return data["replies"][0]["text"]