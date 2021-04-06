#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import csv
from tendril.config import AUDIT_PATH
from tendril.utils.fsutils import VersionedOutputFile

from tendril.validation.base import ValidatableBase
from tendril.entities.projects.base import ProjectBase
from tendril.entities.projects.base import NoProjectException


class ProjectNotFoundError(Exception):
    pass


class ProjectLibraryBase(ValidatableBase):
    _project_classes = [ProjectBase]

    def __init__(self, vctx=None):
        self._projects = []
        self._index = {}
        super(ProjectLibraryBase, self).__init__(vctx)
        self.regenerate()

    @property
    def idents(self):
        return self._index.keys()

    @property
    def projects(self):
        return self._projects

    def is_recognized(self, ident):
        return ident in self._index.keys()

    def regenerate(self):
        self._find_projects()
        self._generate_index()

    @property
    def index(self):
        if not self._index:
            self._generate_index()
        return self._index

    def _try_project(self, path):
        for pclass in self._project_classes:
            try:
                return pclass(path)
            except NoProjectException:
                continue

    def _find_projects(self):
        raise NotImplementedError

    def _generate_index(self):
        self._index = {}
        for project in self._projects:
            if project.ident in self._index.keys():
                self._index[project.ident].append(project)
            else:
                self._index[project.ident] = [project]

    def get(self, ident):
        if ident not in self._index.keys():
            raise ProjectNotFoundError()
        return self._index[ident]

    def export_audit(self, name):
        auditfname = os.path.join(
            AUDIT_PATH, 'projectlib-{0}.audit.csv'.format(name)
        )
        outf = VersionedOutputFile(auditfname)
        outw = csv.writer(outf)
        outw.writerow(['ident', 'name', 'folder', 'status',
                       'description', 'maintainer'])
        for project in self.projects:
            outw.writerow(
                [project.ident, project.projectname, project.projectfolder, project.status,
                 project.description, project.maintainer]
            )

        outf.close()


class FileSystemProjectLibraryBase(ProjectLibraryBase):
    _exclusions = ['.git', '.svn']

    def __init__(self, library_root, vctx=None):
        self._root = library_root
        super(FileSystemProjectLibraryBase, self).__init__(vctx)

    def _find_projects(self):
        self._find_projects_in_folder(self._root)

    def _find_projects_in_folder(self, basefolder):
        for root, dirs, files in os.walk(basefolder):
            dirs[:] = [d for d in dirs
                       if list(filter(d.endswith, self._exclusions)) == []]
            for d in dirs:
                project = self._try_project(os.path.join(root, d))
                if project:
                    self.projects.append(project)


def load(manager):
    manager.install_exc_class('ProjectNotFoundError', ProjectNotFoundError)
