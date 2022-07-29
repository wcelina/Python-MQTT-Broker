'''Publish Menu'''
import time
import json 

class Publish():
    PUBS_MENU = [
        'Publish to...',
        'See All Subscribed Topics',
        'Back'
    ]
    TOPIC_CATEGORY = [
        'Shadow Topics',
        'Message and Location Services Topics',
        'FOTA Topics',
        'Additional Topics',
        'Back']
    SHADOW_TOPIC = [
        "$aws/things/${device_id}/shadow/get\n(Request the device's shadow.)\n",
        '$aws/things/${device_id}/shadow/update\n(Update the device shadow.)'
        'Back\n']
    MSGLOCA_TOPIC = [
        'mqtt_topic_prefix/m/d/${device_id}/d2c\n(Publish messages to nRF Cloud,\nsuch as Location Services data.)\n',
        'mqtt_topic_prefix/m/d/${device_id}/d2c/bulk\n(Publish a batch of messages to nRF Cloud as an array,\nwhich republishes each message in the array to the\
         /d2c topic\n as if each message were published individually.\n Messages sent to /d2c/bulk are not stored.)'
        'Back\n']
    FOTA_TOPIC = [
        '${device_id}/jobs/req\n(Request the current pending job exection for an IP-based device.)',
        '${device_id}/jobs/update\n(Update the status of a job execution for an IP-based device.)',
        'Back\n']
    ADDITIONAL_TOPIC = [
        'm/#\n(Send and receive device messages, and have them\nautomatically stored in the cloud for later retrieval.)\n',
        'Back\n']

    def __init__(self, get_choice):
        self._get_choice = get_choice 
    
    def menu(self, mqtt_topic_prefix, target_id, client):
        '''Publishes Main Menu'''
        select_flag = 0 #for if the user has selected a topic
        print('-------Publish Main Menu--------')
        choice = self._get_choice(self.PUBS_MENU)
        if choice is None or choice == -1:
            return choice 
        if choice == 0: #publish to a topic
            print('____Publish to a Topic____')
            print('  Choose a topic category:')
            category_choice = self._get_choice(self.TOPIC_CATEGORY)
            if category_choice == 0: 
                print('Select the desired Shadow topic:\n')
                shadow_choice = self._get_choice(self.SHADOW_TOPIC)
                if shadow_choice == 0:
                    select_flag = 1
                    topic_format = ('$aws/things/' + target_id + '/shadow/get')
                elif shadow_choice == 1:
                    select_flag = 1
                    topic_format = ('$aws/things/' + target_id +'/shadow/update')
                elif shadow_choice == 2:
                    select_flag = 0
                    self.menu(mqtt_topic_prefix, target_id, client)
            elif category_choice == 1:
                print('Select the desired Messages and Location Services topic:\n')
                msgloca_choice = self._get_choice(self.MSGLOCA_TOPIC)
                if msgloca_choice == 0:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'm/d/' + target_id + '/d2c')
                elif msgloca_choice == 1:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'm/d/' + target_id + '/d2c/bulk')
                elif msgloca_choice == 2:
                    select_flag = 0 
                    self.menu(mqtt_topic_prefix, target_id, client)            
            elif category_choice == 2:
                print('Select the desired FOTA topic:\n')
                fota_choice = self._get_choice(self.FOTA_TOPIC)
                if fota_choice == 0:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + target_id + '/jobs/req')
                elif fota_choice == 1:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + target_id + '/jobs/update')
                elif fota_choice == 2:
                    select_flag = 0
                    self.menu(mqtt_topic_prefix, target_id, client)
            elif category_choice == 3:
                print('Select the desired Additional Topic:\n')
                additional_choice = self._get_choice(self.ADDITIONAL_TOPIC)
                if additional_choice == 0:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'm/#')
                elif additional_choice == 1:
                    select_flag = 0
                    self.menu(mqtt_topic_prefix, target_id, client)

            if select_flag == 1:
                user_msg = input('Enter your message to publish: ')
                print('Initializing... ' + topic_format)
                client.publish('"'+topic_format+'"', '"'+user_msg+'"', 1, True)

            #client.publish(topic=topic_format, payload=user_message, qos=2, retain=True)

        elif choice == 1:   #see subscribed topics 
            print('subscribed topics: (empty for now, include file of subbed topics later)')
        elif choice == 2:   #go back to main menu
            return 