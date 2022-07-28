import os
import http_requests
import argparse
import time
import create_file

devCert_URL = 'https://api.nrfcloud.com/v1/account/certificates'


def parse_args():
    parser = argparse.ArgumentParser(description="Device Credentials Installer",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path", type=str,
                        help="Path to save files.  Selects -s", default="./")
    return parser.parse_args()

args = parse_args()
write_file = create_file.write_file

def found_acc_device(api_key, certs_flag):
    #check if we have all the certs for the device. Make sure file is in format: [certname].[certtype]
    key_exists = os.path.exists('privateKey.pem')
    ca_exists = os.path.exists('caCert.pem')
    client_exists = os.path.exists('clientCert.pem')

    if not(key_exists==True and ca_exists==True and client_exists==True):   #check for missing files
        user_choice = input('Missing file(s). Would you like to automatically generate the missing file(s)? (Y/N) ')
        if user_choice == 'Y':
            create_dev_cert = http_requests.http_req('POST', devCert_URL, api_key)
            if key_exists != True:
                print('\nGenerating Private Key...')
                time.sleep(0.5)
                keyOnly = create_dev_cert['privateKey']
                write_file(args.path, 'privateKey.pem', keyOnly)
            if ca_exists != True:
                print('\nGenerating CA Certificate...')
                time.sleep(0.5)
                caOnly = create_dev_cert['caCert'] 
                write_file(args.path, 'caCert.pem', caOnly)
            if client_exists != True:
                print('\nGenerating Client Certificate...')
                time.sleep(0.5)
                clientOnly = create_dev_cert['clientCert']
                write_file(args.path, 'clientCert.pem', clientOnly)
            print('... Action completed!')
            return certs_flag == 0
        elif user_choice == 'N':
            print('File(s) will not be made.')
            time.sleep(0.5)
            print('Unable to connect without proper device and certificates. Restarting... \n')
            time.sleep(0.5)
            return certs_flag == 1
        else:
            print('Invalid response.')
            return certs_flag == 1
    else:
        print('All file names matched')
        return certs_flag == 0

def create_device(api_key, certs_flag):
    user_input = input('\nNo account device detected.\nWould you like to automatically create an account device and its corresponding certificates? (Y/N) ')
    if user_input == 'Y':
        create_dev_cert = http_requests.http_req('POST', devCert_URL, api_key)  #create uses 'POST'
        keyOnly = create_dev_cert['privateKey']
        caOnly = create_dev_cert['caCert']
        clientOnly = create_dev_cert['clientCert']
        '''Create pem files and save the certificates generated above'''
        write_file(args.path, 'privateKey.pem', keyOnly)    #save privateKey as pem file
        write_file(args.path, 'caCert.pem', caOnly)     #save caCert as pem file
        write_file(args.path, 'clientCert.pem', clientOnly)  #save clientCert as pem file
        return certs_flag == 0
    elif user_input == 'N': 
        print('\nUnable to connect without proper device and certificates.')
        return certs_flag == 1
    else:
        print('Invalid response.')
        return certs_flag == 1