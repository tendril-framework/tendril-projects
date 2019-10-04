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
Project Configuration Matrix Primitives
---------------------------------------
"""

import re
import copy
import itertools
from six import iteritems
from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList
from tendril.schema.helpers import SchemaObjectMapping

from .configurations import ConfigurationDefinitionList


class ConfigMatrixDimensionOption(NakedSchemaObject):
    def elements(self):
        e = super(ConfigMatrixDimensionOption, self).elements()
        e.update({
            'npart': self._p('npart', required=True),
            'tpart': self._p('tpart', required=True),
            'grouplist': self._p('grouplist', required=False, default=[],
                                 parser=SchemaObjectList),
            'motiflist': self._p('motiflist', required=False, default={},
                                 parser=SchemaObjectMapping),
            'sjlist':    self._p('sjlist',    required=False, default={},
                                 parser=SchemaObjectMapping),
            'genlist':   self._p('genlist',   required=False, default={},
                                 parser=SchemaObjectMapping),

        })
        return e


class ConfigMatrixDimensionOptionList(SchemaObjectList):
    _objtype = ConfigMatrixDimensionOption


class ConfigMatrixDimension(NakedSchemaObject):
    handle = 'name'

    def elements(self):
        e = super(ConfigMatrixDimension, self).elements()
        e.update({
            'name': self._p('name', required=True),
            'options': self._p('options', required=True,
                               parser=ConfigMatrixDimensionOptionList),
        })
        return e


class ConfigMatrixDimensionList(SchemaObjectList):
    _objtype = ConfigMatrixDimension


class ConfigMatrixSubconfigGenerator(NakedSchemaObject):
    def elements(self):
        e = super(ConfigMatrixSubconfigGenerator, self).elements()
        e.update({
            'configname':       self._p('configname', required=True),
            'desc':             self._p('desc',       required=True),
            '_dimensions':      self._p('dimensions', required=True,
                                        parser=SchemaObjectList),
            'actions':          self._p('actions',    required=True),
        })
        return e

    def expand(self, baseconfig, dimensions):
        rval = []

        ldimensions = []
        laxes = []
        for dimension in dimensions:
            if dimension.name in self._dimensions:
                ldimensions.append(dimension.name)
                laxes.append(dimension.options)

        for vector in itertools.product(*laxes):
            # TODO Review implications of deepcopy on new fat config objects
            nconfig = copy.deepcopy(baseconfig)
            nconfig.configname = self.configname
            nconfig.desc = self.desc
            for idx, component in enumerate(vector):
                dimname = ldimensions[idx]

                # Update configname
                nconfig.configname = nconfig.configname.replace(
                    '<{0}:{1}>'.format(dimname, 'npart'), component.npart
                )

                # Collapse repeated separators
                nconfig.configname = '-'.join(
                    re.split('-+', nconfig.configname)
                )

                # Update desc
                nconfig.desc = nconfig.desc.replace(
                    '<{0}:{1}>'.format(dimname, 'tpart'), component.tpart
                )

                # Update all others
                for param, action in iteritems(self.actions):
                    if action == 'pass':
                        continue
                    if action == 'extend':
                        if param == 'grouplist':
                            nlist = [x for x in component.grouplist
                                     if x is not None]
                            nconfig.grouplist.extend(nlist)
                            continue
                    if action == 'update':
                        if param in ['genlist', 'sjlist']:
                            getattr(nconfig, param).update(
                                getattr(component, param)
                            )
                            continue
                    raise AttributeError(
                        "{0} Action not recognized for {1} {2}"
                        "".format(action, param, self.configname)
                    )
            rval.append(nconfig)
        return rval


class ConfigMatrixSubconfigGeneratorList(SchemaObjectList):
    _objtype = ConfigMatrixSubconfigGenerator


class ConfigMatrixDefinition(NakedSchemaObject):
    handle = 'baseconfig'

    def elements(self):
        e = super(ConfigMatrixDefinition, self).elements()
        e.update({
            'baseconfig': self._p('baseconfig', required=True),
            'dimensions': self._p('dimensions', required=True,
                                  parser=ConfigMatrixDimensionList),
            'subconfigs': self._p('subconfigs', required=True,
                                  parser=ConfigMatrixSubconfigGeneratorList),
        })
        return e

    def expand(self, baseconfig):
        rval = ConfigurationDefinitionList([])
        for subconfig in self.subconfigs:
            rval.extend(subconfig.expand(baseconfig, self.dimensions))
        return rval


class ConfigMatrixDefinitionList(SchemaObjectList):
    _objtype = ConfigMatrixDefinition

    def expand(self, baseconfig):
        if baseconfig.configname not in self.handles:
            rval = ConfigurationDefinitionList([])
            rval.append(baseconfig)
            return rval
        return self.get(baseconfig.configname).expand(baseconfig)
