"""
Main launchfile for Programming Assignment 2.
Casey Johnson, Spring 2020
"""

from log import LoggingHandler
from comhand import CommandHandler
from argparse import ArgumentParser

# parse command line arguments
parser = ArgumentParser(description="CS 465 Programming Assignment 2 - Access Control")
parser.add_argument("test_file", help="File containing newline-delimited access control commands.")
parser.add_argument("--log-file", default="audit.txt", help="File for logging output.")
args = parser.parse_args()

# open logging
logger = LoggingHandler(log_file=parser.log_file, echo=True)
logger.log("Hello")

# get commands from test file
with open(parser.test_file, 'r') as f:
    commandList = f.readlines()

# process commands
for command in commandList:
    CommandHandler.execute(command)
