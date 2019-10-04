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
Project Configuration Section Elements
--------------------------------------
"""


from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList


class SectionConfigurationModifier(NakedSchemaObject):
    handle = 'configname'

    def elements(self):
        e = super(SectionConfigurationModifier, self).elements()
        e.update({
            'configname': self._p('configname', required=True),
            'desc': self._p('desc', required=False, default=''),
            'groups': self._p('groups', required=False, default=[],
                              parser=SchemaObjectList),
        })
        return e


class SectionConfigurationModifierList(SchemaObjectList):
    _objtype = SectionConfigurationModifier


class ConfigSectionDefinition(NakedSchemaObject):
    handle = 'sectionname'

    def elements(self):
        e = super(ConfigSectionDefinition, self).elements()
        e.update({
            'sectionname': self._p('sectionname', required=True),
            'desc': self._p('desc', required=False, default=''),
            'grouplist': self._p('grouplist', required=False, default=[],
                                 parser=SchemaObjectList),
            'configurations': self._p('configurations', required=False, default=[],
                                      parser=SectionConfigurationModifierList),
        })
        return e


class ConfigSectionDefinitionList(SchemaObjectList):
    _objtype = ConfigSectionDefinition

    def get_modifier(self, sectionname, configname):
        return self.get(sectionname).configurations.get(configname)
