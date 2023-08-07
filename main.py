"""Main file of the app, containing the overall structure of the application."""

import curses
import json
from curses import wrapper
from os import path

from easygui import diropenbox


def main(stdsrc):
    # Initialization of the different colors used in the application
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)
    BLUE = curses.color_pair(3)

    # We prompt the user to select the data directory
    dir_path = diropenbox(title="Sélectionnez le dossier téléchargé depuis Instagram")

    # Path to the interesting files
    followers_path = path.join(dir_path, 'followers_and_following', 'followers.json')
    following_path = path.join(dir_path, 'followers_and_following', 'following.json')

    stdsrc.clear()

    # We first check that the paths are correct
    if not (path.isfile(followers_path) and path.isfile(following_path)):
        stdsrc.addstr(0, 0, 'Le dossier spécifié est incorrect', RED)
    
    else:
        stdsrc.addstr(0, 0, 'Chemin d\'accès correct', GREEN)
        
        # We retrieve the data stored inside the files
        with open(followers_path, 'r') as file:
            followers = json.load(file)
        
        with open(following_path, 'r') as file:
            following = json.load(file)
        
        # We create lists only containing the people's names
        followers_names, following_names = [], []

        for user in followers:
            followers_names.append(user['string_list_data'][0]['value'])
        
        for user in following['relationships_following']:
            following_names.append(user['string_list_data'][0]['value'])
        
        # We create the three lists of individuals
        snobbers, fans, normal = [], [], []

        for name in followers_names:
            if name in following_names:
                normal.append(name)
            
            else:
                fans.append(name)
        
        for name in following_names:
            if name not in followers_names:
                snobbers.append(name)
        
        # We display the result
        result_pad = curses.newpad(1000, 1000)
        stdsrc.refresh()

        height = max(len(normal), len(fans), len(snobbers))

        stdsrc.addstr(2, 0, 'Normal', curses.A_UNDERLINE)
        stdsrc.addstr(2, 40, 'Fans', curses.A_UNDERLINE)
        stdsrc.addstr(2, 80, 'Snobbers', curses.A_UNDERLINE)

        for h in range(0, height):
            if h < len(normal):
                result_pad.addstr(h, 0, normal[h], BLUE)
            
            if h < len(fans):
                result_pad.addstr(h, 40, fans[h], GREEN)
            
            if h < len(snobbers):
                result_pad.addstr(h, 80, snobbers[h], RED)

    # We copy the result inside a text file, so that the user can copy the names...
    with open(path.join(dir_path, 'results.txt'), 'w') as file:
        file.write('Normal :\n\n') # We first write the normal people
        file.writelines('\n'.join(normal))

        file.write('\n\nFans :\n\n') # Then the fans
        file.writelines('\n'.join(fans))

        file.write('\n\nSnobbers :\n\n') # And finally the snobbers
        file.writelines('\n'.join(snobbers))

    # Scrolling effect inside the pad
    current_key, inner_y = curses.KEY_MIN, 0

    while current_key != 10:
        # We refresh the screen
        result_pad.refresh(inner_y, 0, 4, 0, 20, 150)
        stdsrc.refresh()

        # We wait for the user to enter something
        current_key = stdsrc.getch()

        # We update the choice if it is an arrow key
        if current_key == 450:
            inner_y = max(0, inner_y - 5)
        
        elif current_key == 456:
            inner_y = min(height, inner_y + 5)

# <stdsrc> variable is passed to <main> function here
wrapper(main)