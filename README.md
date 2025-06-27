# phxrecording
Tools for managing Phoenix instrument recordings 

- phxstatsfile -- repo of tools to manage stats file. -> [the repo](https://github.com/starxcfg/phxstatsfile/)
- phxrecording.py -- the lib to do the heavy-liftings
- phxrecstart.py -- Easy script to get start time timestamp from a given recording from the OS
- phxrecid.py -- Easy script to allow generating the recording ID directly from the OS
- phxrecmetamodstartstop.py -- Easy script to allow modifying start and stop time in recmeta.json directly from the OS
- phxrecshrinkfilelist.py -- Easy script to allow getting shrinked data file list directly from the OS
- phxrecshrinkfinish.py -- Easy script to allow getting shrinked data file list directly from the OS
- phxrecshrink.sh -- Easy script to shrink a recording from Linux
- phxrecshrink.bat -- Easy script to shrink a recording from Windows

### Usage for calling phxrecshrink.bat in Windows
Requirements: 
* Python version 3.10 or later installed and added into PATH.
* New start and stop timestamps should be exactly insteger multiplications of 360s from the oringinal start time. 

Usage example:Get a new recording with specified start and stop: (source, target, start, stop)
   ```shell
   phxrecshrink.bat C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213 C:\Users\xwork\Work\Phx\Data\ 1715188093 1715191693
   ```

### Usage for calling phxrecshrink.sh in Linux
Requirements: 
* Python version 3.10 or later installed.
* New start and stop timestamps should be exactly insteger multiplications of 360s from the oringinal start time.
* 'python' command is avaliable in shell (may need to install python-is-python3 on Ubuntu)

Usage example:Get a new recording with specified start and stop: (source, target, start, stop)
   ```shell
   ./phxrecshrink.sh /home/testuser/10766_2024-05-08-170213 /home/testuser 1715188093 1715191693
   ```

### Usage for calling phxrecstart.py in OS commandline
```shell
python .\phxrecstart.py -i C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213
```

### Usage for calling phxrecid.py in OS commandline
```shell
python .\phxrecid.py -i 10053 -s 1723831936
```

### Usage for calling phxrecmetamodstartstop.py in OS commandline
```shell
python .\phxrecmetamodstartstop.py -i C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213\recmeta.json -o C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170813\recmeta.json -s 1715188093 -e 1715191693
```

### Usage for calling phxrecshrinkfilelist.py in OS commandline
```shell
python .\phxrecshrinkfilelist.py -i C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213\ -s 1715188093 -e 1715191693
```

### Usage for calling phxrecshrinkfinish.py in OS commandline
```shell
python .\phxrecshrinkfinish.py -i C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213\ -o C:\Users\xwork\Work\Phx\Data\ -s 1715188093 -e 1715191693
```
