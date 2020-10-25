#!/usr/bin/env python3

import selectors
import sys
import socket
import traceback

import libclient

sel = selectors.DefaultSelector()

def create_request(action, content):
    return dict(
        type="text/json",
        encoding="utf-8",
        content=content
    )

def start_connection(host, port, request):
    addr = (host, port)
    print('starting connection to', addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action = None
pathName = None
bucketName = None
fileName = None
fileData = None

while True:
    print('Enter action number:\n')
    print('1. getPath')
    print('2. createBucket')
    print('3. bucketExists')
    print('4. listBuckets')
    print('5. deleteBucket')
    print('6. uploadFile')
    print('7. fileExists')
    print('8. fileList')
    print('9. downloadFile')
    print('10. deleteFile')
    print('--> ', end='')
    number = input()

    print('')

    if number == '1':
        action = 'getPath'
        print('Enter bucket pathName: ', end="")
        pathName = input()
    elif number == '2':
        action = 'createBucket'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
    elif number == '3':
        action = 'bucketExists'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
    elif number == '4':
        action = 'listBuckets'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        break
    elif number == '5':
        action = 'deleteBucket'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
    elif number == '6':
        action = 'uploadFile'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
        print('Enter file name: ', end="")
        fileName = input()
        print('Enter file data: ', end="")
        fileData = input()
    elif number == '7':
        action = 'fileExists'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
        print('Enter file name: ', end="")
        fileName = input()
    elif number == '8':
        action = 'listFiles'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
    elif number == '9':
        action = 'downloadFile'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
        print('Enter file name: ', end="")
        fileName = input()
    elif number == '10':
        action = 'deleteFile'
        print('Enter bucket pathName: ', end="")
        pathName = input()
        print('Enter bucket name: ', end="")
        bucketName = input()
        print('Enter file name: ', end="")
        fileName = input()
        break
    else:
        print('Invalid option.\n')

content = dict(action=action, pathName=pathName, bucketName=bucketName, fileName=fileName, fileData=fileData)
request = create_request(action, content)

start_connection(host, port, request)

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
    

