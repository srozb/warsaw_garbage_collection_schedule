#!/usr/bin/env python3

import fire
import requests

from schedule import Schedule
from mqtt import Client
from config import config


def once(dry_run: bool = False):
    """Do the one-time schedule check and print it out (dry-run) or send to mqtt according to configuration"""
    s.update()
    if dry_run:
        print(s.as_msgs())
    else:
        m = Client()
        m.send(s)

    

def main():
    """Daemonize"""
    #trio.run(process, domain_file, nameservers, workers_num, debug)

s = Schedule(addressPointId=config['addressPointId'])

if __name__ == "__main__":
    fire.Fire({
        'once': once,
        'daemon': main
    })