"""
Main launchfile for Programming Assignment 2.
Casey Johnson, Spring 2020
"""

from src.log import *
from src.comhand import *
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
logger.log("Hello.")

# get commands from test file
with open(args.test_file, 'r') as f:
    commandList = f.readlines()

# ensure first command creates root user
try:
    assert commandList[0].split(" ")[0:2] == [CommandHandler.Keywords.ADD_USER.value, 'root']
except AssertionError:
    print("Fatal: first command must create root user.")
    exit()

# process commands
comhand = CommandHandler(args.accounts_file, args.files_file, args.groups_file)
for command in commandList:
    command = command.strip()
    logger.log('>> ' + command)
    resp = comhand.execute(command)
    logger.log(resp)
