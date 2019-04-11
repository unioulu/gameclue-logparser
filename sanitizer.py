#!/usr/bin/env python3
import csv

def getFirstOccurenceLineNumber(logfile, logEntry):
    with open(logfile, 'r') as f:
        for (i, line) in enumerate(f):
            if logEntry in line:
                return i
    return -1

# Normalize all timestamps to start from 0 on first occurence of gamestart.
def normalizeTimeStamps(logfile, args):
    # Sanitize based on first occurence of "GameStarted"
    t0_line = getFirstOccurenceLineNumber(f'{args.logfiles}{logfile}', "GameStarted")
    with open(f'{args.logfiles}{logfile}') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        data = []
        for row in reader:
            data.append(row)

    t0_value = data[t0_line][0]
    sanitized = []

    # Write sanitized logs to given output path (args.o)
    with open(f'{args.o}{logfile}', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        for timestamp, event in data:
            timestamp_sanitized = '%g'%(float(timestamp.replace(',','.')) - float(t0_value.replace(',','.')))
            writer.writerow([timestamp_sanitized, event])
