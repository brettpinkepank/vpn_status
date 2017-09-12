#!/bin/python

#Slack App running in Flask
#Intended as backend application for /vpn slash command instituted in Slack
#Apps intended to be used to track status of a VM used primarily for connecting to customer VPN's
#/vpn [status, in-use, free] To check VM usage status, or declare the VM as in-use or free, respectively

#Includes
from flask import Flask, request
import time

#Functions for managing application states
def get_status():
        return [app.vpn_status, app.last_user, app.last_time]
def update_status(new_status, new_user, new_time):
        app.vpn_status = new_status
        app.last_user = new_user
        app.last_time = new_time
        return


app = Flask(__name__)

app.vpn_status = "free"
app.last_user = "Nobody"
app.last_time = "Never"


#Route and parse POST data received from slack app
@app.route("/", methods=['GET', 'POST'])
def command_parse():
        data = request.form
        user_name = data["user_name"]
        command = data["command"]
        text = data["text"]
        
        # /vpn status
        if text.lower() == "status":
                status = get_status()
                vpn_status = status[0]
                last_user = status[1]
                last_time = status[2]

                if vpn_status == "in-use":
                        return "The VPN is IN USE by " + last_user + " since " + last_time
                else:

                        return "The VPN is FREE"
        # /vpn in-use
        elif text.lower() == "in-use":
                last_user = user_name
                last_time = time.asctime( time.localtime(time.time()) )
                vpn_status = "in-use"
                update_status(vpn_status, last_user, last_time)
                return "VPN is now in use!"
        # /vpn free
        elif text.lower() == "free":
                last_user = user_name
                last_time = time.asctime( time.localtime(time.time()) )
                vpn_status = "free"
                update_status(vpn_status, last_user, last_time)
                return "VPN is now free!"
        else:
                return "Command not recognized... [status, in-use, free]"

#Run App
if __name__ == '__main__':
    app.run()
