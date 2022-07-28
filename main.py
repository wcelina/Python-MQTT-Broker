import argparse
import logging
import sys
import time 
import json 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import http_requests
import generate_certs 
import option_2
import subscriptions
import publish_msg

ACC_URL = 'https://api.nrfcloud.com/v1/account'
DEV_URL = 'https://api.nrfcloud.com/v1/devices'
AUTH_BEARER_PREFIX = 'Bearer '
PORT = 8883
KEEP_ALIVE = 30

live = True
getting_input = False
api_key = None
device_id = None 
target_id = None
mqtt_topic_prefix = None
client = None
loop_flag = 0
start_menu = 0
certs_flag = None
subbed_list = []

def on_publish(client, userdata, mid):
    '''MQTT published message callback'''
    print('Messages published!', mid)

def on_message(client, userdata, msg):
    '''MQTT message receive callback'''
    print('Message: ', str(msg.payload.decode("utf-8")))
    print('Topic =  ', msg.topic)

def on_unsubscribe(client, userdata, mid):
    '''MQTT topic unsubscribe callback'''
    print('\nUnsubscribed.', mid)

def on_subscribe(client, userdata, mid, granted_qos):
    '''MQTT topic subscribe callback'''
    print('\nSubscribed. ', mid)
    print('QOS: ' + str(granted_qos) + '\n')
    #code to add topic to memory

def on_connect(client, userdata, flags, rc):
    '''MQTT broker connect callback.'''
    global loop_flag 
    print('Connected with result code: ' + mqtt.connack_string(rc))
    if rc == mqtt.CONNACK_ACCEPTED:
        print("CONNACK RECEIVED. Returned code = ", rc)
        loop_flag += 1
        client.connected_flag = True
        time.sleep(0.5)
        print('Subscribing...')
        client.subscribe(d2c_topic)
    else:
        print("Bad connection. Returned code = ", rc)

def parse_args():
    parser = argparse.ArgumentParser(description="Device Credentials Installer",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--apikey", type=str,
                        help="nRF Cloud account API key",
                        default=None)
    parser.add_argument("-v", "--verbose",
                        help="bool: Make output verbose",
                        action='store_true', default=False)
    parser.add_argument("-d", "--deviceid", type=str,
                        help="Device ID",
                        default=None)
    return parser.parse_args()

def get_choice(options):
    ''' Get a choice from the user from a list of menu options '''
    global live
    global getting_input
    getting_input = True
    while True:
        for idx, option in enumerate(options):
            print(str(idx+1) + '. ' + option)
        choice = input('\n>')
        if choice.lower() == 'exit' or choice.lower() == 'quit':
            live = False
            return None
        if choice.lower() == 'back' or choice.lower() == 'return':
            return -1
        try:
            choice = int(choice)
        except ValueError:
            print('Invalid choice. You must enter a number between 1 and ' + str(len(options)))
            continue
        if choice < 1 or choice > len(options):
            print('Invalid choice. You must enter a number between 1 and ' + str(len(options)))
            continue
        getting_input = False
        return choice-1

subscriptions = subscriptions.Subscriptions(get_choice)
publish_msg = publish_msg.Publish(get_choice)

def menu():
    global live
    global start_menu
    
    time.sleep(1)
    menu_options = [
            'Subscriptions',
            'Publish a Message',
            'Option 3',
            'Quit'
        ]

    while (start_menu == 0):
        start_menu += 1
        print("Welcome to the Python Device Monitor Tool!")
    print("-------Main Menu-------")
    print("Select from the following options:")

    choice = get_choice(menu_options)
    if menu_options[choice] == 'Subscriptions':
        subscriptions.menu(mqtt_topic_prefix, target_id, client)
    elif menu_options[choice] == 'Publish a Message':
        publish_msg.menu(mqtt_topic_prefix, target_id, client)
    elif menu_options[choice] == 'Option 3':
        option_2.my_func()
    elif menu_options[choice] == 'Quit':
        live = False 

