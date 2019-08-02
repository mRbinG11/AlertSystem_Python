Alert System

The project has two files:
1.operator.py : code to be run at operator system
2.department.py:code to be run at department system

For the application to work, the systems should be connected to the same local network.

Installations:
1.One of the Rpi's should have mqtt broker installed and running
2.Mosquitto mqtt
3.Kivy

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
1.Select one of the departments
2.Type message and send
3.Video calling starts if the department deems it necessary. Otherwise communication occurs only via text messages

Format of message sent(example):
{"ip":"192.168.x.x","machine_id":"m1","data":"Help needed"}

Messages are published to the topic :"iot/alert/" + dept
where dept is one of the departments i.e Electrical/Mechanical/Maintenance

Messages are received for the topic : "iot/alert/" + machine_id
where machine_id is the unique identifier for the machine