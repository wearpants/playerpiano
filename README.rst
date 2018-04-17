##########################
PlayerPiano
##########################

PlayerPiano amazes your friends by running Python doctests in a fake interactive shell.

See the `PlayerPiano PyPI <https://pypi.org/project/PlayerPiano/>`_ page for more 
info, or this `blog post <https://wearpants.org/petecode/playerpiano-amaze-your-friends/>`_ 
for a demo.

``playerpiano`` plays back a recorded shell session in a terminal.

``recorderpiano`` can be used to record a shell session for later playback.

****************************************
Usage
****************************************
Run ``playerpiano <options> <FILE>``, where FILE is a file containing doctests or the 
name of a module. Do not pass ``mymodule.py`` directly, it will confuse the doctest 
parser. Use ``mymodule`` instead.

Pressing any keys will type source lines, stop at the end of each source block.

Press enter to show the results block.

EOF (^D) will exit the program at the end.

Break (^C) will interrrupt the program immediately.

Options
-------
The ``--color`` option will syntax-highlight source lines. It is currently hard-coded 
for a black background terminal. Use ``--color3`` for Python 3 syntax highlighting.

The ``--no-terminal`` option will disable output on the main terminal. This is less 
than useful at present.

The ``--fifo`` option takes the name of a fifo to duplicate output to. After starting 
playerpiano with this option, you must run ``cat name_of_fifo`` in another terminal before any 
output will be displayed. This is useful when presenting using a projector. Start a second xterm 
& run cat, then put it on the overhead (with the main terminal on your laptop). This allows you to
see what you're doing.
