#!/usr/local/bin/python

import sys
import shlex
from collection.collection import Collection


class CollectionCommandLineParser(object):
    VALID_COMMANDS = ['add', 'show', 'play', 'quit']

    def start(self):
        print 'Welcome to your music collection!'
        self.prompt_input()

    def prompt_input(self):
        use_raw_input = self.kwargs.get('raw_input', True)
        if use_raw_input:
            command = raw_input("> ")
            if command == 'quit':
                print "Bye!"
                sys.exit()
            self.build_kwargs(command)
        else:
            # skip inputs for tests
            pass

    def build_kwargs(self, string_input):
        # build the command kwargs from the input
        split_string =  [s.strip() for s in shlex.split(string_input)]
        command = split_string[0].lower()
        kwargs = {'cmd':command, 'args':split_string[1:]}
        self.parse_kwargs_to_command(**kwargs)

    def parse_kwargs_to_command(self, **kwargs):
        # parse the command from its 'arguments' and
        # pass to a handler function
        command = kwargs.get('cmd')
        args = kwargs.get('args')
        try:
            self.handle_command(command, *args)
        except Exception as e:
            print e
            self.prompt_input()

    def handle_command(self, command, *args):
        # validate against the list of available commands
        # and call the corresponding function
        if command in self.VALID_COMMANDS:
            if command == 'add':
                self.collection.add_album(*args)
            elif command == 'show':
                self.collection.show_albums(*args)
            elif command == 'play':
                self.collection.play_album(*args)
            self.prompt_input()
        else:
            raise Exception("That is not a valid command. "\
              "Commands are: %s" %(', '.join(self.VALID_COMMANDS)))


    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.collection = Collection()


def main(**kwargs):
    parser = CollectionCommandLineParser(**kwargs)
    parser.start()


if __name__ == '__main__':
    main(raw_input=True)


