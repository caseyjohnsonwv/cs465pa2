"""
This file contains a handler for all of the implemented commands.
Casey Johnson, Spring 2020
"""

from permissions import *
from enum import Enum

class CommandHandler:

    def __init__(self, accounts_file, files_file, groups_file):
        self.accounts_file = accounts_file
        self.files_file = files_file
        self.groups_file = groups_file
        self.users = set()
        self.groups = set()
        self.files = set()
        self.logged_in = None

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
        return "Command '{}' not found.".format(command)

    def _has_root_access_(self):
        return self.logged_in and self.logged_in.username == 'root'

    def _get_user_by_name_(self, username):
        for user in self.users:
            if user.username == username:
                return user
    def _get_group_by_name_(self, groupname):
        for group in self.groups:
            if group.name == groupname:
                return group
    def _get_file_by_name_(self, filename):
        for file in self.files:
            if file.name == filename:
                return file

    def _add_group_(self, groupname):
        resp = "Denied: only root can create new groups."
        if self._has_root_access_():
            if groupname == 'nil':
                resp = "Failed: group name 'nil' not permitted."
            elif self._get_group_by_name_(groupname):
                resp = "Failed: group '{}' already exists.".format(groupname)
            else:
                group = Group(name=groupname)
                self.groups.add(group)
                resp = "Group '{}' created.".format(group.name)
        return resp

    def _add_user_(self, username, password):
        resp = "Denied: only root can create new users."
        if (len(self.users) == 0 and username == 'root') or self._has_root_access_():
            if self._get_user_by_name_(username):
                resp = "Failed: user '{}' already exists.".format(username)
            else:
                user = User(username=username, password=password)
                with open(self.accounts_file, 'a') as f:
                    f.write(str(user)+'\n')
                self.users.add(user)
                resp = "User '{}' created.".format(username)
        return resp

    def _add_user_to_group_(self, username, groupname):
        resp = "Denied: only root can change user groups."
        user = self._get_user_by_name_(username)
        group = self._get_group_by_name_(groupname)
        if not user:
            resp = "Failed: user '{}' does not exist.".format(username)
        elif not group:
            resp = "Failed: group '{}' does not exist.".format(groupname)
        elif self._has_root_access_():
            group.add_member(user)
            resp = "User '{}' added to '{}'.".format(user.username, group.name)
        return resp

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
        resp = "Failed: invalid username or password."
        if self.logged_in:
            resp = "Denied: simultaneous logins not permitted."
        else:
            user = self._get_user_by_name_(username)
            if user:
                self.logged_in = user
                resp = "User {} logged in.".format(user.username)
        return resp

    def _log_out_(self):
        resp = "Failed: no user is logged in."
        if self.logged_in:
            resp = "User '{}' logged out.".format(self.logged_in.username)
            self.logged_in = None
        return resp

    def _make_file_(self, filename):
        pass

    def _read_(self, filename):
        pass

    def _write_(self, filename, *text):
        pass
