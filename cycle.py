"""
Cycle Program for Spooler Thermal Testing
Daniel Lefebvre
Jan 14, 2014
"""

import time
import sys, os
from select import select   

def cycle(cli, *args):
    max_vel = 600
    cli.set("S-SPL-DEF-VEL", str(max_vel))
    
    enough = input("Is there sufficient filament on both spools? (y/n): "
    if enough != y
        sys.exit("Oops! Try Again!")
    print “Good to go!”
    
    len = input('How many estimated meters to cycle: ')
    len = -1.0 * float(len)
    total = input('How many cycles in all: ')
    total = float(total)
    vel = 0
    
    cli.set("S-CTRL-MODE", "3")
    len1 = len2 = dlen = 0
    interval = 0.1
    print_update = 0.5    # interval between printed updates (sec)
    n = i = 1

    while (i <= total):
        while (dlen > len):
            vel_in = str(-1 * vel)      
            cli.set("S-SPL-VEL-CMD", vel_in)
            time.sleep(interval)
            len2 = cli.get("LENGTH-PAID")
            dlen = round(len2 - len1, 3)
            n = n + 1
            if (n * interval == print_update): 
                n = 0
                print "   Cycle %i: %s m, %s rad/s" % (i, str(dlen), vel_in)
            if (dlen <= len * 3/4):
                max_vel = 300
            if (dlen <= len * 9/10):
                max_vel = 150
            if kbhit():
                print "Cycle aborted"
                break

        cli.set("S-SPL-VEL-CMD", "0")
        max_vel = 600
        vel = n = 0

        while (dlen < 0):
            vel = min(vel + 20, max_vel)
            vel_out = str(vel)
            cli.set("S-SPL-VEL-CMD", vel_out)
            time.sleep(interval)
            len2 = cli.get("LENGTH-PAID")
            dlen = round(len2 - len1, 3)
            n = n + 1
            if (n * interval == print_update): 
                n = 0
                print "   Cycle %i: %s m, %s rad/s" % (i, str(dlen), vel_out)
            if (dlen >= len * 1/4):
                max_vel = 300
            if (dlen >= len * 1/10):
                max_vel = 150
            if kbhit():
                print "Cycle aborted"
                break
        max_vel = 600
        dlen = vel = n = 0
        i = i + 1

    cli.set("S-SPL-VEL-CMD", "0")
    cli.set("S-CTRL-MODE", "6")
    #print('After: %s\n' % time.ctime())


def wind(cli, *args):
    max_vel = 600
    cli.set("S-SPL-DEF-VEL", str(max_vel))
    print_update = 1.0    # interval between printed updates (sec)
    
    len = input('How many meters to wind on spool: ')
    len = float(len)
    print "Hit Enter to abort"
    
    cli.set("S-CTRL-MODE", "3")
    len1 = len2 = dlen = vel = 0
    len1 = cli.get("LENGTH-PAID")
    interval = 0.1
    n = 1
 
    while (dlen < len):
        vel = min(vel + 20, max_vel)
        svel = str(-1 * vel)
        cli.set("S-SPL-VEL-CMD", svel)
        time.sleep(interval)
        len2 = cli.get("LENGTH-PAID")
        dlen = -1.0 * round(len2 - len1, 3) # inverted to reflect positive length wound
        n = n + 1
        if (n * interval == print_update): 
            n = 0
            print "Wound on spool: %s m" % (str(dlen))
        if kbhit():
            print "Winding aborted"
            break

    print "Total wound: %s m" % (str(dlen))
    cli.set("S-SPL-VEL-CMD", "0")
    cli.set("S-CTRL-MODE", "6")
    #print('After: %s\n' % time.ctime())

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr <> []
