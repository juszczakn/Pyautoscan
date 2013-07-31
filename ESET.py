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
Script for automating the run of ESET

Last Modified: July 29, 2013
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
args = {'executable':''}

if len(sys.argv) > 1:
    for index,arg in enumerate(sys.argv):
        if arg == '-e' or arg == '--executable':
            args['executable'] = sys.argv[index + 1]
        if arg == '-h' or arg == '--help':
            print 'Options are:'
            print '\t-e or --executable <path> | Path to ESET executable'
            print '\t-h or --help | This screen'
            sys.exit(0)

def runEset():
    app = application.Application().start_(args['executable'])

    attempts = 10
    while not app['Terms of use'].Exists() and attempts > 0:
        attempts -= 1
        time.sleep(1)
        
    if attempts == 0:
        print 'Error starting ESET'
        beep()
        sys.exit(-1)
        
    app['Terms of use'].CheckBox.Click()
    app['Terms of use'].Button.Click()

    print 'Terms of use window closed'
    
    dlg = None
    attempts = 60
    while dlg == None and attempts > 0:
        try:
            dlg = app.connect_(title='ESET Online Scanner')
        except:
            attempts -= 1
            time.sleep(2)

    if attempts == 0:
        print 'Error: timeout starting ESET'
        beep()
        sys.exit(-1)

    app['ESET Online Scanner'].Start.Click()
    print 'Started scan'

    attempts = 4000
    while 'Finish' not in app['ESET Online Scanner'].Button.GetProperties()['Texts'][0] and attempts > 0:
        attempts -= 1
        time.sleep(6)

    if attempts == 0:
        print 'Error: timeout running ESET'
        beep()
        sys.exit(-1)

    app['ESET Online Scanner'].CheckBox.Click()
    print 'Uninstall Clicked'
    time.sleep(5)
    
    app['ESET Online Scanner'].FinishButton.Click()
    print 'Finish Clicked'
    time.sleep(5)
    
    app.kill_()

    print "ESET Successfully ran and closed"


if __name__ == '__main__':
    runEset()
    sys.exit(0)

