#!/usr/bin/env python3
import argparse
import os
from LogFile import LogFile
from GameStartedTimeStampNormalizer import GameStartedTimeStampNormalizer
from MutationTimeStampNormalizer import MutationTimeStampNormalizer
from CSVWriter import CSVWriter

DEFAULT_IN = 'logs/'
DEFAULT_OUT = 'output/'
LogFiles = []
GameStartedTimeStampNormalizer = GameStartedTimeStampNormalizer()
MutationTimeStampNormalizer = MutationTimeStampNormalizer()
CSVWriter = CSVWriter()


def createParser():
    parser = argparse.ArgumentParser(
        description=""" Generates research relevant numbers
                          out of the gameclue-spacegame logs.

                          See gameclue-spacegame at: https://github.com/unioulu/gameclue"""
    )
    parser.add_argument("logfiles",
                        nargs='*',
                        help="Log files folder path.",
                        default=DEFAULT_IN)
    parser.add_argument("--list",
                        help="List logfiles found on logfiles path.",
                        action='store_true')
    parser.add_argument("-o",
                        help="Specify the output folder path.",
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
        parser.error(f"Folder: \"{path}\" does not exist! Incorrect path?")
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

    if folderExist(args.logfiles) and containsFiles(args.logfiles):

        for logfile in listLogFilesByFolderPath(args):
            logfile_path = f'{args.logfiles}{logfile}'
            LogFiles.append(LogFile(logfile_path))

        if args.list:
            print(f"Available logfiles:")
            for logfile in LogFiles:
                print(logfile.path)

        if args.o:
            if folderExist(args.o):
                print(f"Sanitizing...")
                for i, logfile in enumerate(LogFiles):
                    LogFiles[i] = GameStartedTimeStampNormalizer.sanitize(logfile)
                    LogFiles[i] = MutationTimeStampNormalizer.sanitize(logfile)

                print(f"Writing files... ({args.o})")
                for logFile in LogFiles:
                    CSVWriter.write(logFile, args.o)
                    CSVWriter.write_mutation(logFile, args.o)
                CSVWriter.write_mutation_report(LogFiles, args.o)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
