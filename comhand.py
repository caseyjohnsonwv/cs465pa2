"""
This file contains a handler for all of the implemented commands.
Casey Johnson, Spring 2020
"""

from enum import Enum

class CommandHandlerError(Exception): pass
class NoSuchCommandError(CommandHandlerError): pass

class CommandHandler:

    def __init__(self, accounts_file, files_file, groups_file):
        self.accounts_file = accounts_file
        self.files_file = files_file
        self.groups_file = groups_file

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

    def execute(self, command):
        """
        This is the only function designed to be called externally. It serves purely as an entrypoint for this class.
        command:    instruction string to be executed.
        return:     string response message to be logged.
        """
        return self._route_(command)

    def _route_(self, command):
        route = None
        tokens = command.split(" ")
        command = tokens[0]
        args = tokens[1:] if len(tokens) > 1 else []
        # compare first token of command to keyword list - could binary search if too slow
        for name,item in self.Keywords.__dict__.items():
            if isinstance(item, self.Keywords) and command == item.value:
                route = ''.join(['_',name.lower(),'_'])
                break
        # if command isn't recognized, throw an error
        if not route:
            raise NoSuchCommandError()
        # route command to its matching function - O(n) is probably best case here
        for name,func in CommandHandler.__dict__.items():
            if callable(func) and name.lower() == route.lower():
                return func(self, *args)
        # if command hasn't been implemented yet, throw an error
        raise NoSuchCommandError()

    def _add_group_(self, groupname):
        pass

    def _add_user_(self, username, password):
        pass

    def _add_user_to_group_(self, username, groupname):
        pass

    def _change_group_(self, filename, groupname):
        pass

    def _change_owner_(self, filename, username):
        pass

    def _change_permissions_(self, filename, owner_perm, group_perm, others_perm):
        pass

    def _details_(self, filename):
        pass

    def _end_(self):
        pass

    def _execute_(self, filename):
        pass

    def _log_in_(self, username, password):
        pass

    def _log_out_(self):
        pass

    def _make_file_(self, filename):
        pass

    def _read_(self, filename):
        pass

    def _write_(self, filename, *text):
        pass
