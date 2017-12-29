#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import sys
import filecmp
import time
import shutil
import subprocess
        
class UpdateProgram(object):
    def __init__(self, targetpath, sourcepath, backuppath, namelist):
        self.namelist = []
        self.targetpath = targetpath
        self.sourcepath = sourcepath
        self.backuppath = backuppath
        self.namelist = namelist
    def is_file_exist(self, name):
        return os.path.isfile(name)

    def is_dir_exist(self, path):
        if self.is_file_exist(path) == True:
            return False
        return os.path.exists(path)

    def is_file_equal(self, sourcefile, comparefile):
        if not self.is_file_exist(sourcefile) or not self.is_file_exist(comparefile):
            return False
        return filecmp.cmp(sourcefile, comparefile)

    def check_to_update(self):
        error = False
        toUpdate = False
        if not self.is_dir_exist(self.sourcepath):
            print 'the update path:%s not exist ' % self.sourcepath
            error = True
            return toUpdate, error
        if not self.is_dir_exist(self.targetpath):
            print 'the program path:%s not exist ' % self.targetpath
            error = True
            return toUpdate, error
        if  len(self.namelist) == 0 or self.targetpath == "" or self.sourcepath == "" or self.backuppath == "":
            error = True;
            print 'the params is error, please check the params '
            return toUpdate, error
        
        for name in self.namelist:
            updatefile = os.path.join(self.sourcepath,name)
            programfile = os.path.join(self.targetpath,name)
            if not self.is_file_exist(updatefile):
                print 'the update file:%s is not exist' % updatefile
                error = True
                return toUpdate, error
            if self.is_file_equal(updatefile, programfile):
                continue
            else:
                toUpdate = True
        return toUpdate, error

    def update_program(self):
        updateTime = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))     
        if not self.is_dir_exist(self.backuppath):
            try:
                os.mkdir(self.backuppath)
            except Exception as e:
                print e
                return False
            
        for name in self.namelist:
            updatefile = os.path.join(self.sourcepath,name)
            programfile = os.path.join(self.targetpath,name)
            backupfile = os.path.join(self.backuppath, name+updateTime)
            if self.is_file_equal(updatefile, programfile):
                continue
            if self.is_file_exist(programfile):
                shutil.move(programfile, backupfile)
            shutil.copy(updatefile, programfile)        
        return True

def xmppserver_update(targetpath, sourcepath, backuppath):
    names = os.listdir(sourcepath)
    if len(names) == 0:
        print 'sourcepath %s has no file ', sourcepath
        return
    print 'you want to update the programs ', names

    
    updateProgram = UpdateProgram(targetpath, sourcepath, backuppath, names)
    (toUpdate, error) = updateProgram.check_to_update()
    if not error:
        if toUpdate:
            try:
                data = subprocess.check_output('supervisorctl stop xmppserver', shell=True)
            except subprocess.CalledProcessError as e:
                print e

            if updateProgram.update_program():
                print 'update the program ok'
            else:
                print 'update the program error'

            try:
                data = subprocess.check_output('supervisorctl start xmppserver', shell=True)
            except subprocess.CalledProcessError as e:
                print e
        else:
            print 'the program is already updated '
    else:
        print 'something is wrong, please check'


def main(args=None, options=None):    
    targetpath = '/root/works/xmppserver'
    sourcepath = '/root/works/program-update/xmppserver-packet-new'
    backuppath = '/root/works/program-update/xmppserver-packet-old'
    xmppserver_update(targetpath, sourcepath, backuppath)



if __name__ == "__main__":
    main()

