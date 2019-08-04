from kivy.config import Config
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '300')

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout

import json
import threading
import paho.mqtt.client as mqtt

dept = "Electrical"
topic = "iot/alert/"
vcall = "False"
f1 = True
f2 = True
mid = ""
broker_url = "192.168.137.1"
broker_port = 1883

class ReceiveDept(App):
	
	def build(self):
		lbl = Label(text='ALERT',size_hint=(None,None),pos_hint={'x':0.43,'y':0.75},font_size='50sp')
		self.mlbl = Label(text=mid+':',size_hint=(None,None),pos_hint={'x':0.15,'y':0.55},font_size='35sp')
		self.albl = Label(text=self.tmp,size_hint=(None,None),pos_hint={'x':0.15,'y':0.3},font_size='20sp')
		self.txt = TextInput(hint_text="Enter text to send",size_hint=(0.4,0.4),pos_hint={'x':0.55,'y':0.35},multiline=True)
		vidbtn = Button(text='VIDEO CALL',size_hint=(0.2,0.13),pos_hint={'x':0.02,'y':0.03})
		endbtn = Button(text='HANG UP', size_hint=(0.2,0.13),pos_hint={'x':0.78,'y':0.03})
		sendbtn = Button(text='SEND',size_hint=(0.15,0.1),pos_hint={'x':0.8,'y':0.35})

		vidbtn.bind(on_press=lambda x:self.vidcall())
		sendbtn.bind(on_press=lambda x:self.send_text())
		endbtn.bind(on_press=lambda x:self.hangup())

		layout = FloatLayout()
		layout.add_widget(lbl)
		layout.add_widget(self.mlbl)
		layout.add_widget(self.albl)
		layout.add_widget(self.txt)
		layout.add_widget(vidbtn)
		layout.add_widget(endbtn)
		layout.add_widget(sendbtn)

		self.thr = threading.Thread(target=self.receive_text)
		self.thr.start()

		return layout

	def vidcall(self):
		client = mqtt.Client()
		client.connect(broker_url, broker_port)
		global vcall
		vcall = "True"
		msg = json.dumps({"video":vcall,"ip":"192.168.43.119","m_id":mid,"data":"vidcall"})
		client.publish(topic=topic + mid, payload=msg, qos=1, retain=False)

	def hangup(self):
		global f1, f2
		f1 = False
		f2 = False
		self.thr.join()
		App.get_running_app().stop()

	def send_text(self):
		client = mqtt.Client()
		client.connect(broker_url, broker_port)
		data = str(self.txt.text)
		global vcall
		vcall = "False"
		msg = json.dumps({"video":vcall,"ip":"192.168.43.119","m_id":mid,"data":data})
		client.publish(topic=topic + mid, payload=msg, qos=1, retain=False)

	def on_message(self,client,userdata,message):
		m_decode = str(message.payload.decode())
		m_in = json.loads(m_decode)
		ip = m_in["ip"]
		self.tmp = ip + "\n" + m_in["data"]
		global mid
		mid = m_in["m_id"]
		self.run()

	def on_msg(self,client,userdata,message):
		m_decode = str(message.payload.decode())
		m_in = json.loads(m_decode)
		self.albl.text = m_in["data"]

	def receive_text(self):
		global f1
		f1 = False
		client = mqtt.Client()
		client.on_message = self.on_msg
		client.connect(broker_url,broker_port)
		client.subscribe(topic + dept,qos=1)
		while f2:
			client.loop()

	def receive_mqtt(self):
		client = mqtt.Client()
		client.on_message = self.on_message
		client.connect(broker_url, broker_port)
		client.subscribe(topic + dept, qos=1)
		while f1:
			client.loop()

obj = ReceiveDept()
obj.receive_mqtt()