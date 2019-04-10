#!/usr/bin/env python3
import argparse
import os
import sanitizer
import counter

LOGS_FOLDER_PATH = './logs'

# Lists available logs found in ./logs
def listLogFiles(path):
    # path = "./logs"
    available_logs = []
    files = os.listdir(path)
    for name in files:
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            available_logs.append(name)
    return available_logs

def parseArguments(args):
    parser = argparse.ArgumentParser(
        description="Generates research relevant numbers out of the gameclue-spacegame logs.",
        epilog="Work in progress."
    )
    parser.add_argument("logfiles",     nargs='*',  help="Log files folder path.",                default="./logs")
    parser.add_argument("--list",                   help="List logfiles found on logfiles path.", action='store_true')
    parser.add_argument("--sanitize",               help="Sanitizes the original game logs.",     action='store_true')
    parser.add_argument("--countkey",   nargs='*',  help="Counts the number of lines by key.")

    args = parser.parse_args(args)
    return args

def isOutputFilePresent():
    if os.path.isfile(os.listdir('./output/processed.csv')):
        return True
    else:
        return False

def main(args):
    args = parseArguments(args)
    useDefaultLogFilesPath = True if not isinstance(args.logfiles, list) else False

    if useDefaultLogFilesPath:
        print("Using default path: ./logs")
        if args.list:
            print(f"Available logfiles: {listLogFiles(args.logfiles)}")

        if args.sanitize:
            print(f"Sanitizing...")
            for logfile in listLogFiles(args.logfiles):
                sanitizer.normalizeTimeStamps(f'logs/{logfile}')
                print(f"Sanitized: {logfile}")

        if args.countkey:
            print(args.countkey)
            for logfile in listLogFiles(args.logfiles):
                for key in args.countkey:
                    print(counter.countLogEntryValues(f'logs/{logfile}', f'{key}'))

    else:
        if args.countkey:
            print(f'Counting keys: {args.countkey}')
            for logfile in listLogFiles(args.logfiles):
                for key in args.countkey:
                    print(counter.countKeys(f'logs/{logfile}', f'{key}'))

if __name__== "__main__":
    import sys
    main(sys.argv[1:])
