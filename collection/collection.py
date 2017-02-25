#!/usr/local/bin/python

import sys
import shlex

VALID_COMMANDS = ['add', 'show', 'play', 'quit']


class Song(object):

    @property
    def status(self):
        status = 'played' if self.played else 'unplayed'
        return status

    def play(self):
        self.played = True
        print 'You are listening to "%s"' %self.title

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.played = False

    def __str__(self):
        return "%s - %s" %(self.title, self.artist)

class Collection(object):

    def get_song_by_title(self, title):
        #MAY NOT NEED
        return next((x for x in self.songs if x.title == title), None)

    def get_songs(self, **kwargs):
        title = kwargs.pop('title')
        artist = kwargs.pop('artist')
        # make this filterable by artist
        print artist
        print title
        #return next((x for x in self.songs if x.artist == artist), None)

    def start(self):
        print 'Welcome to your music collection!'
        self.prompt_input()

    def get_played(self, **kwargs):
        return [song for song in self.get_songs(**kwargs) if song.played]

    def get_unplayed(self, **kwargs):
        return [song for song in self.get_songs(**kwargs) if not song.played]

    def play_song(self, *args):
        song_title = args[0]
        song = self.get_songs(title=song_title)

        if song:
            song.play()
        else:
            print self.songs
            print "where's the song"

    def show_songs(self, *args):
        print args

    def add_song(self, *args):
        song_title = args[0]
        song_artist = args[-1]
        song_obj = self.get_songs(title=song_title)

        if song_obj:
            print "This song is already in the collection. "\
                   "Please add a different one."
            self.prompt_input()
        else:
            song = Song(song_title, song_artist)
            self.songs.append(song)
            print 'Added "%s" by %s' %(song.title, song.artist)

    def prompt_input(self):
        command = raw_input("> ")
        if command == 'quit':
            print "Bye!"
            sys.exit()
        self.build_kwargs(command)


    def handle_command(self, command, *args):
        if command in VALID_COMMANDS:
            #can i map a kw to a function
            #{action: handler_fcuntion}
            #http://stackoverflow.com/questions/13499824/using-python-map-function-with-keyword-arguments
            if command == 'add':
                self.add_song(*args)
            elif command == 'show':
                self.show_songs(*args)
            elif command == 'play':
                self.play_song(*args)
        else:
            print "That is not a valid command. Commands are: %s" %(', '.join(VALID_COMMANDS))
            self.prompt_input()


    def build_kwargs(self, string_input):
        split_string =  [s.strip() for s in shlex.split(string_input)]
        command = split_string[0].lower()
        kwargs = {'cmd':command, 'args':split_string[1:]}
        self.parse_kwargs_to_command(**kwargs)


    def parse_kwargs_to_command(self, **kwargs):
        command = kwargs.get('cmd')
        args = kwargs.get('args')
        self.handle_command(command, *args)


    def __init__(self):
        self.songs = []
