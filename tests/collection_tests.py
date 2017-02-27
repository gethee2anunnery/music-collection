from nose.tools import *
from collection.collection import Collection, Album
from .contextmanager import captured_output
from music import CollectionCommandLineParser
from nose.tools import assert_equal, assert_in
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
import sys


ALBUMS = [
    {"artist":"Metallica", "title":"Ride the Lightning"},
    {"artist":"Beastie Boys", "title":"Pauls Boutique"},
    {"artist":"Beastie Boys", "title":"Licensed to Ill"},
    {"artist":"Pink Floyd", "title":"The Dark Side of the Moon"},
]
NUMBER_PLAYED = 2


class TestCollection(object):
    @classmethod
    def setup_class(klass):
        print "SETUP"
        klass.parser = CollectionCommandLineParser(raw_input=False)
        klass.album_data = ALBUMS
        klass.play_index = NUMBER_PLAYED

    @classmethod
    def teardown_class(klass):
        print "TEARDOWN"

    def call_command(self, string_input):
        # call build kwargs with output capture mixin
        with captured_output() as (out, err):
            self.parser.build_kwargs(string_input)
        output = out.getvalue().rstrip()
        return output

    def test_add(self):
        for album in self.album_data:
            command_str = 'add "%s" "%s"' % (album['title'], album['artist'])
            output = self.call_command(command_str)
            expected_output = 'Added "%s" by %s' %(album['title'], album['artist'])
            assert_equal(output, expected_output)

        # the length of the collection should now match
        # the length of the test data list
        album_count = self.parser.collection.album_count()
        assert_equal(album_count, len(self.album_data))

    def test_play(self):
        for album in self.album_data[:self.play_index]:
            command_str = 'Play "%s"' % (album['title'])
            output = self.call_command(command_str)
            expected_output = 'You are listening to "%s"' %(album['title'])
            assert_equal(output, expected_output)

    def test_play_unadded(self):
        command_str = 'Play "%s"' % ("New Album")
        output = self.call_command(command_str)
        expected_output = 'You must add "New Album" before playing.'
        assert_equal(expected_output, output)


    def test_show_all(self):
        command_str = 'show all'
        output = self.call_command(command_str)
        output_pieces = output.split('\n')

        # loop through the output and compare if to the
        # list of test album data
        for i, a in enumerate(output_pieces, start=0):
            title, artist = self.album_data[i]['title'], self.album_data[i]['artist']
            assert_in(title, a)
            assert_in(artist, a)

            # the first x albums should be played,
            # the rest should be unplayed
            if i < self.play_index:
                assert_in('played', a)
            else:
                assert_in('unplayed', a)

        # compare the number of albums in collection
        # to the number of lines in the output
        album_count = self.parser.collection.album_count()
        assert_equal(album_count, len(output_pieces))


    def test_show_played(self):
        # compare the number of played albums in collection
        # to the number of lines in the output
        command_str = 'show played'
        output = self.call_command(command_str)
        output_pieces = output.split('\n')
        played_count = self.parser.collection.album_count(played=True,
                                                          unplayed=False)
        assert_equal(played_count, len(output_pieces))

    def test_show_unplayed(self):
        command_str = 'show unplayed'
        output = self.call_command(command_str)
        output_pieces = output.split('\n')
        unplayed_count = self.parser.collection.album_count(played=False,
                                                          unplayed=True)
        assert_equal(unplayed_count, len(output_pieces))



