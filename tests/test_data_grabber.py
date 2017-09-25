import os
import unittest
import sys
sys.path.append("../")
import data_grabber


class TestDataGrabber(unittest.TestCase):

    @unittest.expectedFailure
    def test_init_empty(self):
        dg = data_grabber.DataGrabber()

    def test_init_arguments(self):
        dg = data_grabber.DataGrabber(['-f'])

    def test_argument_help(self):
        with self.assertRaises(SystemExit) as cm:
            dg = data_grabber.DataGrabber(['-h'])
        self.assertEqual(cm.exception.code, data_grabber.Codes.SUCCESS)

    def test_wrong_path(self):
        dg = data_grabber.DataGrabber(['-i=c:\blablabla'])
        with self.assertRaises(SystemExit) as cm:
            dg.get_url_list()
        self.assertEqual(cm.exception.code, data_grabber.Codes.PATH_NOT_VALID)

    def test_connection_problem(self):
        dg = data_grabber.DataGrabber([])
        with self.assertRaises(SystemExit) as cm:
            dg.get_file_save_local('http://test', os.getcwd())
        self.assertEqual(cm.exception.code, data_grabber.Codes.CONNECTION_PROBLEM)

    def test_file_exists(self):
        url = 'https://pixabay.com/static/uploads/photo/2012/04/12/23/47/car-30984_960_720.png'
        for i in range(2):
            dg = data_grabber.DataGrabber(['-k'])
            with self.assertRaises(SystemExit) as cm:
                dg.get_url_list()
                dg.get_file_save_local(url, os.getcwd())
        self.assertEqual(cm.exception.code, data_grabber.Codes.FILE_EXISTS)

    def test_file_automatic_naming(self):
        url = 'https://pixabay.com/static/uploads/photo/2012/04/12/23/47/car-30984_960_720.png'
        for i in range(2):
            dg = data_grabber.DataGrabber([''])
            dg.get_url_list()
            dg.get_file_save_local(url, dg.generate_file_name(url))

if __name__ == '__main__':
    unittest.main()