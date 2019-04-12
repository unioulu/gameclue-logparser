#!/usr/bin/env python3
import argparse
import os
import sanitizer
import counter
import mutationparser as mp
import reporter

DEFAULT_IN = 'logs/'
DEFAULT_OUT = 'output/'


def createParser():
    parser = argparse.ArgumentParser(
        description=""" Generates research relevant numbers
                          out of the gameclue-spacegame logs.""",
        epilog="Work in progress."
    )
    parser.add_argument("logfiles",
                        nargs='*',
                        help="Log files folder path.",
                        default=DEFAULT_IN)
    parser.add_argument("--list",
                        help="List logfiles found on logfiles path.",
                        action='store_true')
    parser.add_argument("--sanitize",
                        help="Sanitizes the original game logs.",
                        action='store_true')
    parser.add_argument("--countkey",
                        nargs='*',
                        help="Counts the number of lines by key.")
    parser.add_argument("--split-mutations",
                        help="Output individual logfiles for each mutation.",
                        action='store_true')
    parser.add_argument("--report",
                        help="Generate a csv report containing meaningful stats.",
                        action="store_true")
    parser.add_argument("-o",
                        help="Output folder path.",
                        default=DEFAULT_OUT)
    return parser


parser = createParser()


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
        parser.error(f'Folder: \"{path}\" does not exist! Incorrect path?')
        return False


def containsFiles(path):
    files = os.listdir(path)
    if not files == []:
        return True
    else:
        parser.error(f"Folder: \"{path}\" is empty! Try another folder path?")
        return False


def main(args):
    parser = createParser()
    args = parser.parse_args(args)

    useDefaultLogFilesPath = True if not isinstance(
        args.logfiles, list) else False
    if not useDefaultLogFilesPath:
        args.logfiles = args.logfiles[0]

    useDefaultOutputPath = True if args.o in DEFAULT_OUT else False

    if folderExist(args.logfiles) and containsFiles(args.logfiles):
        if args.list:
            print(f"Available logfiles:")
            for logfile in listLogFilesByFolderPath(args):
                print(logfile)

        if args.sanitize:
            print(f"Sanitizing...")
            for logfile in listLogFilesByFolderPath(args):
                print(f'{args.logfiles}{logfile}')
                # Sanitize based on first occurence of "GameStarted"
                sanitizer.normalizeTimeStampsByKey(logfile, "GameStarted", args)
                print(f"Sanitized: {logfile}")

        if args.countkey:
            for logfile in listLogFilesByFolderPath(args):
                print(f'Counting keys: {args.countkey} for logfile: {logfile}')
                for key in args.countkey:
                    result = counter.countKeys(f'{args.logfiles}/{logfile}', f'{key}')
                    print(f"{logfile} | {key}: {result[0]}")
                    print(f"{logfile} | {key}: {result[1]}")

        if args.split_mutations:
            for logfile in listLogFilesByFolderPath(args):
                logfilepath = f'{args.logfiles}{logfile}'
                mp.parse(logfilepath, args)

        if args.report:
            for logfile in listLogFilesByFolderPath(args):
                logfilepath = f'{args.logfiles}{logfile}'
                print(logfilepath)
                reporter.generate(logfilepath)

        if args.o:
            if folderExist(args.o):
                print(f"Output produced to: \"{args.o}\"")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
