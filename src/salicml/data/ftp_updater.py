#!/usr/bin/env python

import os

from ftplib import FTP
from salicml.data.loader import FILE_EXTENSION

CREDENTIALS = {
    'FTP_USER': os.environ.get('FTP_USER', ''),
    'FTP_PASSWORD': os.environ.get('FTP_PASSWORD', ''),
}


def execute_upload_pickle(source_file):
    if not source_file.endswith(FILE_EXTENSION):
        exit('Can\'t upload \'{}\'. Only files with format {} are '
             'allowed.'.format(source_file, FILE_EXTENSION))

    ftp = init_ftp()
    dest_file_path = 'raw/' + os.path.basename(source_file)
    save_file_in_ftp(ftp, source_file, dest_file_path)
    ftp.quit()


def save_file_in_ftp(ftp, source_file_path, dest_file_path):
    dest_filename = os.path.basename(dest_file_path)
    dest_dirname = os.path.dirname(dest_file_path)
    ftp.cwd(dest_dirname)
    with open(source_file_path, 'rb') as f_send:
        print('Uploading file \'{}\'...'.format(source_file_path))
        ftp.storbinary('STOR {}'.format(dest_filename), f_send)
        ftp.sendcmd('SITE CHMOD 644 ' + dest_filename)
        print('File \'{}\' saved in \'ftp/{}\''.format(source_file_path,
                                                       dest_file_path))


def init_ftp():
    host = '138.68.73.247'
    user = CREDENTIALS['FTP_USER']
    passwd = CREDENTIALS['FTP_PASSWORD']

    ftp = FTP(host)
    ftp.login(user, passwd)

    return ftp
