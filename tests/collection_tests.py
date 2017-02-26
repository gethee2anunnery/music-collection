from nose.tools import *
from collection.collection import Collection, Album
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestCollection(object):
    @classmethod
    def setup_class(klass):
        print "SETUP"
        klass.collection = Collection(raw_input=False)



    @classmethod
    def teardown_class(klass):
        print "TEARDOWN"

    def call_command(self, string_input):
        return self.collection.build_kwargs(string_input)

    def test_add_album(self):
        # add an album with valid input
        self.collection.add_album("Ride the Lightning", "Metallica")
        assert_equal(self.collection.album_count(), 1)


        # add an album with 3 params

        # add an album with 1 param


        # add an album with weird characters

        # add an album with no quotes

        # add an album and verify count

    @raises(Exception)
    def test_album_duplicate(self):
        self.collection.add_album("Ride the Lightning", "Metallica")

    def test_play_album(self):
        print "play albums"
        # play an album

        # play an album that hasn't been added yet

        # play an album without quotes

    def test_show_albums(self):
        print "list albums"

        #show all

        #show unplayed

        #show played

        #show unplayed by artist

        #show played by artist

        #test that status doesn't show up if in param

    def test_commands(self):
        print "testing commands"
        # pass an invalid command



