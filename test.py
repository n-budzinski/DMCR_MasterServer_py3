import unittest
from utils import get_file, check_alpha, reverse_address


class TestFile(unittest.TestCase):
    def testload(self):
        """
        Test get_file
        """
        file = "cancel.dcml"
        result = get_file(file)
        self.assertMultiLineEqual(result, "<NGDLG>\n<NGDLG>")

class TestAlpha(unittest.TestCase):

    def testalphafalse(self):
        """
        Test check_alpha "!@#!@$"
        """
        string = "!@s12@$"
        result = check_alpha(string)
        self.assertFalse(result)

    def testalphatrue(self):
        """
        Test check_alpha
        """
        string = "12IO1adm"
        result = check_alpha(string)
        self.assertTrue(result)

class TestFile(unittest.TestCase):
    def testreverseaddress(self):
        """
        Test reverse_address
        """
        address = ["4.3.2.1"]
        result = reverse_address(address)
        self.assertMultiLineEqual('{:x}'.format(int(result)), "1020304")

if __name__ == '__main__':
    unittest.main()