def main():
    global live
    global d2c_topic
    global c2d_topic
    global client
    global target_id
    global mqtt_topic_prefix
    global loop_flag

    args = parse_args()
    api_key = args.apikey
    device_id = args.deviceid

    if api_key is None:
        api_key = input("Enter your nRF Cloud API Key: ")
    print('\nQuerying nRF Cloud for account details...')
    
    resp = http_requests.http_req('GET', ACC_URL, api_key)   #fetch account information
    mqtt_endpoint = resp['mqttEndpoint']
    mqtt_topic_prefix = resp['mqttTopicPrefix']
    
    client_id = mqtt_topic_prefix[mqtt_topic_prefix.index('/')+1:]
    client_id = client_id[:client_id.index('/')]
    client_id = 'account-' + client_id 

    print('\n    MQTT Endpoint: ' + mqtt_endpoint)
    print('MQTT Topic Prefix: ' + mqtt_topic_prefix)
    print('   MQTT Client ID: ' + client_id)
    time.sleep(1)

    print('\nSearching nRF Cloud for account devices...')
    resp = http_requests.http_req('GET', DEV_URL, api_key)   #fetch device information
    device_list = []
    for device in resp['items']:
        device_list.append(device['id']) #put device IDs in device_list array
    found_device = [i for i in device_list if i.startswith('account-')]
    if found_device:
        found_flag = 1
        device_id = str(found_device)
        device_id = device_id.strip("['']")
        time.sleep(0.5)
        print('\nFound account device:', device_id) 
        time.sleep(0.5)
        generate_certs.found_acc_device(api_key, certs_flag)
    else:
        found_flag = 0

    if found_flag == 0:   #if no account device found, ask if user wants to create one
        generate_certs.create_device(api_key, certs_flag) 
    if certs_flag == 1:    #files not generated, go back to login
        main()
    
    print('Processing files...')
    time.sleep(0.5)

    #print out list of devices in nRF Cloud
    print('Querying nRF Cloud for all devices')
    for device in resp['items']:
        print('\n  Device ID: ' + device['id'])
        print('Device Name: ' + device['name'])
        print('       Type: ' + device['type'])
        print(' Created On: ' + device['$meta']['createdAt'])
        print('    Version: ' + device['$meta']['version'])
        time.sleep(0.25)
    if target_id is None:   #wait for target device to be chosen
        print('\nSelect a target device:')
        device = get_choice(device_list)
        if device is None or device == -1:
            sys.exit()
        target_id = device_list[int(device)]
        time.sleep(0.25)
    print('\nSelected device: ' + target_id)
    
    '''Automatically subscribe to topics after login, initialized here'''
    print('Initializing auto-subscribed topics...')
    d2c_topic = mqtt_topic_prefix + 'm/d/' + target_id + '/d2c'
    c2d_topic= mqtt_topic_prefix + 'm/d/' + target_id + '/c2d'
    time.sleep(1)
    print('\nCloud-to-Device MQTT Topic: ' + c2d_topic)
    time.sleep(0.5)
    print('Device-to-Cloud MQTT Topic: ' + d2c_topic)
   
    time.sleep(1)   
    print('\nConnecting to MQTT broker...\n')
    client = mqtt.Client(client_id, clean_session=True)
    client.on_connect = on_connect  #bind functions to callback
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish
    client.on_message = on_message
    client.tls_set(ca_certs=str('./caCert.pem'), certfile=str('./clientCert.pem'),
                    keyfile=str('./privateKey.pem'), cert_reqs=mqtt.ssl.CERT_REQUIRED,
                    tls_version=mqtt.ssl.PROTOCOL_TLS, ciphers=None)
    client.connect_async(mqtt_endpoint, PORT, KEEP_ALIVE)

    while live: 
        client.loop_start()
        while loop_flag == 0:
            time.sleep(0.01)
        menu()
        client.loop_stop()
        time.sleep(3)

    client.disconnect()
    client.loop_stop()
    print('.... Exiting!')


if __name__=="__main__":
    main()
