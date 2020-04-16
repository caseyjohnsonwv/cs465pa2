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
        return "Command {} not found.".format(command)

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
            if groupname in Group.RESERVED_NAMES:
                resp = "Failed: group name {} not permitted.".format(groupname)
            elif self._get_group_by_name_(groupname):
                resp = "Failed: group {} already exists.".format(groupname)
            else:
                group = Group(name=groupname)
                self.groups.add(group)
                resp = "Group {} created.".format(group.name)
        return resp

    def _add_user_(self, username, password):
        resp = "Denied: only root can create new users."
        if (len(self.users) == 0 and username == 'root') or self._has_root_access_():
            if self._get_user_by_name_(username):
                resp = "Failed: user {} already exists.".format(username)
            else:
                user = User(username=username, password=password)
                with open(self.accounts_file, 'a') as f:
                    f.write(str(user)+'\n')
                self.users.add(user)
                resp = "User {} created.".format(username)
        return resp

    def _add_user_to_group_(self, username, groupname):
        resp = "Denied: only root can change user groups."
        user = self._get_user_by_name_(username)
        group = self._get_group_by_name_(groupname)
        if not user:
            resp = "Failed: user {} does not exist.".format(username)
        elif not group:
            resp = "Failed: group {} does not exist.".format(groupname)
        elif self._has_root_access_():
            group.add_member(user)
            user.add_to_group(group)
            resp = "User {} added to {}.".format(user.username, group.name)
        return resp

    def _change_group_(self, filename, groupname):
        resp = "Denied: files can only be moved to groups to which the user belongs."
        file = self._get_file_by_name_(filename)
        if not file:
            resp = "Failed: file {} does not exist.".format(filename)
        elif self._has_root_access_() or (self.logged_in and file.owner == self.logged_in):
            for group in self.logged_in.get_groups():
                if groupname == group.name:
                    file.set_group(group)
                    resp = "User {} added {} to group {}.".format(self.logged_in.username, file.name, group.name)
                    break
        else:
            resp = "Denied: only file owners and root can change file groups."
        return resp

    def _change_owner_(self, filename, username):
        resp = "Denied: only root can change file owners."
        file = self._get_file_by_name_(filename)
        user = self._get_user_by_name_(username)
        if not file:
            resp = "Failed: file {} does not exist.".format(filename)
        elif not user:
            resp = "Failed: user {} does not exist.".format(username)
        elif self._has_root_access_():
            file.set_owner(user)
            resp = "User {} made {} the owner of {}.".format(self.logged_in, user.username, file.name)
        return resp

    def _change_permissions_(self, filename, owner_perm, group_perm, others_perm):
        resp = "Denied: only file owners and root can change file permissions."
        file = self._get_file_by_name_(filename)
        if not file:
            resp = "Failed: file {} does not exist.".format(filename)
        elif self._has_root_access_() or (self.logged_in and file.owner == self.logged_in):
            file.set_permissions(owner=owner_perm, group=group_perm, others=others_perm)
            resp = "User {} changed permissions for {} to '{}{}{}'.".format(self.logged_in, file.name, owner_perm, group_perm, others_perm)
        return resp

    def _details_(self, filename):
        file = self._get_file_by_name_(filename)
        resp = str(file) if file else "Failed: file {} does not exist.".format(filename)
        return resp

    def _end_(self):
        with open(self.files_file,'w') as f:
            for file in self.files:
                f.write(str(file)+'\n')
        with open(self.groups_file,'w') as f:
            for group in self.groups:
                f.write(str(group)+'\n')
        return "File and group data saved."

    def _execute_(self, filename):
        file = self._get_file_by_name_(filename)
        if not self.logged_in:
            resp = "Denied: no user is logged in."
        elif Permissions.grant_access(user=self.logged_in, file=file, action='x'):
            resp = "Executed {} successfully.".format(file.name)
        else:
            resp = "Denied: {} cannot execute {}.".format(self.logged_in, file.name)
        return resp

    def _log_in_(self, username, password):
        resp = "Denied: simultaneous logins not permitted."
        if not self.logged_in:
            user = self._get_user_by_name_(username)
            if not user:
                resp = "Failed: user {} not found.".format(username)
            elif user.password != password:
                resp = "Failed: invalid username or password."
            else:
                self.logged_in = user
                resp = "User {} logged in.".format(user.username)
        return resp

    def _log_out_(self):
        resp = "Failed: no user is logged in."
        if self.logged_in:
            resp = "User {} logged out.".format(self.logged_in.username)
            self.logged_in = None
        return resp

    def _make_file_(self, filename):
        resp = "Denied: no user is logged in."
        if self.logged_in:
            if self._get_file_by_name_(filename):
                resp = "Failed: file {} already exists.".format(filename)
            elif filename in File.RESERVED_NAMES:
                resp = "Failed: file name {} not permitted.".format(filename)
            else:
                file = File(name=filename, owner=self.logged_in)
                self.files.add(file)
                resp = "File {} with owner {} and default permissions created.".format(filename, self.logged_in.username)
        return resp

    def _read_(self, filename):
        file = self._get_file_by_name_(filename)
        if not self.logged_in:
            resp = "Denied: no user is logged in."
        elif not file:
            resp = "Failed: file {} does not exist.".format(filename)
        else:
            user = self.logged_in
            if Permissions.grant_access(user=user, file=file, action='r'):
                msg = file.read()
                resp = "{}:\n{}.".format(file.name, msg)
            else:
                resp = "Denied: user {} does not have read permission for {}.".format(self.logged_in, filename)
        return resp

    def _write_(self, filename, *text):
        msg = ' '.join(text)
        file = self._get_file_by_name_(filename)
        if not self.logged_in:
            resp = "Denied: no user is logged in."
        elif not file:
            resp = "Failed: file {} does not exist.".format(filename)
        else:
            user = self.logged_in
            if Permissions.grant_access(user=user, file=file, action='w'):
                file.write(msg)
                resp = "Text written to {}.".format(filename)
            else:
                resp = "Denied: user {} does not have write permission for {}.".format(self.logged_in, filename)
        return resp
