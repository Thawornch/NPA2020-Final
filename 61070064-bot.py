import urllib.parse
import requests
import json
from datetime import datetime
import time
from ncclient import manager
from pprint import pprint
import xml.dom.minidom
import xmltodict


def bearertoken(self, bearer):
    self.bearer = bearer
    self.auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(self.bearer)}

def requestroomId(self, roomName):
    webex_url = "https://webexapis.com/v1/rooms"
    webex_response = requests.get(url=webex_url, headers=self.auth).json()['items']
    for room in webex_response:
        if room['title'] == roomName:
            return room['id']
    return "Not found!"

def setroomId(self, roomId):
    self.roomId = roomId

def LastedMsg(self, data='text'):
    webex_url = "https://webexapis.com/v1/messages"
    webex_param = {"roomId": self.roomId}
    webex_response = requests.get(url=webex_url, headers=self.auth, params=webex_param).json()
    return webex_response['items'][0][data]

def sendMsg(self, text):
    webex_url = "https://webexapis.com/v1/messages"
    webex_param = {"roomId":self.roomId, 'text':text}
    webex_response = requests.post(url=webex_url, headers=self.auth, json=webex_param).json()
    return webex_response

webExobj = WebexTeam.bearertoken
roomId = WebexTeam.requestroomId(roomName="NPA2020@ITKMITL")

if roomId != "Not found!":
    WebexTeam.setroomId(roomId)

    m = manager.connect(
        host="10.0.15.108",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )

    def get_interfaces_state(int_name):
        netconf_filter = """
            <filter>
                <native
                    xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <interface>
                            <Loopback>
                                <name>61070064</name>
                            </Loopback>
                        </interface>
                </native>
            </filter>
        """
        netconf_reply = m.get_config('running', netconf_filter)

    while 1:
        msg = WebexTeam.getLastestMsg(data='text')
        print("The most recent message is {}".format(msg))

        if msg == "61070064":
            interface_state = get_interfaces_state("Loopback61070064")
            WebexTeam.sendMsg("Loopback61070064 - Operational status is {}".format(interface_state))
        elif msg.lower() == 'End':
            break
        time.sleep(1)
