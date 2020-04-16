"""
This file contains data structures represnting accounts, groups, and files in memory.
Casey Johnson, Spring 2020
"""

class User:
    """
    Class for easily manipulating user data in memory.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.groups = set()

    def __repr__(self):
        return ''.join([self.username, ': ', self.password])

    def add_to_group(self, group):
        self.groups.add(group)
    def remove_from_group(self, group):
        self.groups.remove(group)
    def get_groups(self):
        return self.groups


class Group:
    """
    Class for easily manipulating group data in memory.
    """
    RESERVED_NAMES = {'nil'}

    def __init__(self, name):
        self.name = name
        self.members = set()

    def __repr__(self):
        msg = [self.name+':']
        for member in self.members:
            msg.append(member.username)
        return ' '.join(msg)

    def add_member(self, user):
        self.members.add(user)
    def get_members(self):
        return self.members

NILGROUP = Group(name='nil')


class File:
    """
    Class for easily manipulating file data in memory.
    """
    RESERVED_NAMES = {'accounts.txt', 'audit.txt', 'files.txt', 'groups.txt'}

    def __init__(self, name, owner, owner_perm='rw-', group_perm='---', others_perm='---', group=NILGROUP):
        self.name = name
        with open(self.name, 'w'): pass
        self.owner = owner
        self.group = group
        self.perms = {'owner':owner_perm, 'group':group_perm, 'others':others_perm}

    def __repr__(self):
        msg = [self.name+":", self.owner.username, self.group.name]
        for val in self.perms.values():
            msg.append(val)
        return ' '.join(msg)

    def set_owner(self, owner):
        self.owner = owner
    def get_owner(self):
        return self.owner

    def set_group(self, group):
        self.group = group
    def get_group(self):
        return self.group

    def set_permissions(self, owner='---', group='---', others='---'):
        if owner:
            self.perms['owner'] = owner
        if group:
            self.perms['group'] = group
        if others:
            self.perms['others'] = others
    def get_permissions(self):
        return self.perms

    def write(self, text):
        with open(self.name, 'a') as f:
            f.write(text + '\n')
    def read(self):
        with open(self.name, 'r') as f:
            return f.read().strip()
