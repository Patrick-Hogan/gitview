#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created: 2018-07-24
Author: Patrick Hogan
"""

import os
from subprocess import getstatusoutput as run

class Repo():

    def __init__(self, git_dir=None):
        self.refs = dict()
        self.commits = dict()

        if git_dir is None:
            cmd = 'git rev-parse --git-dir'
        else:
            cmd = 'git --git-dir={0} rev-parse --git-dir'.format(git_dir)
        if git_dir is None:
            git_dir = '.'
        (status, git_dir) = run(cmd)
        if status != 0:
            msg = ('Cannot locate git-dir. Run from inside a git repo '
                  'or initialize with git-dir!')
            raise Exception(msg)

        self.git_dir = git_dir
        self.git = 'git --git-dir={0}'.format(git_dir)

        self.add_refs()
        self.add_commits()

    def add_refs(self):
        cmd = '{0} rev-parse --symbolic-full-name --all'.format(self.git)
        (status, refs) = run(cmd)
        if status != 0:
            msg = 'Unable to retreive ref names.'
            raise Exception(msg)
        for ref in refs.split():
            parts = ref.split('/')[1:]
            ref_type = parts[0]
            ref_name = '/'.join(parts[1:])

            if ref_type in ['heads','remotes']:
                cmd = '{0} rev-list {1}'.format(self.git, '{0}')
            elif ref_type == 'tags':
                cmd = '{0} rev-parse {1}'.format(self.git, '{0}')
            else:
                print("Warning: ref type not recognized: {0}".format(ref))
                continue
            (status, commits) = run(cmd.format(ref))
            if status != 0:
                print("Unable to get commit(s) for {0}".format(name))
                continue
            self.refs.setdefault(ref_type,{})[ref_name] = commits.split()

    class Commit():
        def __init__(self, git_dir, sha):
            self.Author = ""
            self.AuthorDate = ""
            self.Commit = ""
            self.CommitDate = ""
            self.Subject = ""
            self.Body = ""

            cmd = ('git --git-dir={0} show '
                   '--pretty=fuller --no-patch {1}').format(git_dir, sha)
            (status, gitlog) = run(cmd)
            if status != 0:
                print("Unable to obtain commit: {0}".format(sha))
                return None
            self.sha = sha
            lines = gitlog.split('\n')
            self.Author = lines[1].split(':')[1].strip()
            self.AuthorDate = lines[2].split(':')[1].strip()
            self.Commit = lines[3].split(':')[1].strip()
            self.CommitDate = lines[4].split(':')[1].strip()
            self.Subject = lines[6]
            if len(lines) > 7:
                self.Body = "\n".join(lines[8:])

        def __str__(self):
            return "\n".join([
                self.sha,
                'Author: {0}'.format(self.Author),
                'AuthorDate: {0}'.format(self.AuthorDate),
                'Commit: {0}'.format(self.Commit),
                'CommitDate: {0}'.format(self.CommitDate),
                'Subject: {0}'.format(self.Subject),
                '', self.Body])

        def __repr(self):
            return self.__str__()

    def add_commits(self):
        cmd = '{0} show --pretty=fuller --no-patch'.format(self.git)
        for ref_type in self.refs.keys():
            for ref_name, shas in self.refs[ref_type].items():
                for sha in shas:
                    if sha in self.commits:
                        continue
                    self.commits[sha] = self.Commit(self.git_dir, sha)

    def __str__(self):
        refs = []
        for ref_type, ref_names in self.refs.items():
            for name in ref_names:
                refs.append('{0}/{1}'.format(ref_type, name))
        lines = ['Git Repository: {0}'.format(self.git_dir)]
        lines.extend(['    {0}'.format(ref) for ref in refs])
        return ('\n'.join(lines))

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    from gitview_gui import GitviewGui
    repo = Repo()
    gui = GitviewGui()
    for reftype, reflist in repo.refs.items():
        gui.draw_branch(reflist)
    gui.run()
