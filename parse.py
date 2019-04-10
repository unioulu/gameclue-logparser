#!/usr/bin/env python3
import argparse
import os
import sanitizer
import counter

parser = argparse.ArgumentParser(
    description="Generates research relevant numbers out of the gameclue-spacegame logs.",
    epilog="Work in progress."
)

def listLogFilesByFolderPath(args):
    path = args.logfiles
    available_logs = []
    files = os.listdir(path)
    for name in files:
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            available_logs.append(name)
    return available_logs

def folderExist(path):
    try:
        os.listdir(path)
        return True
    except FileNotFoundError:
        parser.error(f"Folder: \"{path}\" does't exist! Path typed incorrectly?")
        return False

def containsFiles(path):
    files = os.listdir(path)
    if not files == []:
        return True
    else:
        parser.error(f" Folder: \"{path}\" is empty! Try another folder path?")
        return False

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

def main(args):
    args = parseArguments(args)

    useDefaultLogFilesPath = True if not isinstance(args.logfiles, list) else False
    if not useDefaultLogFilesPath:
        args.logfiles = args.logfiles[0]

    if folderExist(args.logfiles) and containsFiles(args.logfiles):
        if args.list:
            print(f"Available logfiles:")
            for logfile in listLogFilesByFolderPath(args):
                print(logfile)

        if args.sanitize:
            print(f"Sanitizing...")
            for logfile in listLogFilesByFolderPath(args):
                sanitizer.normalizeTimeStamps(f'logs/{logfile}')
                print(f"Sanitized: {logfile}")

        if args.countkey:
            for logfile in listLogFilesByFolderPath(args):
                print(f'Counting keys: {args.countkey} for logfile: {logfile}')
                for key in args.countkey:
                    result = counter.countKeys(f'logs/{logfile}', f'{key}')
                    print(f"{logfile} | {key}: {result[0]}")
                    print(f"{logfile} | {key}: {result[1]}")

if __name__== "__main__":
    import sys
    main(sys.argv[1:])
