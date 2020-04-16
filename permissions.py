"""
This file contains a wrapper on all file permissions handling.
Casey Johnson, Spring 2020
"""

class Permissions:
    """
    Wrapper class for easily manipulating permissions strings.
    """
    def is_read_enabled(permString):
        return 'r' in permString
    def is_write_enabled(permString):
        return 'w' in permString
    def is_execute_enabled(permString):
        return 'x' in permString

    def to_json(file_perms):
        j = {
            'r':{key:Permissions.is_read_enabled(file_perms[key]) for key in file_perms.keys()},
            'w':{key:Permissions.is_write_enabled(file_perms[key]) for key in file_perms.keys()},
            'x':{key:Permissions.is_execute_enabled(file_perms[key]) for key in file_perms.keys()},
            }
        return j

    def grant_access(user, file, action):
        perms = Permissions.to_json(file.get_permissions())
        test1 = file.get_owner() == user and perms[action]['owner']
        test2 = file.get_group() in user.get_groups() and perms[action]['group']
        test3 = perms[action]['others']
        if any([test1, test2, test3]):
            return True
        return False
