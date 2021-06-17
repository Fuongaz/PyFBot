from fbchat import Client
from fbchat.models import *
from random import randrange
from colorama import Fore, init
from requests import *
from datetime import datetime
from google_trans_new import google_translator 
from youtubesearchpython import VideosSearch
from NHentai.nhentai import NHentai
from tqdm import tqdm
from bs4 import BeautifulSoup
import sys
import time
import wikipedia
import feedparser
import TiktokApi
import os
import pyttsx3
import math
import gdshortener
import re
import random
import yaml

lg = Fore.LIGHTGREEN_EX
ly = Fore.LIGHTYELLOW_EX
lr = Fore.LIGHTRED_EX

info = lg + """
			██████╗░██╗░░░██╗███████╗██████╗░░█████╗░████████╗
			██╔══██╗╚██╗░██╔╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝
			██████╔╝░╚████╔╝░█████╗░░██████╦╝██║░░██║░░░██║░░░
			██╔═══╝░░░╚██╔╝░░██╔══╝░░██╔══██╗██║░░██║░░░██║░░░
			██║░░░░░░░░██║░░░██║░░░░░██████╦╝╚█████╔╝░░░██║░░░
			╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚═════╝░░╚════╝░░░░╚═╝░░░
""" + ly + """ 
			PYFBOT | FACEBOOK MESSAGER BOT WRITTEN IN PYTHON
					AUTHOR BY PHUONGAZ
 """ + lg

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
account = ''
current_folder_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.dirname(os.path.abspath(__file__)) + "/config.yaml", 'r') as stream: 

	try: 
		username = yaml.safe_load(stream)['user_mame']
		password = yaml.safe_load(stream)['password']

	except: print('Vui lòng nhập tài khoản/mật khẩu')



