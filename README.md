# CS465PA2
Casey Johnson,
Spring 2020

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

## Project Completeness

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
students: alice bob
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
businessmajors: chad
pike: chad
```

### testcase5.txt
This test case is designed to ensure the first command creates users `root`. When this command doesn't create `root` immediately, the program is terminated.

## Acknowledgements
