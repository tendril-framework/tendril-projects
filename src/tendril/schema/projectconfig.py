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
Product Definition Schema
-------------------------

"""


import os
import warnings
from decimal import Decimal
from tendril.schema.base import SchemaControlledYamlFile
from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList
from tendril.schema.helpers import FileList

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class ComponentGroupDefinition(NakedSchemaObject):
    def __init__(self, content, *args, **kwargs):
        self.basedir = kwargs.pop('basedir')
        super(ComponentGroupDefinition, self).__init__(content, *args, **kwargs)

    def elements(self):
        e = super(ComponentGroupDefinition, self).elements()
        e.update({
            self.name: self._p('name', required=True),
            self.desc: self._p('desc', required=False, default=''),
            self.file: self._p('file', required=False, default=[],
                               parser=FileList,
                               parser_args={'basedir': self.basedir})
        })
        return e

    @property
    def ident(self):
        return self.name

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.ident)


class ComponentGroupListing(SchemaObjectList):
    _objtype = ComponentGroupDefinition
    _pass_args = ['basedir']


class ProjectConfig(SchemaControlledYamlFile):
    supports_schema_name = 'ProjectConfig'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def __init__(self, projectfolder, *args, **kwargs):
        self._projectfolder = projectfolder
        super(ProjectConfig, self).__init__(self._cfpath, *args, **kwargs)

    @property
    def projectfolder(self):
        return self._projectfolder

    @property
    def _cfpath(self):
        return os.path.join(self._projectfolder, 'configs.yaml')

    @property
    def docfolder(self):
        raise NotImplementedError

    @property
    def pricingfolder(self):
        raise NotImplementedError

    @property
    def indicative_pricing_folder(self):
        warnings.warn("Deprecated Access of indicative_pricing_folder",
                      DeprecationWarning)
        return self.pricingfolder

    def elements(self):
        e = super(ProjectConfig, self).elements()
        e.update({
            'grouplist': self._p('grouplist', required=False,
                                 parser=ComponentGroupListing,
                                 parser_args={'basedir': self.projectfolder},
                                 default=[{'name': 'default',
                                           'desc': 'Unclassified'}]),
            # 'name':        self._p('name'),
            # 'core':        self._p('derive_sno_from', required=False),
            # 'calibformat': self._p('calibformat',     required=False, parser=self._get_calibformat),
            # 'cards':       self._p('cards',           required=False, parser=SimpleCardListing, default={}),
            # 'cables':      self._p('cables',          required=False, parser=SimpleCableListing, default={}),
            # 'labels':      self._p('labels',          required=False, parser=LabelListing, default={}),
            # 'line':        self._p(('productinfo', 'line',)),
            # 'info':        self._p('productinfo',     parser=self._get_info_instance),
            # 'pricing':     self._p('pricing',         required=False, parser=StructuredUnitPrice)
        })
        return e

    def schema_policies(self):
        policies = super(ProjectConfig, self).schema_policies()
        policies.update({})
        return policies

    def __repr__(self):
        return "<ProjectConfig {0}>".format(self.ident)


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('ProjectConfig', ProjectConfig,
                        doc="Base Schema for Tendril Project Configuration Files")
