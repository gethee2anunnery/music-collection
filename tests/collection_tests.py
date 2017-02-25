from nose.tools import *
from .collection import collection

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"
