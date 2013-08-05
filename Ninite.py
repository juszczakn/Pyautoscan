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
Script for automating the running of Ninite

Last Modified: August 5, 2013
'''

import pywinauto
import time
import sys
from pywinauto import application

# cli parameter parsing
args = {'ninite':''}
# Logging
log = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter('%(message)s'))
log.addHandler(ch)
log.setLevel(logging.INFO)

if len(sys.argv) > 1:
    for index,arg in enumerate(sys.argv):
        if arg == '-e' or arg == '--executable':
            args['ninite'] = sys.argv[index + 1]
        if arg == '-l' or arg == '--logfile':
            hdlr = logging.FileHandler(sys.argv[index + 1])
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            log.addHandler(hdlr)
            log.setLevel(logging.INFO)
        if arg == '-h' or arg == '--help':
            print 'Options arg:'
            print '\t-e or --executable | Path to exectuable, including filename'
            print '\t-l or --logfile <path> | log file'
            print '\t-h or --help | This page'
            sys.exit(0)

print 'Remember, -h or --help for help!\n'
beepFreq = 2500
beepDur = 1000

def beep():
    try:
        Beep(beepFreq, beepDur)
    except:
        log.info('Unable to beep... :(')


#Runs the Ninite executable
def runNinite():
    log.info('Starting ', args['ninite'])
    #Start the Ninite Application
    app = application.Application().start_(args['ninite'])

    #Attempt to connect to the Ninite application after it has finished downloading
    dlg = None
    attempts = 0
    while dlg == None and attempts < 30:
        try:
            dlg = app.connect_(title="Ninite")
        except:
            attempts += 1
            time.sleep(2)

    #If the connection timed out, print error. 
    if dlg == None:
        log.info("Error connecting to Ninite: timed out")
        beep()
        sys.exit(-1)
    else:
        log.info('Ninite successfully started and connected')

    #Check to see whether Ninite has finished installing or not.
    #600 attempts = ~20 minutes
    attempts = 600
    while attempts > 0:
        if 'Finished.' not in app.dlg.SysLink3.GetProperties()['Texts'][0]:
            attempts -= 1
            time.sleep(2)
        elif 'Finished.' in app.dlg.SysLink3.GetProperties()['Texts'][0]:
            break

    #Check to see whether or not Ninite timed out
    if attempts == 0:
        log.info('Timed out installing.')
        beep()
        sys.exit(-1)
    else:
        log.info('Installation Succeeded!')
        app.kill_()


#If run as a script call runNinite
if __name__ == '__main__':
    runNinite()

