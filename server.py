#usr/bin/env /usr/local/bin/python  
# encoding: utf-8
import os
import socket
import tarfile
import commands
import netifaces as ni
socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BUF_SIZE = 1024

full_path=''
name=''

def accept_file():
    
    host= ni.ifaddresses('eth1')[2][0]['addr']
    port = 10018
    socket.bind((host,port))
    socket.listen(5)
   
    conn, addr = socket.accept()
    print 'connecting from:',addr
 
    buffer  = conn.recv(1024)
    global full_path
    full_path = buffer.split('\0')[0]
    print full_path

    global name
    temp = full_path.split('/',2)[2]
    name = temp.split('.',2)[0]
    print name
  
    if True == os.path.isfile(full_path):
	print 'file(%s) is already exist'% full_path
        del_op= 'rm '+ full_path
        os.system(del_op)
  
    dir = full_path.split('.')[0]
    if True == os.path.exists(dir):
	print "directory already exist %s"% dir
	delete_con = 'docker rm -f '+name+ ' >/dev/null 2>&1'
        print delete_con
        os.system(delete_con)
        del_dir = 'rm -fr '+ dir    
        os.system(del_dir)

    conn.send('ready')
    #conn, addr = socket.accept()
    fname = open(full_path, 'wb')
    while True:
    	strng = conn.recv(4096)
    	if not strng:
        	fname.close()
        	conn.close()
        	print "recv file success"
          	break
        else:
        	fname.write(strng)

def unpackage():
    dir = full_path.split('.')[0]
    os.mkdir(dir)

    t = tarfile.open(full_path, "r:")  
    t.extractall(dir)  
    t.close()

def do_restore():
 
    base_image = 'busybox'
    #delete_op = 'docker rm -f '+name+ ' >/dev/null 2>&1'
    #print delete_op
    #os.system(delete_op)
    
    create_op = 'docker create --name='+name+' '+base_image
    #print create_op
    ret,id = commands.getstatusoutput(create_op)
    print id
       
    restore_op ='docker restore --force=true --image-dir=/tmp/'+name+' '+id
    print restore_op
    os.system(restore_op)

if __name__ == '__main__':  
    '''
    - get the filename
    - get the file
    - unpack the file
    - restore the image
    '''
  #while True:
    accept_file()
    unpackage()
    do_restore()
    exit()
