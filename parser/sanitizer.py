#!/usr/bin/env python3
import csv


def sanitize(logfile):
    gameStartedRow = getFirstOccurenceLineNumber(logfile.path, "GameStarted")
    print(gameStartedRow, logfile.path)
    if gameStartedRow != -1:
        timestamp_delta, other = logfile.data[gameStartedRow]
        for timestamp, events in logfile.data:
            timestamp = '%g' % (float(timestamp.replace(
                ',', '.')) - float(timestamp_delta.replace(',', '.')))
    else:
        print(f"Could not find the first occurence of {logEntry} in {logfile}")


def getFirstOccurenceLineNumber(logfile, logEntry):
    with open(logfile, 'r') as f:
        for (i, line) in enumerate(f):
            if logEntry in line:
                return i
    return -1


# Normalize all timestamps to start from 0 on first occurence of "key"
def normalizeTimeStampsByKey(logfile, key, args):
    t0_line = getFirstOccurenceLineNumber(f'{args.logfiles}{logfile}', key)
    with open(f'{args.logfiles}{logfile}') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        data = []
        for row in reader:
            data.append(row)

    t0_value = data[t0_line][0]
    sanitized = []

    # Write sanitized logs to given output path (args.o)
    with open(f'{args.o}{logfile}', 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_ALL)

        for timestamp, event in data:
            timestamp_sanitized = '%g' % (float(timestamp.replace(
                ',', '.')) - float(t0_value.replace(',', '.')))
            writer.writerow([timestamp_sanitized, event])


def normalizeTimeStamps(logfile, args):
    t0_timestamp = getFirstLine(logfile)[0]
    if not t0_timestamp == 0:
        data = []
        with open(logfile) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                print(row)
                timestamp, values = row
                data.append(row)

        with open(logfile, 'w+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for timestamp, event in data:
                sanitized_timestamp = '%g' % (float(timestamp.replace(
                    ',', '.')) - float(t0_timestamp.replace(',', '.')))
                writer.writerow([sanitized_timestamp, event])

        return logfile
    else:
        return -1


def getFirstLine(logfile):
    with open(logfile, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for i, row in enumerate(reader):
            if i == 0:
                return row
    return -1
