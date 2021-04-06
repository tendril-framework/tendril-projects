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
"""
Base Class for Projects
=======================
"""


from tendril.validation.base import ValidatableBase
from tendril.schema import ProjectConfig


class NoProjectException(Exception):
    pass


class ProjectBase(ValidatableBase):
    _config_class = ProjectConfig

    def __init__(self, projectfolder, *args, **kwargs):
        super(ProjectBase, self).__init__(*args, **kwargs)
        self._project_folder = projectfolder
        self._config_obj = None
        _ = self.config

    @property
    def config(self):
        if not self._config_obj:
            try:
                self._config_obj = self._config_class(self._project_folder)
            except self._config_class.FileNotFoundExceptionType:
                raise NoProjectException()
            self._config_obj.validate()
            self._validation_errors.add(self._config_obj.validation_errors)
        return self._config_obj

    @property
    def ident(self):
        return self.config.ident

    @property
    def projectname(self):
        return self.config.projectname

    @property
    def projectfolder(self):
        return self.config.projectfolder

    @property
    def status(self):
        return self.config.status

    @property
    def description(self):
        return self.config._description

    @property
    def maintainer(self):
        return self.config._maintainer

    @property
    def configurations(self):
        return self.config.configurations

    @property
    def modules(self):
        raise NotImplementedError

    def _validate(self):
        _ = self.config
