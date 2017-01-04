#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import redis
import json

class motorCommand:
    def __init__(self,pin,command,direction=None,speed=None):
        self.pin = pin
        self.command = command
        self.direction = direction
        self.speed = speed

    def __str__(self):
        return json.dumps(
            {
                'pin':self.pin,
                'command':self.command,
                'direction':self.direction,
                'speed':self.speed
            }
        )

r = redis.StrictRedis(host='localhost', port=6379, db=0)

print "Back from Python on the server\n"

form = cgi.FieldStorage()
command = form.getvalue("command")
pin = form.getvalue("pin")
direction = form.getvalue("direction")
speed = form.getvalue("speed")

#message = r.get('baz')
#print message

#command2 = motorCommand(27,'START','FORWARD',100)
command2 = motorCommand(pin,command,direction,speed)
print str(command2)
r.rpush('motorQueue', str(command2))

#command3 = motorCommand(28,'stop')
#print command3
#r.rpush('motorQueue', str(command3))
