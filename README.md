Pyautoscan
==========

Automate the installation and execution of virus removal tools
+ Ninite
+ ESET
+ Malwarebytes Anti-Malware
+ Spybot

## Installation
**Requirements**
+ Windows OS (tested with Vista 64 bit)
+ Python 2.7
+ pywinauto (tested with 4.2.0)

## Running
Options are listed at the beginning of each file, and can be listed with -h or --help. They all take a parameter -e, followed by the path the the executable you wish to run.
You might encounter some quirks when running these with UAC enabled, as 
```sh
python <scriptname> <options>
```

An example of running each:

```sh
python Ninite.py -e "C:\Path\To\Executable" # Run Ninite, there are no other options
python ESET.py -e "C:\Path\To\Executable" # Run ESET, there are no other options
python Malwarebytes.py -e "C:\Path\To\Executable" -u -q # Update Malwarebytes and run a quick scan
python Spybot.py -e "C:\Path\To\Executable" -u # Uninstall Spybot
```


## License
These scripts are licensed under the MIT open source license.
