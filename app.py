#!/usr/bin/env python

import cgi
import cgitb
cgitb.enable()

import tic_tac_toe

def begin_game(human_letter):
    if(human_letter in ('X','O')):
        return tic_tac_toe.begin_game(human_letter)
    return 'What? How did you choose {0}?'.format(human_letter)

def next_turn(human_letter, square, progress):
    return tic_tac_toe.next_turn(human_letter, square, progress)

if __name__ == '__main__':
    query = cgi.FieldStorage()
    human_letter = query.getfirst('pl')
    progress = query.getfirst('pg')
    square = query.getfirst('sq')
    print "Content-type: text/html\n"
    if progress:
        print next_turn(human_letter, square, progress)
    elif human_letter != None:
        print begin_game(human_letter)
    else:
        print 'No letter chosen.'
