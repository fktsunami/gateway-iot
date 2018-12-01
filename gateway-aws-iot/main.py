#!/usr/bin/env python
import rospy
from gateway_node import GateWaysNode
import time

client_id = 'GateWay01'
publish_topic = 'warning'

if __name__ == '__main__':
    while(True):
        try:
            gate_way = GateWaysNode(client_id, publish_topic)
            gate_way.config()
            gate_way.start()
        except Exception as e:
            print("Something went wrong in main!")
            print(e)
        time.sleep(1)
        print('===================================')
        print('Trying to reconnect...')
