#!/usr/bin/env /usr/local/bin/python  
# encoding: utf-8  

import os
import socket
import tarfile

PORT = 10018
HOST= '192.168.30.12'

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST,PORT))
BUF_SIZE = 1024

def get_name():
    print 'please input the docker image you want to migrate'
    name = raw_input("name: ")
    
    checkpoint_sh = 'docker checkpoint --image-dir=/tmp/'+name+' '+name
    os.system(checkpoint_sh)
    return name

def tar_file(name):
    #create file path.
    PATH = '/tmp/'+name

    if False == os.path.exists(PATH):
        print "error,directory not exis"
        
    #create the tar file.
    fname = '/tmp/'+name+'.tar'
    
    tar_file = tarfile.open(fname,'w')
    for root,dir,files in os.walk(PATH):  
         for file in files:  
                 fullpath=os.path.join(root,file)  
                 tar_file.add(fullpath,arcname=file)  
    tar_file.close()  
    
    if False == os.path.isfile(fname):
         print "error,tar failed"

    return fname

def send_file(file):  
    #print "send:"+file
    
    #first send the file name
    socket.send(file,BUF_SIZE)
    
    #sync with server side.
    data = socket.recv(BUF_SIZE)
    
    if data == 'ready': 
    	 file_to_send = open(file, 'rb')
     	 while True:
    		data = file_to_send.read(4096)
    		if not data:
	      		break;
    		socket.sendall(data)      
     
    file_to_send.close()
    socket.send('',BUF_SIZE)
    socket.close()
    
if __name__ == '__main__': 
    image_name = get_name()
    file = tar_file(image_name)
    send_file(file)
    exit()
    
