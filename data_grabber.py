#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import sys
import os
import time


class Codes():
    """ Enumeration replacement """
    SUCCESS = 0
    CONNECTION_PROBLEM = 1
    PATH_NOT_VALID = 2
    FILE_EXISTS = 3


class DataGrabber():
    """ class that can download links from www """

    def __init__(self, arguments):
        ''' default input_path and output_path is the current working directory until
            it will be overwritten through arguments, see below '''
        self.input_path, self.output_path = os.getcwd(), os.getcwd()
        self.overwrite, self.keepname = False, False
        self.single_file_only = False
        self.list_count = 0
        self.read_bytes = 0
        self.file_count = 0
        self.begin_time = time.time()
        if(len(arguments) > 0):
            self.parse_arguments(arguments)

    def get_url_list(self):
        ''' will extract an url list from text files which will lay in given folder '''
        url_list = []
        # check for existing folder
        if(os.path.isdir(self.input_path)):
            # get a list of all files in given folder
            list_files = os.listdir(self.input_path)
            # iterate through all files in the folder
            for file in list_files:
                # only .txt will be read yet but it is flexible to extend
                if(file.endswith('.txt')):
                    url_list.extend(self.read_text_files(open(self.input_path + '/' + file, 'rb')))
            self.list_count = len(url_list)
            return url_list
        elif(self.single_file_only):
            if(self.input_path.endswith('.txt')):
                url_list.extend(self.read_text_files(open(self.input_path, 'rb')))
            self.list_count = len(url_list)
            return url_list
        else:
            print('Please verify the given input_path: {0}'.format(self.input_path))
            sys.exit(Codes.PATH_NOT_VALID)

    def read_text_files(self, temp_url_list):
        ''' read url's from opened files '''
        # read all lines in txt file and save in url_list
        temp_list = temp_url_list.readlines()
        return temp_list

    def store_file(self, path, file_download):
        ''' store the file to path '''
        file_data = file_download.read()
        self.generate_statistics(len(file_data))
        with open(path, 'wb') as output:
            output.write(file_data)

    def get_file_save_local(self, input_url, output_file):
        ''' save the grabbed file with the generated or extracted file name '''
        try:
            file_download = urllib2.urlopen(input_url)
            if(self.overwrite):
                self.store_file(output_file, file_download)
            elif(os.path.exists(output_file)):
                print('Please delete existing file or use "--force" | "-f"!')
                sys.exit(Codes.FILE_EXISTS)
        except Exception as e:
            print('Exception occured: {0}\nPlease check url and connectivity!'.format(str(e)))
            sys.exit(Codes.CONNECTION_PROBLEM)

    def generate_file_name(self, temp_url):
        ''' generate the file name with timestamp or will use the name from url '''
        if(self.keepname):
            local_file_name = temp_url.replace('\r\n', '')[temp_url.rfind('/') + 1:]
        else:
            file_extension = temp_url.replace('\r\n', '')[temp_url.rfind('.'):]
            # extract the file extension, so it is more general for any file
            local_file_name = 'file-{0}{1}'.format(time.time(), file_extension)
        return local_file_name

    def generate_statistics(self, read_bytes):
        ''' generate some statistics to show the user '''
        self.read_bytes += read_bytes
        self.file_count += 1

    def show_statistics(self):
        ''' shows information over data / files and elapsed time '''
        print('\nReceived bytes: {0:>10} Bytes\n'.format(self.read_bytes) +
              'Elapsed time: {0:>10.3f} sec\n'.format(time.time() - self.begin_time) +
              'Files received: {0:>10}\n'.format(self.file_count) +
              'Work finished!')

    def parse_arguments(self, arguments):
        ''' parse given arguments, do it case insensitive '''
        for in_parameter in arguments:
            # only single what will be parsed
            param = in_parameter.lower()
            if('--single' in param):
                self.single_file_only = True
                self.input_path = (in_parameter.split('='))[1]
            # will set the inpath, where the text files are lay
            if('--inpath' in param):
                self.input_path = (in_parameter.split('='))[1]
            # will set the outpath where the data files will be stored
            if('--outpath' in param):
                self.output_path = (in_parameter.split('='))[1]
            # keeps the original names from url and parse it correctly
            if('--keepname' in param):
                self.keepname = True
            # will force to overwrite, if stored file exists
            if('--force' in param):
                self.overwrite = True
            # give a help about all possible arguments
            if('--help' in param):
                self.show_help()

    def show_help(self):
        ''' display the possible arguments at commandline '''
        print('possible arguemnts are:\n' +
              '--single=<filepath>:\tsingle file must be given\n' +
              '--inpath=<path>:\tset the path where the txt files with url\'s lays\n' +
              '--outpath=<path>:\tset the path where the data will be stored\n'
              '--keepname:\tkeep the name of data from url\n' +
              '--force:\twill overwrite date if data with same name is available\n' +
              '--help:\tshows the help with all parameters')
        sys.exit(Codes.SUCCESS)


def progress_bar(current, maximum):
    ''' adds a progress bar for multiple url's '''
    step = 100 / maximum * current
    sys.stdout.write(('=' * int(step / 2)) + ('' * (100 - step)) + ("\r [ %d" %step + "% ] "))
    sys.stdout.flush()

if __name__ == '__main__':
    dg = DataGrabber(sys.argv[1:])
    for temp_url in dg.get_url_list():
        # download the file and store it to given folder
        dg.get_file_save_local(temp_url, dg.generate_file_name(temp_url))
        progress_bar(dg.file_count, dg.list_count)
    # show 100 % progress
    progress_bar(100, 100)
    dg.show_statistics()
    sys.exit(Codes.SUCCESS)