class Events(Client):
	def onMessage(self, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
		if message_object.text is not None:
			params = message.split()
			cmd = params[0].lower()
			if cmd == '.?':
				help_mess = """
	+ covid : xem tình hình covid hiện tại
	+ covid-news: xem tin tức về tình hình dịch bệnh
	+ query <ip> <port> (lưu ý dấu . nên đỏi thành ,) : xem tình trạng máy chủ mcbe
	+ mèo|cat : xem ảnh mèo
	+ chó|dog : xem ảnh bạn
	+ say <ngôn ngữ (ví dụ "en")> <nội dung>: Tạo bản ghi âm
	+ weather <thành phố|tỉnh thành>: xem thời tiết
	+ ytb <tên muốn tìm> : tìm video trên youtube
	+ shortlink <link> : rút ngắn liên kết
	+ nhentai <tên muốn tìm> : Ai biết gì đâu
	+ playmusic <link youtube> : nghe nhạc đã tải
	+ wiki <nội dung muốn tìm> : Xem wikipedia
	+ xs <nam|bắc>: Xem kết quả sổ số hôm nay
	+ dịch <nội dung> : dịch ngoại ngữ sang tiếng việt
	+ qrcode <nội dung> : tạo mã QRCode
	PyFBot by Phuongaz
	"""
				client.sendMessage(message=help_mess, thread_id=thread_id, thread_type=thread_type)
			if cmd == 'hi':
				client.send(Message(text='Hí chào cậu, mình đứng đây từ chiều'), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'covid':
				content = BotHandle.CovidIMT()
				client.send(Message(text=content), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'query':
				host = params[1].replace(',', '.')
				port = params[2]
				content = BotHandle.QueryMCBE(host=host, port=port)
				client.send(Message(text=content), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'mèo' or cmd == 'cat':
				url = 'https://api.thecatapi.com/v1/images/search'
				response = get(url)
				result = response.json()[0]['url']
				client.sendRemoteImage(image_url=result, thread_id=thread_id, thread_type=thread_type)
			if cmd == 'chó' or cmd == 'dog':
				url = 'https://dog.ceo/api/breeds/image/random'
				response = get(url)
				result = response.json()['message']
				client.sendRemoteImage(image_url=result, thread_id=thread_id, thread_type=thread_type)	
			if cmd == 'dịch':
				if thread_id == author_id:
					str1 = message.replace('dịch ', '')
					text = BotHandle.Translator(content=str1)
					client.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'ytb':
				string = message.replace('ytb ', '')
				videosSearch = VideosSearch(string, limit = 3)
				result = videosSearch.result()
				for video in result['result']:
					self.send(Message(text='Tên: ' + video['title'] + '\nLink: ' + video['link']), thread_id=thread_id, thread_type=thread_type)   
			if cmd == 'say':
				content = " ".join(map(str, params[2:]))
				file_name = BotHandle.Speak(text_to_speak=content, language=params[1].lower())
				client.sendLocalVoiceClips(clip_paths=file_name, thread_id=thread_id, thread_type=thread_type)
				os.remove(file_name)
			if cmd == 'weather':
				city = message.replace('weather ', '')
				content = BotHandle.getWeather(city=city)
				message_id = client.send(Message(text=content), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'shortlink':
				link = message.replace('shortlink ', '')
				s = gdshortener.ISGDShortener()
				content = 'Link: ' + (s.shorten(link)[0])
				message_id = client.send(Message(text=content), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'nhentai':
				name = message.replace('nhentai ', '')
				nhentai = NHentai()
				search_obj = nhentai.search(query=name, sort='popular', page=1)
				i = 0
				for douji in search_obj.doujins:
					content = 'Tên: ' + douji.title + '\n' + 'link: ' + douji.id
					message_id = client.send(Message(text=content), thread_id=thread_id, thread_type=thread_type)
					if i == 4:
						break;
					i+1
			if cmd == 'playmusic':
				ytlink = message.replace('playmusic ', '')
				path = BotHandle.downloadMP3(ytlink)
				client.sendMessage(message='Tải thành công, vui lòng chờ!')
				client.sendLocalVoiceClips(clip_paths=path, thread_id=thread_id, thread_type=thread_type)
				os.remove(path)
			if cmd == 'wiki':
				question = message.replace('wiki ', '')
				wiki = BotHandle.wiki(search=question)
				client.send(Message(text=wiki), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'xs':
				if params[1].lower() == 'nam':
					return_msg = BotHandle.getXSMN()
					message_id = client.send(Message(text=return_msg), thread_id=thread_id, thread_type=thread_type)
				if params[1].lower() == 'bac' or params[1].lower() == 'bắc':
					return_msg = BotHandle.getXSMB()
					client.send(Message(text=return_msg), thread_id=thread_id, thread_type=thread_type)	
			if cmd == 'qrcode':
				content = message.replace('qrcode ', '')
				file_name = BotHandle.createQRCode(content=content)
				message_id = client.sendLocalImage(image_path=file_name, thread_id=thread_id, thread_type=thread_type)
				os.remove(file_name)
			if cmd == 'covid-news':
				content = BotHandle.getCovidNews()
				message_id = client.send(Message(text=content), thread_id=thread_id, thread_type=thread_type)
			if cmd == 'tiktok':
				if params[1].lower() == 'music':
					if params[2] is not None:
						music = BotHandle.getTiktokMusicURL(params[2])
						client.sendRemoteVoiceClips(clip_url=musics, thread_id=thread_id, thread_type=thread_type)


	def onFriendRequest(self, from_id, msg):
		client.friendConnect(friend_id=from_id)

	def onPendingMessage(self, thread_id, thread_type, metadata, msg):
		client.send(Message(text='Chào bạn mình tên là PyFBot\nVui lòng chat: .? để xem các lệnh hiện có'), thread_id=thread_id, thread_type=thread_type)

class BotHandle:

	def CovidIMT():
		response = get('https://disease.sh/v3/covid-19/countries/Vietnam')
		vn = response.json()
		content = 'Tổng ca mắc: ' + str(vn['cases']) + '\nSố ca mắc hôm nay: ' + str(vn['todayCases']) + '\nTử vong: ' + str(vn['deaths']) + '\nHồi phục: ' + str(vn['recovered']) + '\nThông tin ngày: ' + str(datetime.now())
		return content

	def Translator(content):
		translator = google_translator()  
		detect_result = translator.detect(str1)
		return translator.translate(str1, lang_src=detect_result, lang_tgt='vi')

	def getXSMN():
		url = 'https://xskt.com.vn/rss-feed/mien-nam-xsmn.rss'
		feed_content = feedparser.parse(url)
		first_node = feed_content['entries']
		return first_node[0]['title'] + "\n" + first_node[0]['description']
		
	def getXSMB():
		url = 'https://xskt.com.vn/rss-feed/mien-bac-xsmb.rss'
		feed_content = feedparser.parse(url)
		first_node = feed_content['entries']
		return first_node[0]['title'] + "\n" + first_node[0]['description']

	def createQRCode(content):
		url = 'https://api.qrserver.com/v1/create-qr-code/?data='+ content +'d&amp;size=100x100'
		file_name = current_folder_path + '/components/qrcode.png'
		with open(file_name, "wb") as file:
			response = get(url)
			file.write(response.content)
		return file_name

	def getCovidNews():
		response = get("https://tuoitre.vn/tin-moi-nhat.htm")
		soup = BeautifulSoup(response.content, "html.parser")
		titles = soup.findAll('h3', class_='title-news')
		links = [link.find('a').attrs["href"] for link in titles]
		for link in links:
			news = get("https://tuoitre.vn" + link)
			soup = BeautifulSoup(news.content, "html.parser")
			title = soup.find("h1", class_="article-title").text
			abstract = soup.find("h2", class_="sapo").text
			body = soup.find("div", id="main-detail-body")
			content = body.findChildren("p", recursive=False)[0].text + body.findChildren("p", recursive=False)[1].text
			lower = content.lower()
			if lower.find('covid-19') != -1 or lower.find('covid') != -1:
				#image = body.find("img").attrs["src"]
				content = """
	Tiêu đề: {title}

	Mô tả: {abstract}

	Nội dung: {content}
	""".format(title=title, abstract=abstract, content=content)
				return content

	def getTiktokMusicURL(or_url):
		Api = TiktokApi.Tiktok()
		vid = Api.getInfoVideo(params[2])
		return vid['music']['playUrl']

	def wiki(search):
		wikipedia.set_lang("vi")
		return wikipedia.summary(search, sentences=1)

	def downloadMP3(ytlink):
		url1 = "https://yt1s.com/api/ajaxSearch/index"
		data = {"q": ytlink,"vt": "mp3"}
		r = post(url1,data=data)
		response =  r.json()

		vid = response['vid']				# Get video id
		k = response['kc']
		title = response['title']	
		a_rtist = response['a']
		client.send(Message(text='Đang tải: ' + title), thread_id=thread_id, thread_type=thread_type)

		url2 = "https://yt1s.com/api/ajaxConvert/convert"

		data = {"vid": vid,"k": k}

		r2= post(url2,data=data)

		for _ in range(20):
			sys.stdout.flush()
			time.sleep(0.1)
			sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b')	

		res = r2.json()

		dlink = res['dlink']
		url3 = dlink

		headers = {
			"authority": "dl228.iijjvii.biz",
			"method": "GET",
			"path": "/?file=M3R4SUNiN3JsOHJ6WWQ3aTdPRFA4NW1rRVJIOG10b0F0dndkN3lSb0lwMWdrc1prKytIckI5eEVLK3hFK1lPdkZKVmc1ei9PZE56QUhpeTYvYW9qVG5hQTVOTnp0QytjdFlncFZjeE9SaGZzazd2bXhCZHZoaExoYTlySVVPcHdZR2NvNWhKRmhXUEI2dWlHdEJUc3RqT3VxRURJSVc4SHV6OEZOUExZNWFCTHcyWGZVUHZoN0pRUXBpT2c5cE5FMzgrSnBnRGd4cjRCdHQ5bVlWWnhmNVZjeXAvSzg4YnByRlFidUw4KzIyenFwUEwxUUprd0UvaS9USEYxSmpJQSsrcjdWUllia25SSXFqenNyL2gzdnpKUFlyWW8rM1RsckE9PQ%3D%3D",
			"scheme": "https",
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-US,en;q=0.9",
			"referer": "https://yt1s.com/",
			"sec-ch-ua": "\"Chromium\";v=\"90\", \"Opera\";v=\"76\", \";Not A Brand\";v=\"99\"",
			"sec-ch-ua-mobile": "?0",
			"sec-fetch-dest": "document",
			"sec-fetch-mode": "navigate",
			"sec-fetch-site": "cross-site",
			"upgrade-insecure-requests": "1",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94"
		}

		params = {"file": dlink}

		r3 = get(url3,stream=True)

		tnm = str(title)
		curname = tnm+".mp3"
		songname = curname.replace('/', '').replace('|', '')

		rcode = r3.status_code			  
		if rcode == 200 :
			total = int(r3.headers.get('content-length', 0))   # Progressbar
			with open(rcurrent_folder_path + '/components/' + songname, 'wb') as file, tqdm(
				desc=songname,
				total=total,
				unit='iB',
				unit_scale=True,
				unit_divisor=1024,
			) as bar:
				for data in r3.iter_content(chunk_size=1024):
					size = file.write(data)					 # Downloading
					bar.update(size)  
			return current_folder_path + '/components/'+songname
		else :
			print("Download failed ! ",rcode)

	def QueryMCBE(host, port):
		url = 'http://mcapi.us/server/query?ip=' + host + '&port=' + port
		response = get(url)
		json = response.json()
		if json['status'] == 'success':
			if json['online']:
				online = 'hoạt động'
			else:
				online = 'offline'
			player = str(json['players']['now']) +'/'+ str(json['players']['max'])
			content = 'Trạng thái: ' + online + '\nNgười chơi: ' + player
		else:
			content = 'Lỗi: ' + json['error'] + '\nVui lòng thử lại sau' 
		return content

	def getWeather(city):
		ow_url = "http://api.openweathermap.org/data/2.5/weather?"
		if not city:
			pass
		api_key = "fe8d8c65cf345889139d8e545f57819a"
		call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
		response = get(call_url)
		data = response.json()
		if data["cod"] != "404":
			city_res = data["main"]
			current_temperature = city_res["temp"]
			current_pressure = city_res["pressure"]
			current_humidity = city_res["humidity"]
			suntime = data["sys"]
			sunrise = datetime.fromtimestamp(suntime["sunrise"])
			sunset = datetime.fromtimestamp(suntime["sunset"])
			wthr = data["weather"]
			weather_description = wthr[0]["description"]
			now = datetime.now()
			content = """Hôm nay là ngày {day} tháng {month} năm {year}
Mặt trời mọc vào {hourrise} giờ {minrise} phút
Mặt trời lặn vào {hourset} giờ {minset} phút
Nhiệt độ trung bình là {temp} độ C
Áp suất không khí là {pressure} héc tơ Pascal
Độ ẩm là {humidity}%
Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
																						   hourset = sunset.hour, minset = sunset.minute, 
																						   temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
			return content

	def Speak(text_to_speak, language):
		url = 'https://translate.google.com/translate_tts'

		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
		}

		params = {
			'ie': 'UTF-8',
			'client': 'gtx',
			'q': text_to_speak,
			'tl': language
		}

		if not text_to_speak:
			return False

		clip_filename = current_folder_path + '/components/voicetest.mp3'

		clip = get(url, params=params, headers=headers).content
		if clip:
			try:
				with open(clip_filename, 'wb') as f:
					print(f"Saving in file: {clip_filename}")
					f.write(clip)
				return clip_filename
			except Exception as e:
				print(f"ERROR: Cannot write: {clip_filename} -- ({e})")
		else:
			print('ERROR: Nothing to save in file. Try again later.')


print(info)
with open(current_folder_path + "/config.yaml", 'r') as stream: 

	try: 
		account = yaml.safe_load(stream)
		if account['user_name'] == '' or account['password'] == '':
			print('Vui lòng nhập tài khoản/mật khẩu (config.yaml)')
			sys.exit()
	except yaml.YAMLError as exc:
		print(exc)

client = Events(account['user_name'], account['password'], user_agent=user_agent)
client.listen()