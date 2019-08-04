Alert System

The project has two files:
1. operator.py: code to be run at operator system
2. department.py: code to be run at department system

For the application to work, the systems should be connected to the same local network.

Installations:
1. One of the Rpi's should have mqtt broker installed and running
2. Mosquitto mqtt
3. Kivy

Note: test.h264 is the video used for testing purposes

operator.py:

Global variables used:
broker_url: ip address of the machine acting as broker
broker_port: 1883
machine_id: an identifier uniquely identifying a machine

Classes:
Alert_dept(Screen) : For the primary screen 
Video_s(Screen) : Screen for video chat
AlertSystem(App) : Class to handle the two screens

Flow when a user/operator of a machine needs to send a message to the department:
1. Select one of the departments
2. Type message and send
3. Video calling starts if the department deems it necessary. Otherwise communication occurs only via text messages

Format of message sent(example):
{"ip":"192.168.x.x","machine_id":"m1","data":"Help needed"}

Messages are published to the topic :"iot/alert/" + dept
where dept is one of the departments i.e Electrical/Mechanical/Maintenance

Messages are received for the topic : "iot/alert/" + machine_id
where machine_id is the unique identifier for the machine

department.py:

Global variables used:
broker_url: ip address of the machine acting as broker
broker_port: 1883
mid: an identifier uniquely identifying the alert sending machine
flags: to maintain threading process
vcall: boolean to switch status of videocall
dept: name of dept
topic: topic used in mqtt subscribe & publish

Class ReceiveDept(App): App that runs when the respective alert is received

Flow of Control:
1. Receive the alert on the subcribed topic
2. Assess the alert
3. Decide whether text messages would suffice or video call is necessary

Format of message sent(example):
{"video":"Ture","ip":"192.168.x.x",,"data":"Necessary steps to resolve issue"}

Messages are subscribed to the topic :"iot/alert/" + dept
where dept is the respective departments i.e Electrical/Mechanical/Maintenance

Messages are published to the topic : "iot/alert/" + mid
where mid is the unique identifier for the machine