#!/usr/bin/env python3
"""
This shows a simple example of an enhanced authentication with an MQTT Broker
which supports the SMOKER authentication method which described here:

    https://arxiv.org/abs/1904.00389

Ensure that the 'examples' and the 'src' directory is in the python path.

Author:
    Fabian Fischer <fabian.fischer.1@students.bfh.ch>
"""

import sys
import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from crypto_helper import CryptoHelper


def mqtt_connect_cb(client, userdata, flags, rc, properties):
    mqtt.subscribe('test/I', 1)


def mqtt_auth_cb(client, reason_code, properties):
    prop = properties.json()
    nonce = prop['AuthenticationData']
    signed_message = authN.sign_message(nonce)

    auth_props = Properties(PacketTypes.AUTH)
    auth_props.AuthenticationMethod = ("SMOKER")
    auth_props.AuthenticationData = (signed_message)

    mqtt.auth(reasoncode=reason_code, properties=auth_props)


def mqtt_disconnect_cb(client, userdata, rc):
    sys.exit(rc)


def mqtt_message_cb(client, userdata, msg):
    print('Got message "{}"'.format(msg.payload.decode('utf-8')))


def main():
    global mqtt
    global authN

    authN = CryptoHelper()

    authN.generate_keypair()
    clientid = authN.get_public_key_encoded()
    auth_data = authN.get_public_key()
    auth_props = Properties(PacketTypes.AUTH)
    auth_props.AuthenticationMethod = ("SMOKER")
    auth_props.AuthenticationData = (auth_data)

    mqtt = mqtt.Client(client_id=clientid, protocol=5)

    mqtt.on_connect = mqtt_connect_cb
    mqtt.on_disconnect = mqtt_disconnect_cb
    mqtt.on_message = mqtt_message_cb
    mqtt.on_auth = mqtt_auth_cb

    print('Connect to MQTT Broker..')
    mqtt.connect_async('127.0.0.1', 1883, 60, properties=auth_props)
    mqtt.loop_start()

    print('Sleep for 3 seconds..')
    time.sleep(3)

    print('Publish test message..')
    mqtt.publish('test/I', 'test message')
    time.sleep(2)

    print('Disconnect from MQTT Broker..')
    mqtt.disconnect()
    time.sleep(2)


if __name__ == '__main__':
    main()
