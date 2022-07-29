'''Subscriptions Menu'''
import time

class Subscriptions():
    SUBS_MENU = [
        'Subscribe to...',
        'Unsubscribe from...',
        'Subscriptions',
        'See All Topics',
        'Back']
    TOPIC_CATEGORY = [
        'Shadow Topics',
        'Message and Location Services Topics',
        'FOTA Topics',
        'Additional Topics',
        'Back']
    SHADOW_TOPIC = [
        '${device_id}/shadow/get/accepted\n(Receive a trimmed shadow that contains\nonly essential shadow data.)\n',
        '$aws/things/${device_id}/shadow/get/rejected\n(Receive info about a rejected shadow reqest.)\n',
        '$aws/things/${device_id}/shadow/update/delta\n(Receive info about changes in the shadow request.)\n',
        'Back\n']
    MSGLOCA_TOPIC = [
        'mqtt_topic_prefix/m/d/${device_id}/c2d\n(Receive messages from nRF Cloud,\nsuch as Location Services data.)\n',
        'mqtt_topic_prefix/m/d/${device_id}/d2c\n(Publish messages to nRF Cloud,\nsuch as Location Services data.)\n',
        'Back\n']
    FOTA_TOPIC = [
        '${device_id}/jobs/rcv\n(Receive a FOTA job execution for\nan IP-based device.)\n',
        'Back\n']
    ADDITIONAL_TOPIC = [
        'm/#\n(Send and receive device messages, and have them\nautomatically stored in the cloud for later retrieval.)\n',
        'a/connections\n(Receive connection events from your devices,\ninforming you when they connected and disconnected.)\n',
        'Back\n']

    def __init__(self, get_choice):
        self._get_choice = get_choice 

    def menu(self, mqtt_topic_prefix, target_id, client):
        '''Subscriptions Main Menu'''
        select_flag = 0
        print('-------Subscriptions Menu-------')
        choice = self._get_choice(self.SUBS_MENU)
        if choice is None or choice == -1:
            return choice 
        if choice == 0: #subscribe to a topic
            print('____Subscribe to a Topic____')
            print('  Choose a topic category:')
            category_choice = self._get_choice(self.TOPIC_CATEGORY)
            if category_choice == 0: 
                print('Select the desired Shadow topic:\n')
                shadow_choice = self._get_choice(self.SHADOW_TOPIC)
                if shadow_choice == 0:
                    select_flag = 1
                    topic_format = (target_id + '/shadow/get/accepted')
                elif shadow_choice == 1:
                    select_flag = 1
                    topic_format = ('$aws/things/' + target_id +'/shadow/get/rejected')
                elif shadow_choice == 2: 
                    select_flag = 1
                    topic_format = ('$aws/things/' + target_id + '/shadow/update/delta')         
                elif shadow_choice == 3:
                    select_flag = 0
                    self.menu(mqtt_topic_prefix, target_id, client)
            elif category_choice == 1:
                print('Select the desired Messages and Location Services topic:\n')
                msgloca_choice = self._get_choice(self.MSGLOCA_TOPIC)
                if msgloca_choice == 0:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'm/d/' + target_id + '/c2d')
                elif msgloca_choice == 1:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'm/d/' + target_id + '/d2c')
                elif msgloca_choice == 1:
                    select_flag = 0 
                    self.menu(mqtt_topic_prefix, target_id, client)            
            elif category_choice == 2:
                print('Select the desired FOTA topic:\n')
                fota_choice = self._get_choice(self.FOTA_TOPIC)
                if fota_choice == 0:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + target_id + '/jobs/rcv')
                elif fota_choice == 1:
                    select_flag = 0
                    self.menu(mqtt_topic_prefix, target_id, client)
            elif category_choice == 3:
                print('Select the desired Additional Topic:\n')
                additional_choice = self._get_choice(self.ADDITIONAL_TOPIC)
                if additional_choice == 0:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'm/#')
                elif additional_choice == 1:
                    select_flag = 1
                    topic_format = (mqtt_topic_prefix + 'a/connections')
                elif additional_choice == 2:
                    select_flag = 0
                    self.menu(mqtt_topic_prefix, target_id, client)
            
            if select_flag == 1:
                print('Initializing... ' + topic_format)
                client.subscribe(topic_format, 2)


        elif choice == 1:   #unsubscribe to a topic
            print('----Unsubscribe to a Topic----')
            user_topic = input(str('Enter the topic address: (i.e. /my/topic)'))
            topic_format = (mqtt_topic_prefix + '/m/d/' + target_id + user_topic)
            print('Initializing... ' + topic_format)
            client.unsubscribe(topic_format)

        elif choice == 2:   #list topics subscribed to
            print('list subbed topics here')

        elif choice == 3:   #list all topics
            print('\n----Message and Location Services Topics----')
            print('>> m/d/${deviceID}/c2d\n'
                  '>> m/d/${deviceID}/d2c\n'
                  '>> m/d/${deviceID}/d2c/bulk')
            print('\n----Shadow Topics----')
            print('${deviceID}/shadow/get/accepted\n'
                  '>> $aws/things/${deviceID}/shadow/get/rejected\n'
                  '>> $aws/things/${deviceID}/shadow/update/delta\n'
                  '>> $aws/things/${deviceID}/shadow/get\n'
                  '$aws/things/$${deviceID}/shadow/update')
            print('\n----FOTA Topics----')
            print('>> ${deviceID}/jobs/rcv\n'
                  '>> ${deviceID}/jobs/req\n'
                  '>> ${deviceID}/jobs/update')
            print('\n----Additional Topics----')
            print('>> m/#\n'
                  '>> a/connections\n\n')
            
            time.sleep(3)

        elif choice == 4:   #go back to main menu
            return

    def evt(self, event):
        '''Receive subscription list from device'''
        self._subscriptions = event['addressList'].copy()


#subbed_list.append(topic_format)
#subbed_list.remove()
