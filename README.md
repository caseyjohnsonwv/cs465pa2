# CS465PA2
Casey Johnson, Spring 2020


## System Information
This software is designed to run on Python 3.5 or newer. Development has spanned both Windows 10 and Ubuntu 16.04 systems.


## Installation and Usage
To install from GitHub, simply clone the repository onto your machine and `cd` to the project's top-level directory. To install from a compressed distribution, unzip the project source on your machine and do the same.

To run with test case file `testcase1.txt` in subdirectory `/tests`, use:
```
python3 access.py tests/testcase1.txt
```
Required files `accounts.txt`, `audit.txt`, `files.txt`, and `groups.txt` will be placed in the root directory. All files created by the program's `mkfile` command will also appear in the root directory.


## Design Architecture

### Completeness
Each source file contains headers with descriptions of completeness. In summary, the program successfully executes all five test cases included in subdirectory `/tests` and the expected results are reflected in `audit.txt` each time.

### Overview
In accordance with best practices, I attempted to follow an object-oriented architecture. The idea came when I wanted to standardize logging by building a separate class in its own file `log.py`, then call the logger after each command. The logger is also used to echo audit messages to the terminal via the option `echo=True` in its constructor. This led me to build a command handler `comhand.py`, a permissions handler `permissions.py`, and a data structures handler `structures.py`. While the program is run from `access.py`, most of the work is done by these other source files.

The command handler is called via `execute()`, an external wrapper, which passes the command down to a routing function. Every internal function follows the naming scheme `_<keyword>_()`, such as `_change_permissions_()` and `_make_file_()`. The router matches the first token of the command to the proper keyword using the `Keywords` enum, then uses C-level mechanics via `.__dict__` to execute the command. Iterating over the class's internal functions proved much easier than manually routing each command, and each function passes an output string back up the chain to `access.py`.

The structures `File`, `Group`, and `User` are just basic data wrappers, similar to something we might have built in CS 110. The greatest challenge, though, came with permissions strings. I decided to use dictionaries for storing the strings within `File` objects and a custom `Permissions` class for interpretation. This class has a method `grant_access()`, which takes a User object, File object, and action character `[r|w|x]` as arguments. This one function handles all standard Unix permissions testing based on ownership, group membership, and file permissions. It returns `True` if the user should be granted access, or `False` if not. This is all powered by other helper functions in `permissions.py`, which made access control for files much easier to implement.

As they are created, users are immediately serialized in `accounts.txt` via the overridden function `.__repr__()`. The command handler also tracks created accounts, files, groups, the logged-in user, and output file pointers in memory. If `_end_()` is called, file and group data is serialized, then execution is immediately halted.

### accounts.txt
The `accounts.txt` file follows a simple structure: `<username>: <password>`. For example, a user named `root` with password `admin` would be stored as `root: admin` with each successive entry on its own line. This simple naming scheme allows for standardized interpretation alongside the other mandatory colon-delimited files `groups.txt` and `files.txt`.


## Test Case Descriptions

### testcase1.txt
This test case is described in-depth in the original project assignment.
```
accounts.txt
---
root: ya84*_o
alice: Wvu_4_Life
bob: SHHHsecret
tom: geek_247
```
```
files.txt
---
file1.txt: tom nil rw- --- ---
file2.txt: alice students rw- rw- r--
```
```
groups.txt
---
students: bob alice
```
```
file1.txt
---
Text from Alice in file1
Text from Tom in file1
```
```
file2.txt
---
Text from Alice in file2
Text from Bob in file2
```

### testcase2.txt
This test case is described in-depth in the original project assignment.
```
accounts.txt
---
root: @r00t(705)
steveo: d@man^304
rita: #101'holla!
```
```
files.txt
---
script: steveo testers -wx rw- --x
```
```
groups.txt
---
testers: rita steveo
```
```
script
---
echo Hello World!
echo Hello World!
```

### testcase3.txt
This test case is designed primarily to test group-level permissions. User `root` is created, then forced to log-in before proceeding. `root` makes a file `file1.txt` and elevates its permissions to `rw- rw- r--`. Group `editors` and user `charlie` are also created. `root` then logs out.

Next, `charlie` logs in and attempts read and write operations on `file1.txt`. The write operation is denied because the file's permissions do not allow write operations for non-owners and non-group users. `root` adds `charlie` to the group `editors`, but writing is still denied because `file1.txt` does not belong to the same group. When `root` adds the file to `editors`, finally `charlie` is allowed to write in it.

`root` also creates user `ruth`, who attempts read and write operations on `file1.txt`. While `ruth` can read what `charlie` wrote, she is denied access to write in the file herself because she is a non-owner and non-group user.

```
accounts.txt
---
root: admin
charlie: secretcharliepassword
ruth: secretruthpassword
```
```
files.txt
---
file1.txt: root editors rw- rw- r--
```
```
groups.txt
---
editors: charlie
```
```
file1.txt
---
random text from charlie
```

### testcase4.txt
This test case is designed primarily to test permissions modifications. User `root` is created and logs in. Users `jimbo` and `chad` are then created, along with groups `pike` and `businessmajors`. To test users belonging to multiple groups, `chad` is added to both.

User `root` then attempts a series of rejected commands, including creation of files with all four reserved names, permissions elevation of a reserved file, and duplicated creation of a file. All of these operations are denied.

Next, `root` creates two files. User `root` writes in `file1.txt`, changes its group to `pike`, and elevates its permissions to `rwx r-x r--`. User `root` also writes in `file2.txt`, changes its group to `businessmajors`, and lowers its permissions to `--- --- ---`. At this point, even `root` is denied read access to the file. User `root` elevates `file2.txt` to `r-x r-x r--` and changes its owner to `jimbo`.

User `chad` attempts execute operations on both files, both of which are allowed because he belongs to both `pike` with `file1.txt` and `businessmajors` with `file2.txt`. User `jimbo` attempts the same operations. Exeuction is allowed on `file1.txt` because `jimbo` is the owner, but denied on `file2.txt` because he does not belong to the correct group.

```
accounts.txt
---
root: admin
jimbo: coalbaron69
chad: fratboy420
```
```
files.txt
---
file1.txt: root pike rwx r-x r--
file2.txt: jimbo businessmajors r-x r-x r--
```
```
groups.txt
---
pike: chad
businessmajors: chad
```
```
file1.txt
---
root writing in file1.txt
```
```
file2.txt
---
root writing in file2.txt
```

### testcase5.txt
This test case is designed to ensure the first command creates users `root`. When this command doesn't create `root` immediately, the program is terminated.


## Acknowledgements
