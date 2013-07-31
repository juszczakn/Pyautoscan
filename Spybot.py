'''
Script for automating the run of Spybot

Last Modified: July 24, 2013
'''

import pywinauto
import time
import sys
from pywinauto import application
from winsound import Beep

print 'Remember, -h or --help for help!\n'
beepFreq = 2500
beepDur = 1000

def beep():
    try:
        Beep(beepFreq, beepDur)
    except:
        print 'Unable to beep... :('

# Default values
args = {'executable':'',
        'uninstall':False}

# Check parameters
if len(sys.argv) > 1:
    for index,arg in enumerate(sys.argv):
        if arg == '-e' or arg == '--executable':
            args['executable'] = sys.argv[index + 1]
        if arg == '-u' or arg == '--uninstall':
            args['uninstall'] = True
        if arg == '-h' or arg == '--help':
            print 'Options are:'
            print '\t-e or --executable <path> | Path to Spybot executable'
            print '\t-u or --uninstall | Uninstall Spybot'
            print '\t-h or --help | This screen'
            sys.exit(-1)


def uninstallSpybot():
    app = application.Application().start_(args['executable'] + ' /verysilent')

    # Wait and try to connect to Uninstall prompt
    dlg = None
    attempts = 5
    while dlg == None and attempts > 0:
        try:
            dlg = app.connect_(title_re='Uninstall Application')
        except:
            attempts -= 1
            time.sleep(1)

    # Prompt did not show up.
    if dlg == None:
        print 'Error uninstalling Spybot'
        beep()
        sys.exit(-1)

    # Wait for uninstall button prompt
    attempts = 10
    while not app.dlg.UninstallButton.Exists():
        attempts -= 1
        time.sleep(1)

    # timeout
    if attempts == 0:
        print 'Unable to uninstall Spybot'
        beep()
        sys.exit(-1)

    # click the prompt to uninstall
    try:
        app.dlg.UninstallButton.Click()
    except:
        beep()
        print 'Error clicking button'

    print 'Spybot successfully uninstalled'
    

# Run Spybot default
def runSpybot():
    app = application.Application().start_(args['executable'] + ' /autoimmunize /autocheck /autofix /autoclose')

    # Wait for popup
    attempts = 100
    while not app['Legal stuffTformLegals'].Exists() and attempts > 0:
        attempts -= 1
        time.sleep(2)

    if attempts == 0:
        print 'Error: timeout starting Spybot'
        beep()
        sys.exit(-1)
    
    # Click popup when it appears
    dlg = app['Legal stuffTformLegals']
    dlg.OK.Click()

    print 'Spybot succesfully started.'

    # Wait for program to stop running before exiting
    attempts = 1200
    while app['Spybot - Search & Destroy'].Exists() and attempts > 0:
        attempts -= 1
        time.sleep(6)

    if attempts == 0:
        print 'Error: timeout running Spybot'
        beep()
        sys.exit(-1)

    print 'Spybot finished successfully.'




def main():
    if args['uninstall']:
        uninstallSpybot()
    else:
        runSpybot()
    
if __name__ == '__main__':
    main()
    sys.exit(0)

