gitspeculis
======================

a little python script for (constantly) mirroring git repositories

## usage
- think of source repostiroy
- create target repository
- create local directory for temporary files

```
Usage:
    gitspeculis.py (-f <config> | --file <config>) [--verbose]
    gitspeculis.py -h | --help

Options:
    -h --help        Show this screen.
    -f --file        Reads config from YAML File.
```

## config
```
# define your jobname here
myjobname:
    # Source repository (any git address is okay)
    source: https://source/repository.git
    # Target repository (any git address is okay)
    target: target@reposiory.git
    # Place where repository is cached locally
    temp:   /tmp/temporarydir
```


## install
for example in /opt

1. `cd /opt`
2. `git clone https://github.com/derphilipp/gitspeculis.git`
3. `cd gitspeculis`
4. `virtualenv venv`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt` (if this fails, try to install the package from your os repository)
7. `cp gitspeculis.yaml.dist gitspeculis.yaml`
8. `vim gitspeculis.yaml`

## running in crontab
I use a shell wrapper script for handling the virtualenv

1. `/opt/gitspeculis`
2. `cp gitspeculis-cron.sh.dist gitspeculis-cron.sh`
3. `vim gitspeculis-cron.sh`
4. edit your crontab and add `/opt/gitspeculis/gitspeculis-cron.sh`
