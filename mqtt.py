import paho.mqtt.publish as publish

from typing import (
    Dict
)

from schedule import Schedule
from config import config


class Client(object):
    def __init__(self):
        self.auth = {'username': config['mqtt']['username'], 'password': config['mqtt']['password']}
    def send(self, schedule: Schedule):
        publish.multiple(schedule.as_msgs(), hostname=config['mqtt']['host'], port=1883, will=None, auth=self.auth)

    
    
