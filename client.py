#!/usr/bin/env /usr/local/bin/python  
# encoding: utf-8  

import os
import socket
import tarfile

PORT = 10018
HOST=''
image_name=''

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_name():
    print 'please input the docker image you want to migrate'
    global image_name
    image_name = raw_input("name: ")
    
    print 'please input the destionation ip'
    global HOST
    HOST = raw_input("host:")

    checkpoint_sh = 'docker checkpoint --image-dir=/tmp/'+image_name+' '+image_name
    os.system(checkpoint_sh)

#package.
def tar_file():
    #create file path.
    file_path = '/tmp/'+image_name #eg: /tmp/mytest
    
    if False == os.path.exists(file_path):
        print "error ,file dir(%s) not exist"% file_path
        
    full_name = '/tmp/'+image_name+'.tar' #eg: /tmp/mytest.tar
    
    tar_file = tarfile.open(full_name,'w')
    for root,dir,files in os.walk(file_path):  
         for file in files:  
                 fullpath=os.path.join(root,file)  
                 tar_file.add(fullpath,arcname=file) 

    tar_file.close()  
    
    if False == os.path.isfile(full_name):
         print "error,tar failed"

def send_file():  
    
    try:
        socket.connect((HOST,PORT))
    except Exception,e:
	print 'Error connecting to server:%s'%e
    
    full_name = '/tmp/'+image_name+'.tar' #eg: /tmp/mytest.tar
    
    print "send:"+full_name

    try:
    	socket.send(full_name,1024)
    	data = socket.recv(1024)
    except Exception,e:
	print 'Error,socket send or recv file name failed:%s'% e
        return 
  
    if data == 'ready': 
    	 file_to_send = open(full_name, 'rb')
   	 while True:
    		data = file_to_send.read(4096)
    		if not data:
	      		break;

    		socket.sendall(data)      
     
    file_to_send.close()
    socket.send('',1024)
    socket.close()
    
if __name__ == '__main__':  
    '''
    - get the input
    - checkpoint then get the image
    - tar file
    - send the file
    '''
    get_name()
    tar_file()
    send_file()
    exit()
    
