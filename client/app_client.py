#!/usr/bin/env python3

import selectors
import sys
import socket
import traceback
import io

import libclient

sel = selectors.DefaultSelector()


def start_connection(host, port, request):
    addr = (host, port)
    print('starting connection to', addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <path>")
    sys.exit(1)

host, port, pathName = sys.argv[1], int(sys.argv[2]), sys.argv[3]
action = 'getPath'
bucketName = None
fileName = None
fileData = None

content = dict(action=action, pathName=pathName, bucketName=bucketName, fileName=fileName, fileData=fileData)
request = dict(
        type="text/json",
        encoding="utf-8",
        content=content
    )

def send_message():
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()

start_connection(host, port, request)

#send_message()

while True:
    
    print('Enter action number:\n')
    print('1. Create Path')
    print('2. Create Bucket')
    print('3. Bucket Exists')
    print('4. List Buckets')
    print('5. Delete Bucket')
    print('6. Upload File')
    print('7. File Exists')
    print('8. File List')
    print('9. Download File')
    print('10. Delete File')
    print('11. Change Path')
    print('--> ', end='')
    number = input()

    print('')

    if number == '1':
        action = 'getPath'
        content['action'] = action
        print('Enter bucket pathName: ', end="")
        content['pathName'] = input()
        send_message()
        break
    elif number == '2':
        action = 'createBucket'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        send_message()
        break
    elif number == '3':
        action = 'bucketExists'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        send_message()
        break
    elif number == '4':
        action = 'listBuckets'
        content['action'] = action
        send_message()
        break
    elif number == '5':
        action = 'deleteBucket'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        send_message()
        break
    elif number == '6':
        action = 'uploadFile'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        print('Enter file name: ', end="")
        content['fileName'] = input()
        print('Enter file data: ', end="")
        content['fileData'] = input()
        send_message()
        break
    elif number == '7':
        action = 'fileExists'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        print('Enter file name: ', end="")
        content['fileName'] = input()
        send_message()
        break
    elif number == '8':
        action = 'listFiles'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        send_message()
        break
    elif number == '9':
        action = 'downloadFile'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        print('Enter file name: ', end="")
        content['fileName'] = input()
        send_message()
        break
    elif number == '10':
        action = 'deleteFile'
        content['action'] = action
        print('Enter bucket name: ', end="")
        content['bucketName'] = input()
        print('Enter file name: ', end="")
        content['fileName'] = input()
        send_message()
        break
    elif number == '11':
        action = 'getPath'
        content['action'] = action
        print('Enter bucket pathName: ', end="")
        content['pathName'] = input()
        print('\nPath changed to', content['pathName'], '\n')
    else:
        print('Invalid option.\n')



    

