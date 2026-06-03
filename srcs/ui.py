from ursina import *

def create_ui():
    play_button = Button(
        text='Play',
        scale=(0.1, 0.1),
        position=(-0.7, 0.4),
    )

    shuffle_button = Button(
        text='Shuffle',
        scale=(0.1, 0.1),
        position=(-0.55, 0.4),
    )

    return play_button, shuffle_button