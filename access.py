"""
Main launchfile for Programming Assignment 2.
Casey Johnson, Spring 2020
"""

from log import *
from comhand import *
from argparse import ArgumentParser

# parse command line arguments
parser = ArgumentParser(description="CS 465 Programming Assignment 2 - Access Control")
parser.add_argument("test_file", help="File containing newline-delimited access control commands.")
parser.add_argument("--log-file", default="audit.txt", help="File for logging output.")
parser.add_argument("--accounts-file", default="accounts.txt", help="File for account access data.")
parser.add_argument("--groups-file", default="groups.txt", help="File for group access data.")
parser.add_argument("--files-file", default="files.txt", help="File for file access data.")
args = parser.parse_args()

# create required files (hidden by .gitignore)
with open(args.accounts_file, 'w'): pass
with open(args.groups_file, 'w'): pass
with open(args.files_file, 'w'): pass

# open logging
logger = LoggingHandler(log_file=args.log_file, echo=True)
logger.log("Hello")

# get commands from test file
with open(args.test_file, 'r') as f:
    commandList = f.readlines()

# process commands
for command in commandList:
    command = command.strip()
    try:
        CommandHandler.execute(command)
    except NoSuchCommandError:
        print("Can't execute '{}' - not yet implemented!".format(command))
