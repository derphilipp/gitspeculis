"""
Usage:
    gitspeculis.py (-f <config> | --file <config>) [--verbose]
    gitspeculis.py -h | --help

Options:
    -h --help        Show this screen.
    -f --file        Reads config from YAML File.
"""
import yaml
import os
import git
import logging
from docopt import docopt


class PathDoesNotExist(Exception):
    """
    A path does not exist
    """
    pass


class Job(object):
    """
    Represents a job of a to-be-clone git repository
    """
    def __init__(self, job_name, job_values):
        self.name = job_name
        self.source = job_values['source']
        self.target = job_values['target']
        self.temp = os.path.normpath(job_values['temp'])
        parentdir = os.path.dirname(self.temp)
        if not os.path.exists(parentdir):
            raise PathDoesNotExist("Path {} does not exists".format(parentdir))

    @property
    def repo(self):
        """
        Repository of job
        """
        return git.Repo(self.temp)

    @property
    def repository_exists(self):
        """
        If a (temporary) repository already exists
        """
        if not os.path.exists(self.temp):
            return False
        try:
            git.Repo(self.temp)
        except git.exc.InvalidGitRepositoryError:
            return False
        return True

    def clone(self):
        """
        Initial cloning of origin repository to temporary repository
        """
        logging.info("Cloning %s from %s", self.name, self.source)
        git.Repo.clone_from(self.source, self.temp, mirror=True)

    def fetch(self):
        """
        Fetch changes from source repository to temporary repository
        """
        assert self.repo.remotes.origin.url == self.source
        logging.info("Fetching %s from %s", self.name, self.source)
        self.repo.remotes.origin.fetch()

    def set_push_url(self):
        """
        Set push url for temporary repository to target repository
        """
        logging.info("Setting push url %s to %s", self.name, self.target)
        config_writer = self.repo.remotes.origin.config_writer
        config_writer.set("pushurl", self.target)
        config_writer.release()

    def push(self):
        """
        Push all changes from temporary repository to target repository
        """
        logging.info("Trying to push %s to %s", self.name, self.target)
        self.set_push_url()
        self.repo.remotes.origin.push(mirror=True)


def from_file(args):
    """
    Execute program with commandlineoptions
    """
    with open(args['<config>'], 'r') as filedata:
        config = yaml.load(filedata)
        for job_name, job_config in config.items():
            job = Job(job_name, job_config)
            if not job.repository_exists:
                job.clone()
            else:
                job.fetch()
            job.push()


if __name__ == '__main__':
    PROGRAM_PARAMETERS = docopt(__doc__)
    if PROGRAM_PARAMETERS['--file']:
        from_file(PROGRAM_PARAMETERS)
