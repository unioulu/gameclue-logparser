# gameclue-log-parser

Parser that processes [unioulu/gameclue] game logs.

## Purpose

This program is used to process game logs produced by [unioulu/gameclue]. In practice, the program makes sense of the
log files, calculates meaningful research relevant values and uses those values to produce a MutationReport.csv file.

# Prerequisites

To run this programs, python 3.X is required.

# Running

You can run this program by calling ``./parse.py``, like this:
```shell
$ ./parse.py logs/ --output output/
```

# Arguments

```
$ ./parse.py --help
usage: parse.py [-h] [--list] [-o OUTPUT] [logfiles [logfiles ...]]

Generates research relevant numbers out of the gameclue-spacegame logs. See
gameclue-spacegame at: https://github.com/unioulu/gameclue

positional arguments:
  logfiles              Log files folder path.

optional arguments:
  -h, --help            show this help message and exit
  --list                List logfiles found on logfiles path.
  -o OUTPUT, --output OUTPUT
                        Specify the output folder path.
```

[unioulu/gameclue]: (https://github.com/unioulu/gameclue)
