from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.textinput import TextInput
import paho.mqtt.client as mqtt
from kivy.uix.dropdown import DropDown
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.spinner import Spinner
import json
import threading

dept="Electrical"
broker_url="192.168.43.64"
broker_port=1883
machine_id ="m1"
class Alert_dept(Screen):

    flag = True
    topic="iot/alert/"
    def __init__(self, **kwargs):
        super(Alert_dept, self).__init__(**kwargs)
        layout = RelativeLayout()
        drop = DropDown()
        self.msg = TextInput(hint_text="Message to be received",size_hint=(0.75,.3),pos_hint={'x':0.07,'y':0.55})
        self.hi = TextInput(hint_text="Enter message to send",size_hint=(0.75,.3),pos_hint={'x':0.07,'y':0.2})
        sendbutton = Button(text='SEND', size_hint=(.1,.1),pos_hint={'x':0.37,'y':0.07})
        sendbutton.bind(on_press=lambda x:self.sendmsg())
        #endbutton = Button(text='HANG UP', size_hint=(.2,.1),pos_hint={'x':0.1,'y':0.05})
        #endbutton.bind(on_press=lambda x:self.hangup())
        #testbtn = Button(text = 'Change', size_hint = (.2,.1),pos_hint={'x':0.1,'y':0.05})
        #testbtn.bind(on_press = lambda x:self.switch_next())
        self.spinner = Spinner(text='Mechanical',values=('Electrical', 'Mechanical', 'Maintenance'),size_hint=(.15,.09),pos_hint={'x':0.05,'y':0.9})
        self.spinner.bind(on_text=self.show_selected_value)
        layout.add_widget(self.msg)
        layout.add_widget(self.hi)
        layout.add_widget(sendbutton)
        layout.add_widget(self.spinner)
        #layout.add_widget(endbutton)
        #layout.add_widget(testbtn)
        self.add_widget(layout)
    
    def on_enter(self):
        self.flag = True
        self.msg.text =""
        self.hi.text=""
        self.t1 = threading.Thread(target=self.recvmsg)
        self.t1.start()

    def on_message(self, client, userdata, message):
        m_decode = str(message.payload.decode())
        m_in = json.loads(m_decode)
        video_t = m_in["video"]
        if(video_t == "True"):
         self.switch_next()
        self.msg.text = m_in["data"]

    def show_selected_value(spinner, text):
        pass    
        

    def sendmsg(self):
        client = mqtt.Client()
        client.connect(broker_url, broker_port)
        ip = "192.168.x.x"
        global dept
        dept = self.spinner.text
        data = self.hi.text
        msg = json.dumps({"ip":ip,"m_id":machine_id,"data":data})
        topic_s = "iot/alert/" + dept
        client.publish(topic=topic_s, payload=msg, qos=1, retain=False)

    def recvmsg(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(broker_url, broker_port)
        topic_r = self.topic + machine_id
        client.subscribe(topic_r, qos=1)
        while self.flag:
            client.loop()

    def switch_prev(self, *args):
        
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.previous()

    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()
        self.flag=False
        self.t1.join()
           
class Video_s(Screen):

    flag2 = True
    topic="iot/alert/"
    def __init__(self, **kwargs):
        super(Video_s, self).__init__(**kwargs)
        layout = RelativeLayout()
        endbutton = Button(text='HANG UP', size_hint=(.2,.1),pos_hint={'x':0.1,'y':0.05})
        endbutton.bind(on_press=lambda x:self.hangup())
        layout.add_widget(endbutton)
        chatbutton = Button(text='SEND', size_hint=(.2,.1),pos_hint={'x':0.75,'y':0.05})
        chatbutton.bind(on_press=lambda x:self.sendmsg())
        layout.add_widget(chatbutton)
        self.msg_send = TextInput(hint_text="Enter your message",size_hint=(0.3,.35),pos_hint={'x':0.67,'y':0.17})
        self.msg_recv = TextInput(hint_text="Waiting for messages...",size_hint=(0.3,.35),pos_hint={'x':0.67,'y':0.52})
        self.video = Video(source='test.h264',size_hint=(.6,.8),pos_hint={'x':0.05,'y':0.1})
        layout.add_widget(self.video)
        layout.add_widget(self.msg_recv)

        layout.add_widget(self.msg_send)
        self.add_widget(layout)

    def on_enter(self):
        self.flag2 = True
        self.msg_send.text =""
        self.msg_recv.text =""
        self.t2 = threading.Thread(target=self.recvmsg)
        self.t2.start()
        self.video.state ='play'

    def play_video(self):
        pass#self.video.state = 'play'

    def hangup(self):
        self.flag2=False
        self.t2.join()
        self.switch_prev()

    def on_message(self, client, userdata, message):
        m_decode = str(message.payload.decode())
        m_in = json.loads(m_decode)
        self.msg_recv.text= m_in["data"]
        video_t = m_in["video"]
        if(video_t == "True"):
            self.play_video()
            
        
    def sendmsg(self):
        client = mqtt.Client()
        client.connect(broker_url, broker_port)
        ip = "192.168.43.64"
        data = self.msg_send.text
        global dept
        msg = json.dumps({"ip":ip,"m_id":machine_id,"data":data})
        topic_s = self.topic + dept
        client.publish(topic=topic_s, payload=msg, qos=1, retain=False)
        
        
    def recvmsg(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(broker_url, broker_port)
        topic_r = self.topic + machine_id
        client.subscribe(topic_r, qos=1)
        while self.flag2:
            client.loop()
    
    def switch_prev(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.previous()

    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()

class AlertSystem(App):

    def build(self):

        root = ScreenManager()
        root.add_widget(Alert_dept(name='Screen 1'))
        root.add_widget(Video_s(name='Screen 2'))

        return root


if __name__ == '__main__':
    AlertSystem().run()
