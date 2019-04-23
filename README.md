# gameclue-log-parser

Parser that processes [unioulu/gameclue] game logs.

## Purpose

This program is used to process game logs produced by [unioulu/gameclue]. In practice, the program makes sense of the
log files, calculates meaningful research relevant values and uses those values to produce a MutationReport.csv file.

# Prerequisites

To run this programs, python 3.X is required.

# Running

You can run this program from the root of this project by calling ``./parser/parse.py``, like this:
```shell
$ ./parser/parse.py logs/ --output output/
```

*Note*: Please keep in mind that logfiles folder and output path must include the trailing slash (`/`).
*Note*: The logfiles path must containt the logfiles only, _without_the_fps_logs_ since they are not currently supported.

# Arguments

```
$ ./parser/parse.py --help
usage: parse.py [-h] [--list] [-o O] [logfiles [logfiles ...]]

Generates research relevant numbers out of the gameclue-spacegame logs. See
gameclue-spacegame at: https://github.com/unioulu/gameclue

positional arguments:
  logfiles    Log files folder path.

optional arguments:
  -h, --help  show this help message and exit
  --list      List logfiles found on logfiles path.
  -o O        Specify the output folder path.
```

[unioulu/gameclue]: (https://github.com/unioulu/gameclue)
