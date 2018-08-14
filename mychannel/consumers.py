from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync #Wrapper for sync code
import cv2 as cv
import time
import base64
import numpy as np
import json
import threading
import urllib.request as urllib2

class CamConsumer(WebsocketConsumer):

	def connect(self):
		self.room_name = "ServerCams"
		self.room_group_name = "ServerCam"
		async_to_sync(self.channel_layer.group_add)(
				self.room_group_name,
				self.channel_name
			)
		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
				self.room_group_name,
				self.channel_name
			)

	def receive(self, text_data=None):
		text_data = json.loads(text_data)
		
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
			'type' : 'getWebCam',
			'text' : text_data['url'],
			'choice' : text_data['choice']

			}
		)
	

	def getWebCam(self, event):
		cut_beginning = len("data:image/png;base64,")
		if(len(event['text'])>cut_beginning):
			# # Get Base64 data from WebSocket as a string
			frame = event['text'][cut_beginning:]
			img = None

			sec_byte_array = base64.b64decode(frame)
		
			im_array = np.asarray(bytearray(sec_byte_array), dtype=np.uint8)
			img = cv.imdecode(im_array, cv.IMREAD_COLOR)
			

			choice = event["choice"]
			print("Choice: " + str(choice))
			if(choice == "lap"):
				img = cv.Laplacian(img, cv.CV_64F)
			elif(choice == "sobx"):
				img = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
			elif(choice == "soby"):
				img = cv.Sobel(img,cv.CV_64F,0,1,ksize=5)
			elif(choice == "canny"):
				img = cv.Canny(img,150,200)
			elif(choice == "template"):
				template = cv.imread('face.png',0)
				img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
				w, h = template.shape[::-1]
				res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
				threshold = 0.6
				loc = np.where( res >= threshold)
				for pt in zip(*loc[::-1]):
					cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
			elif(choice == "face"):
				face_cascade = cv.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_frontalface_default.xml')
				eye_cascade = cv.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_eye.xml')

				gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
				
				faces = face_cascade.detectMultiScale(img, 1.3, 5)
		
				if(len(faces)>0):
					print("Found " + str(len(faces)) + " faces.")
				else:
					print("Face Not Found")

				for (x,y,w,h) in faces:
				    img = cv.rectangle(img,(x,y),(x+w,y+h),(4,1,35),2)
				    roi_gray = gray[y:y+h, x:x+w]
				    roi_color = img[y:y+h, x:x+w]
				    eyes = eye_cascade.detectMultiScale(roi_gray)
				    for (ex,ey,ew,eh) in eyes:
				        cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(10,0,102),2)
			else:
				pass

			ret, frame = cv.imencode('.png', img)
			base64_img = base64.b64encode(frame)
			
			png_base64 = base64_img.decode("utf-8")
		
			png_hdr = "data:image/png;base64,"
			self.send(text_data = png_hdr + png_base64)



class ChatConsumer(AsyncWebsocketConsumer):


	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		#self.room_name = 'google'
		self.room_group_name = 'mychannel_%s' % self.room_name
		await self.channel_layer.group_add(
        		self.room_group_name,
        		self.channel_name
        	)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)

	async def receive(self, bytes_data=None, text_data=None):
		#print(dir(text_data))
		#print(text_data[:3])
		# print(bytes_data)

		if(text_data):
			await self.channel_layer.group_send(
					self.room_group_name,
					{
					'type' : 'chat_message',
					'text' : text_data
					}
				)
		if(bytes_data):
			await self.channel_layer.group_send(
					self.room_group_name,
					{
					'type' : 'video_message',
					'video' : bytes_data
					}
				)

	# Method to call from Receive
	async def video_message(self, event):
		video = event['video']
		print("Video: " + str(len(video)))
		await self.send(bytes_data=video)

	# Method to call from Receive
	async def chat_message(self, event):
		text = event['text']
		
		await self.send(text_data= text);


class CamShow(AsyncWebsocketConsumer):


	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		#self.room_name = 'google'
		self.room_group_name = 'mychannel_%s' % self.room_name
		await self.channel_layer.group_add(
        		self.room_group_name,
        		self.channel_name
        	)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)

	async def receive(self, bytes_data=None, text_data=None):
		#print(dir(text_data))
		#print(text_data[:3])
		# print(bytes_data)

		if(text_data):
			await self.channel_layer.group_send(
					self.room_group_name,
					{
					'type' : 'chat_message',
					'text' : text_data
					}
				)
		if(bytes_data):
			await self.channel_layer.group_send(
					self.room_group_name,
					{
					'type' : 'video_message',
					'video' : bytes_data
					}
				)

	# Method to call from Receive
	async def video_message(self, event):
		video = event['video']
		print("Video: " + str(len(video)))
		await self.send(bytes_data=video)

	# Method to call from Receive
	async def chat_message(self, event):
		text = event['text']
		
		await self.send(text_data= text);