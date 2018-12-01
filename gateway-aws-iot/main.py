#!/usr/bin/env python
import rospy
from gateway_node import GateWaysNode

client_id = 'GateWay01'
publish_topic = 'warning'

if __name__ == '__main__':
    try:
        gate_way = GateWaysNode(client_id, publish_topic)
        gate_way.config()
        gate_way.start()
    except Exception as e:
        print("Something went wrong in main!")
        print(e)
