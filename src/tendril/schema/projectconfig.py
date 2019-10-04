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
Project Configuration Schema
----------------------------
"""

from __future__ import print_function

import os
from decimal import Decimal
from tendril.schema.base import SchemaControlledYamlFile

from tendril.entities.projects.primitives import GroupDefinitionList
from tendril.entities.projects.primitives import MotifDefinitionList
from tendril.entities.projects.primitives import SJDefinitionList
from tendril.entities.projects.primitives import GeneratorDefinitionList
from tendril.entities.projects.primitives import TestProtocolDefinition

from tendril.entities.projects.configurations import ConfigurationDefinitionList
from tendril.entities.projects.configsections import ConfigSectionDefinitionList
from tendril.entities.projects.configmatrices import ConfigMatrixDefinitionList

from tendril.entities.projects.legacy import ProjectConfigLegacyMixin

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class NoProjectError(Exception):
    pass


class ProjectConfig(SchemaControlledYamlFile, ProjectConfigLegacyMixin):
    supports_schema_name = 'ProjectConfig'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')
    FileNotFoundExceptionType = NoProjectError
    configs_location = ['configs.yaml']

    def __init__(self, projectfolder, *args, **kwargs):
        self.projectfolder = projectfolder
        self._configurations = None
        super(ProjectConfig, self).__init__(self._cfpath, *args, **kwargs)

    @property
    def projectfolder(self):
        return self._projectfolder

    @projectfolder.setter
    def projectfolder(self, value):
        if not os.path.splitext(value)[1]:
            self._projectfolder = value
        else:
            for _ in self.configs_location:
                value = os.path.split(value)[0]
            self._projectfolder = value

    # @property
    # def docfolder(self):
    #     raise NotImplementedError
    #
    # @property
    # def pricingfolder(self):
    #     raise NotImplementedError

    @property
    def _cfpath(self):
        return os.path.join(self._projectfolder, *self.configs_location)

    def elements(self):
        e = super(ProjectConfig, self).elements()
        e.update({
            'grouplist': self._p('grouplist', required=False,
                                 parser=GroupDefinitionList,
                                 parser_args={'basedir': self.projectfolder},
                                 default=[{'name': 'default',
                                           'desc': 'Unclassified'}]),
            'motiflist': self._p('motiflist', required=False, default={},
                                 parser=MotifDefinitionList),
            'sjlist':    self._p('sjlist',    required=False, default={},
                                 parser=SJDefinitionList),
            'genlist':   self._p('genlist',   required=False, default={},
                                 parser=GeneratorDefinitionList),
            'tests':     self._p('tests',     required=False, default=[],
                                 parser=TestProtocolDefinition),
            'snoseries': self._p('snoseries', required=True),
            '_base_configurations': self._p('configurations', required=True,
                                            parser=ConfigurationDefinitionList),  # noqa
            'configsections': self._p('configsections', required=False,
                                      default=[],
                                      parser=ConfigSectionDefinitionList),
            'configmatrices': self._p('configmatrix', required=False,
                                      default=[],
                                      parser=ConfigMatrixDefinitionList),
            '_maintainer':  self._p('maintainer', required=False, default=''),
            '_description': self._p('desc', required=False, default=''),
            'status':       self._p('status', required=False, default=''),
        })
        return e

    def schema_policies(self):
        policies = super(ProjectConfig, self).schema_policies()
        policies.update({})
        return policies

    @property
    def configurations(self):
        if not self._configurations:
            self._configurations = ConfigurationDefinitionList([])
            for configuration in self._base_configurations:
                configuration.preprocess()
                configuration.apply_defaults(self)
                self._configurations.extend(
                    self.configmatrices.expand(configuration)
                )
            for configuration in self._configurations:
                configuration.postprocess()
        return self._configurations

    @property
    def rawconfig(self):
        return self._raw_content

    def __repr__(self):
        return "<ProjectConfig {0}>".format(self.ident)


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('ProjectConfig', ProjectConfig,
                        doc="Base Schema for Tendril "
                            "Project Configuration Files")
