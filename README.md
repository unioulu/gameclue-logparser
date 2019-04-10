# gameclue-log-parser

Parser that processes [unioulu/gameclue] game logs.

## Purpose

This program is supposed to be able to:
  - [x] Sanitize gamelogs by normalizing timestamps starting from 0 on first occurence of "GameStarted"
  - [x] Use custom folder path for logfiles (folder path)
  - [x] Use custom folder path for output (folder path)
  - [ ] Timeframe gamelogs with given time slot parameter
    - In practice means grouping of events, for example in 1 second intervals.
  - [ ] Produce a key-value pair report with per log with...
    - [ ] Order of mutations played (include "All mutation" that concludes all mutations played)
    - [ ] Time of playing per mutation
    - [ ] Number of normal shots fired per mutation
    - [ ] Number of charge shots fired per mutation
    - [ ] ... and many others, that must be defined

# Prerequisites

To run this programs, python 3.X is required.

# Running

You can run this program by calling ``./parse.py``, like this:
```shell
$ ./parse.py --help
```

# Arguments

```
usage: parse.py [-h] [--list] [--sanitize]
                [--countkey [COUNTKEY [COUNTKEY ...]]] [-o O]
                [--slice-output SLICE_OUTPUT]
                [logfiles [logfiles ...]]

Generates research relevant numbers out of the gameclue-spacegame logs.

positional arguments:
  logfiles              Log files folder path.

optional arguments:
  -h, --help            show this help message and exit
  --list                List logfiles found on logfiles path.
  --sanitize            Sanitizes the original game logs.
  --countkey [COUNTKEY [COUNTKEY ...]]
                        Counts the number of lines by key.
  -o O                  Output folder path.
  --slice-output SLICE_OUTPUT
                        Slices the output
```

[unioulu/gameclue]: (https://github.com/unioulu/gameclue)
