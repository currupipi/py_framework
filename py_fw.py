#! /usr/bin/env python

import os, sys, subprocess, time, re

#Check if you are root
def check_if_root():
    """Exit with 1 if the user is not root
    """
    if os.getuid()!=0:
        sys.exit(1)

#Ensure directroy exists (create it if not)
def forcedir(directory):
    """Ensure directory exists, otherwise tries to create it"""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            return -1

#Check java version
def get_java_version():
    """Gets system default java version"""
    command = "mkfifo temp && java -version 2> temp | grep version temp | awk '{print $3}' && rm temp"
    try:
        output = subprocess.check_output(command, shell=True)
        return output
    except:
        return -1

#Download files from an URL
def download_file(ndk_url, name):
    """Downloads file from url (first param) skiping https certs and saves it with the given name (second param)"""
    command = 'wget --no-check-certificate -O %s %s' %(name, ndk_url)  
    try:
        print "Trying to download the file from %s :\n" %ndk_url
        output = subprocess.check_call(command, shell=True)
        return output
    except subprocess.CalledProcessError, e:
        print "wget failed! :\n", e.output
        sys.exit(1)

#Create tar from file or directory
def tar(path_file, name):
    """Creates a tar + gzip archive from a path to a file or directory(first param) with a give name (second param)
       See also untar(tar_file, path=None)"""
    import tarfile
    try:
        tar = tarfile.open(name, "w:gz")
        tar.add(path_file)
        tar.close()
    except tarCreationError, e:
        error = e
        print error

#Extract a tar file
def untar(tar_file, path=None):
    """Creates a tar + gzip archive from a path to a file or directory(first param) with a give name (second param)
       See also untar(tar_file, path=None)"""
    import tarfile
    if path is None:
        path = os.curdir    
    try:
        tar = tarfile.open(tar_file)
        tar.extractall(path)
        tar.close()
    except tar.ExtractError, e:
        error = e
        print error

#Send email
def mail(subject, bodym, sender, receivers, server):
    """Sends simple email using SMTP
        Example:
            py_fw.mail('Test', 'Sending mail from py_fw', 'me@currupipi.com', 'your_senders@currupipi.com', 'smtp.some.where')
    """
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    if server is None:
        server= 'your_default_smtp'
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receivers
        msg['Subject'] = subject
        body = bodym
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        try:
            server = smtplib.SMTP('some_fancy_server_here')
            server.sendmail(sender, receivers, text)
            print "Successfully sent email"
        except SMTPException:
             print "Error: unable to send email"


#Dump Postgresql
def postgredump(database, user, output):
    """Simple postgresql dump for backups, it needs database name (first param), postgresql user (second param)
       and dump output name (third param) """ 
    import subprocess
    command = "/usr/bin/pg_dump -U %s  %s -f %s" % (user, database, output)
    try:
        subprocess.call(command, shell=True)
    except:
        print 'ERROR: unable to dump postgresql database'


#Delete old stuff
def rotate_backups(bpath, numcopies):
    """Only keep certain number of directories (second param)  in a path (first param), delting recursively old directories """
    dir_list = sorted(os.listdir(bpath), key = os.path.getmtime)
    list_size = len(dir_list)
    if list_size > numcopies:
        import shutil
        rem_dir = dir_list [ :(list_size - numcopies) ]
        for directory in rem_dir:
            shutil.rmtree(directory)



#MAIN PROGRAM
if __name__ == "__main__":
    main()   
