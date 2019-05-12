import os
import time
from subprocess import call,check_output,Popen, PIPE

path_to_watch = "./test_folder/"

before = dict([(f, os.stat(path_to_watch+f).st_mtime)
            for f in os.listdir(path_to_watch)])
#dropbx = '/Users/hamidrezaomidvar/Desktop/Dropbox-Uploader/dropbox_uploader.sh'
dropbx = '/home/users/homidvar/Dropbox-Uploader/dropbox_uploader.sh'
f = 'dummy.txt'
while 1:

    time.sleep(1)

    after = dict([(f, os.stat(path_to_watch+f).st_mtime)
                for f in os.listdir(path_to_watch)])

    added = [f for f in after if not f in before]

    modified = [f for f in after if f in before and after[f] != before[f]]


    if added:
        for f in added:
            try:
              lsout=Popen(['lsof',path_to_watch+f],stdout=PIPE, shell=False)
              check_output(["grep",path_to_watch+f], stdin=lsout.stdout, shell=False)
              del after[f]
            except:
              print('Adding')
              bash_cmd = [dropbx, 'upload', path_to_watch+f, '/']
              call(bash_cmd)

    if modified:
        for f in modified:
            
            try:
              lsout=Popen(['lsof',path_to_watch+f],stdout=PIPE, shell=False)
              check_output(["grep",path_to_watch+f], stdin=lsout.stdout, shell=False)
              after[f]=-1
            except:
              print('Modifying')
              bash_cmd = [dropbx, 'delete', '/'+f]
              call(bash_cmd, stdout=open(os.devnull, 'wb'))
              bash_cmd = [dropbx, 'upload',
                          path_to_watch+f, '/']
              call(bash_cmd)

    before = after
