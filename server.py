#usr/bin/env /usr/local/bin/python  
# encoding: utf-8
import os
import socket
import tarfile
import commands

PORT = 10018
HOST ='192.168.30.12'

socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST,PORT))
socket.listen(5)
BUF_SIZE = 1024

def accept_file():
    conn, addr = socket.accept()
    print 'connecting from:',addr
 
    buffer  = conn.recv(BUF_SIZE)
    file = buffer.split('\0')[0]
    print file
    conn.send('ready')
 
    #conn, addr = socket.accept()
    fname = open(file, 'wb')
    while True:
       strng = conn.recv(4096)
       if not strng:
          fname.close()
          conn.close()
          print "recv file success"
          break
       else:
          fname.write(strng)
 
    if False == os.path.isfile(file):
      print "error,recv file failed"
      
    #print  file
    return file    

def unpackage(file):
    dir = file.split('.')[0]
    os.mkdir(dir)
    t = tarfile.open(file, "r:")  
    t.extractall(dir)  
    t.close()
    
def do_restore(file):
    
    tarfile = file.split('/',2)[2]
    name = tarfile.split('.',2)[0]
    #print name
    
    base_image = 'busybox'
    #delete_op = 'docker rm -f '+name+ ' >/dev/null 2>&1'
    #print delete_op
    #os.system(delete_op)
    
    create_op = 'docker create --name='+name+' '+base_image
    ret,id = commands.getstatusoutput(create_op)
    #print id
       
    restore_op ='docker restore --force=true --image-dir=/tmp/'+name+' '+id
    print restore_op
    os.system(restore_op)

if __name__ == '__main__':  
  
  #while True:
     file = accept_file()
     unpackage(file)
     do_restore(file)

   
