"""
This file contains basic data structure wrappers on user, group, and file data.
Casey Johnson, Spring 2020
"""

class Permissions:
    """
    Wrapper class for easily manipulating permissions strings.
    """
    def build_string(read, write, execute):
        perm = ['-']*3
        if read:
            perm[0] = 'r'
        if write:
            perm[1] = 'w'
        if execute:
            perm[2] = 'x'
        return ''.join(perm)

    def to_json(perm):
        perm = {'read':False, 'write':False, 'execute':False}
        if 'r' in perm:
            perm['read'] = True
        if 'w' in perm:
            perm['write'] = True
        if 'x' in perm:
            perm['execute'] = True
        return perm


class User:
    """
    Class for easily manipulating user data in memory.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return ''.join([self.username, ': ', self.password])


class Group:
    """
    Class for easily manipulating group data in memory.
    """
    def __init__(self, name):
        self.name = name
        self.members = set()

    def __repr__(self):
        msg = [self.name+':']
        for member in self.members:
            msg.append(member)
        return ' '.join(msg)

    def add_member(self, username):
        self.members.add(username)


class File:
    """
    Class for easily manipulating file data in memory.
    """
    def __init__(self, name, owner, owner_perm='rw-', group_perm=None, others_perm=None, group='nil'):
        self.name = name
        with open(self.name, 'w'): pass
        self.owner = owner
        self.group = group
        self.perms = {'owner':owner_perm, 'group':group_perm, 'others':others_perm}

    def __repr__(self):
        msg = [self.name+":", self.owner, self.group]
        for val in self.perms.values():
            msg.append(val)
        return ' '.join(msg)

    def set_owner(owner):
        self.owner = owner
    def get_owner():
        return self.owner

    def set_group(group_name):
        self.group = group_name
    def get_group():
        return self.group

    def set_permissions(owner=None, group=None, others=None):
        if owner:
            self.perms['owner'] = owner
        if group:
            self.perms['group'] = group
        if others:
            self.perms['others'] = others
    def get_permissions():
        return self.perms
