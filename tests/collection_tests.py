from nose.tools import *
from collection.collection import Collection
from .contextmanager import captured_output
from music import CollectionCommandLineParser
from nose.tools import assert_equal, assert_in
import sys


ALBUMS = [
    {"artist": "Metallica", "title": "Ride the Lightning"},
    {"artist": "Beastie Boys", "title": "Pauls Boutique"},
    {"artist": "Beastie Boys", "title": "Licensed to Ill"},
    {"artist": "Pink Floyd", "title": "The Dark Side of the Moon"},
]
NUMBER_PLAYED = 2
SHOW_ARTIST = "Beastie Boys"


class TestCollection(object):
    @classmethod
    def setup_class(klass):
        klass.parser = CollectionCommandLineParser(raw_input=False)
        klass.album_data = ALBUMS
        klass.play_index = NUMBER_PLAYED
        klass.show_artist = SHOW_ARTIST

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
            expected_output = 'Added "%s" by %s' % \
                              (album['title'], album['artist'])
            assert_equal(output, expected_output)

        # the length of the collection should now match
        # the length of the test data list
        album_count = self.parser.collection.album_count()
        assert_equal(album_count, len(self.album_data))

    def test_play(self):
        for album in self.album_data[:self.play_index]:
            command_str = 'Play "%s"' % (album['title'])
            output = self.call_command(command_str)
            expected_output = 'You are listening to "%s"' % (album['title'])
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
            title, artist = self.album_data[i]['title'],\
                            self.album_data[i]['artist']
            assert_in(title, a)
            assert_in(artist, a)

        # compare the number of albums in collection
        # to the number of lines in the output
        album_count = self.parser.collection.album_count()
        assert_equal(album_count, len(output_pieces))

        # compare to test data
        assert_equal(album_count, len(self.album_data))

    def test_show_played(self):
        # compare the number of played albums in collection
        # to the number of lines in the output
        command_str = 'show played'
        output = self.call_command(command_str)
        output_pieces = output.split('\n')
        played_count = self.parser.collection.album_count(played=True,
                                                          unplayed=False)
        # compared to output
        assert_equal(played_count, len(output_pieces))

        # compared to test data
        assert_equal(played_count, self.play_index)

    def test_show_unplayed(self):
        command_str = 'show unplayed'
        output = self.call_command(command_str)
        output_pieces = output.split('\n')
        unplayed_count = self.parser.collection.album_count(played=False,
                                                            unplayed=True)
        # compared to output
        assert_equal(unplayed_count, len(output_pieces))

        # compared to test data
        assert_equal(unplayed_count, len(self.album_data) - self.play_index)

    def test_invalid_show_arg(self):
        # pass an invalid argument to 'show'
        command_str = 'show bananas'
        output = self.call_command(command_str)
        assert_in('bananas is not a valid argument', output)

    def test_show_all_with_artist(self):
        # compare number of artist albums in data
        # to number command all returns
        album_count = len([k for k in self.album_data
                          if k['artist'] == self.show_artist])

        command_str = 'show all by "%s"' % (self.show_artist)
        output = self.call_command(command_str)
        output_pieces = output.split('\n')

        # compare to test data
        assert_equal(len(output_pieces), album_count)

        # compare to collection albums
        all_albums = self.parser.collection\
                         .album_count(artist=self.show_artist)
        assert_equal(all_albums, album_count)

    def test_played_with_artist(self):
        command_str = 'show played by "%s"' % (self.show_artist)
        output = self.call_command(command_str)
        output_pieces = output.split('\n')
        played_count = self.parser.collection\
                                  .album_count(artist=self.show_artist,
                                               played=True,
                                               unplayed=False)
        # compare output to number of played items
        assert_equal(len(output_pieces), played_count)

    def test_unplayed_with_artist(self):
        command_str = 'show unplayed by "%s"' % (self.show_artist)
        output = self.call_command(command_str)
        output_pieces = output.split('\n')
        unplayed_count = self.parser.collection\
                                    .album_count(artist=self.show_artist,
                                                 played=False,
                                                 unplayed=True)
        # compare output to number of unplayed items
        assert_equal(len(output_pieces), unplayed_count)
