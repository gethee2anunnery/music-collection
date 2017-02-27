#!/usr/local/bin/python



class Album(object):

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

    def get_album_status(self, album_name):
        album = self.filter_albums_by_kwargs(title=album_name)
        if album:
            return album[0].status

    def filter_albums_by_kwargs(self, **kwargs):
        title = kwargs.pop('title', None)
        artist = kwargs.pop('artist', None)
        played = kwargs.pop('played', True)
        unplayed = kwargs.pop('unplayed', True)
        filtered_list = self.albums

        # filter by artist and title
        if artist:
            filtered_list = [album for album in filtered_list \
                             if album.artist == artist]
        elif title:
            filtered_list = [album for album in filtered_list \
                             if album.title == title]

        # filter by played and unplayed
        if not played:
            filtered_list = [album for album in filtered_list\
                             if not album.played]
        if not unplayed:
            filtered_list = [album for album in filtered_list\
                             if album.played]

        return filtered_list

    def album_count(self, **kwargs):
        return len(self.filter_albums_by_kwargs(**kwargs))


    def play_album(self, *args):
        album_title = args[0]
        album = self.filter_albums_by_kwargs(title=album_title)

        if album:
            album[0].play()
        else:
            raise Exception('You must add "%s" before playing.' % album_title)

    def show_albums(self, *args):

        # parse the args to 'show' and get a filtered list
        inclusion_param = args[0]
        played = inclusion_param == 'all' or inclusion_param == 'played'
        unplayed = inclusion_param == 'all' or inclusion_param == 'unplayed'

        # if we find an artist param to filter by, add that
        artist = args[-1] if args[-1] != args[0] else None

        # get a filtered album list and pass to a
        # printer function or return a message
        albums_to_show = self.filter_albums_by_kwargs(played=played,
                                                      unplayed=unplayed,
                                                      artist=artist)
        if len(albums_to_show) > 0:
            self.print_albums(albums_to_show,
                              played=played,
                              unplayed=unplayed)
        else:
            raise Exception("There are no matching albums to show.")


    def print_albums(self, album_list, **kwargs):
        # print list of albums with played status or not
        played = kwargs.pop('played')
        unplayed = kwargs.pop('unplayed')
        show_status = played != unplayed

        for album in album_list:
            status = "(%s)" % album.status if show_status else ''
            print '"%s" by %s %s' % (album.title, album.artist, status)

    def add_album(self, *args):
        is_valid_input = len(args) == 2

        # if not 2 arguments (title and artist), error
        # else, parse the args and either create and add
        # a new album or raise a duplicate error

        if not is_valid_input:
            raise Exception('Please provide a valid artist and title')
        else:
            album_title = args[0]
            album_artist = args[-1]
            album_obj = self.filter_albums_by_kwargs(title=album_title)

            if album_obj:
                raise Exception("This album is already in the collection. "\
                       "Please add a different one.")
            else:
                album = Album(album_title, album_artist)
                self.albums.append(album)
                print 'Added "%s" by %s' %(album.title, album.artist)


    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.albums = []

