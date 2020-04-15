"""
This file contains a handler for all of the implemented commands.
Casey Johnson, Spring 2020
"""

from enum import Enum

class CommandHandlerError(Exception): pass
class NoSuchCommandError(CommandHandlerError): pass

class CommandHandler:

    class Keywords(Enum):
        """
        Each command keyword is also matched with an internal keyword for command routing.
        Executable functions within this class follow the same naming scheme as these internal keywords.
        """
        ADD_GROUP = "groupadd"
        ADD_USER = "useradd"
        ADD_USER_TO_GROUP = "usergrp"
        CHANGE_GROUP = "chgrp"
        CHANGE_OWNER = "chown"
        CHANGE_PERMISSIONS = "chmod"
        DETAILS = "ls"
        END = "end"
        EXECUTE = "execute"
        LOG_IN = "login"
        LOG_OUT = "logout"
        MAKE_FILE = "mkfile"
        READ = "read"
        WRITE = "write"

    def execute(command):
        """
        This is the only function designed to be called externally. It serves purely as an entrypoint for this class.
        command:    instruction string to be executed.
        """
        return CommandHandler._route_(command)

    def _route_(command):
        route = None
        tokens = command.split(" ")
        command = tokens[0]
        if len(tokens) > 1:
            args = tokens[1:]
        # compare first token of command to keyword list - could binary search if too slow
        for name,item in CommandHandler.Keywords.__dict__.items():
            if isinstance(item, CommandHandler.Keywords) and command == item.value:
                route = ''.join(['_',name.lower(),'_'])
                break
        # if command isn't recognized, throw an error
        if not route:
            raise NoSuchCommandError()
        # route command to its matching function - O(n) is probably best case here
        for name,func in CommandHandler.__dict__.items():
            if callable(func) and name.lower() == route.lower():
                return func(*args)
        # if command hasn't been implemented yet, throw an error
        raise NoSuchCommandError()
