'''
The MIT License (MIT)

Copyright (c) 2013 Nicholas Juszczak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
'''
Script for automating the running of Spybot
and uninstalling

<<<<<<< HEAD
Last Modified: August 5, 2013
=======
Last Modified: July 31, 2013
>>>>>>> 6c5bd96d02642efb4442c6ce09cbd6cb3691c8fa
'''

import pywinauto
import time
import sys
import logging
from pywinauto import application
from winsound import Beep

# Default values
args = {'executable':'',
        'uninstall':False}
# Logging
log = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter('%(message)s'))
log.addHandler(ch)
log.setLevel(logging.INFO)

# Check parameters
if len(sys.argv) > 1:
    for index,arg in enumerate(sys.argv):
        if arg == '-e' or arg == '--executable':
            args['executable'] = sys.argv[index + 1]
        if arg == '-u' or arg == '--uninstall':
            args['uninstall'] = True
        if arg == '-l' or arg == '--logfile':
            hdlr = logging.FileHandler(sys.argv[index + 1])
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            log.addHandler(hdlr)
            log.setLevel(logging.INFO)
        if arg == '-h' or arg == '--help':
            print 'Options are:'
            print '\t-e or --executable <path> | Path to Spybot executable'
            print '\t-u or --uninstall | Uninstall Spybot'
            print '\t-l or --logfile <path> | log file'
            print '\t-h or --help | This screen'
            sys.exit(-1)


print 'Remember, -h or --help for help!\n'
beepFreq = 2500
beepDur = 1000

def beep():
    try:
        Beep(beepFreq, beepDur)
    except:
        print 'Unable to beep... :('


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
        log.error('Error uninstalling Spybot')
        beep()
        sys.exit(-1)

    # Wait for uninstall button prompt
    attempts = 10
    while not app.dlg.UninstallButton.Exists():
        attempts -= 1
        time.sleep(1)

    # timeout
    if attempts == 0:
        log.error('Unable to uninstall Spybot')
        beep()
        sys.exit(-1)

    # click the prompt to uninstall
    try:
        app.dlg.UninstallButton.Click()
    except:
        beep()
        log.error('Error clicking button')

    log.info('Spybot successfully uninstalled')
    

# Run Spybot default
def runSpybot():
    app = application.Application().start_(args['executable'] + ' /autoimmunize /autocheck /autofix /autoclose')

    # Wait for popup
    attempts = 100
    while not app['Legal stuffTformLegals'].Exists() and attempts > 0:
        attempts -= 1
        time.sleep(2)

    if attempts == 0:
        log.error('Error: timeout starting Spybot')
        beep()
        sys.exit(-1)
    
    # Click popup when it appears
    dlg = app['Legal stuffTformLegals']
    dlg.OK.Click()

    log.info('Spybot succesfully started.')

    # Wait for program to stop running before exiting
    attempts = 1200
    while app['Spybot - Search & Destroy'].Exists() and attempts > 0:
        attempts -= 1
        time.sleep(6)

    if attempts == 0:
        log.error('Error: timeout running Spybot')
        beep()
        sys.exit(-1)

    log.info('Spybot finished successfully.')


def main():
    if args['uninstall']:
        uninstallSpybot()
    else:
        runSpybot()
    
if __name__ == '__main__':
    main()
    sys.exit(0)

