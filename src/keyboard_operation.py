#
# what: define kbhit, getch
# reference: https://westgate-lab.hatenablog.com/entry/2019/12/28/123451
#

import sys, termios, atexit
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

#
# what: check for input from keyboard
#
def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []

#
# what: input from keyboard without echo
#
def getch():
    return sys.stdin.read(1)

atexit.register(set_normal_term)
set_curses_term()
