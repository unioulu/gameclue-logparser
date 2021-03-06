# gameclue-log-parser

Parser that processes [unioulu/gamecluespacegame] game logs to produce research relevant data.

## Purpose

This program is used to process game logs produced by [unioulu/gamecluespacegame]. In practice, the program makes sense of the
log files, calculates meaningful research relevant values and uses those values to produce a MutationReport.csv file.

# Prerequisites

To run this programs, python 3.X is required.

# Running

You can run this program from the root of this project by calling ``./parser/parse.py``, like this:
```shell
$ ./parser/parse.py logs/ --output output/
```

## Caveats

- *Note*: Given logfiles path must be an existing folder and the output path *must* include a trailing slash (`/`).
- *Note*: Given logfiles path must contain logfiles produced by the [unioulu/gamecluespacegame] *only* _without_the_fps_logs_. Parsing fps logs are currently not supported.

# Arguments

```
$ ./parser/parse.py --help
usage: parse.py [-h] [--list] [-o O] [logfiles [logfiles ...]]

Generates research relevant numbers out of the gameclue-spacegame logs. See
gameclue-spacegame at: https://github.com/unioulu/gameclue-spacegame

positional arguments:
  logfiles    Log files folder path.

optional arguments:
  -h, --help  show this help message and exit
  --list      List logfiles found on logfiles path.
  -o O        Specify the output folder path.
```

[unioulu/gamecluespacegame]: (https://github.com/unioulu/gameclue-spacegame)
