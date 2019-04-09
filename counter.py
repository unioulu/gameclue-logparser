#!/usr/bin/env python3
import csv

def countKeys(logfile, key):
    count = 0
    rows = []
    with open(logfile, 'r') as f:
        for (i, line) in enumerate(f):
            if key in line:
                count = count + 1
                rows.append(line)
        return count, rows
