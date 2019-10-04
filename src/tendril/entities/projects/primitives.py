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
Project Configuration Primitives
--------------------------------
"""

from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList
from tendril.schema.helpers import SchemaObjectMapping
from tendril.schema.helpers import FileList


class GroupDefinition(NakedSchemaObject):
    handle = 'name'

    def __init__(self, content, *args, **kwargs):
        self.basedir = kwargs.pop('basedir')
        super(GroupDefinition, self).__init__(content, *args, **kwargs)

    def elements(self):
        e = super(GroupDefinition, self).elements()
        e.update({
            'name': self._p('name', required=True),
            'desc': self._p('desc', required=False, default=''),
            'file': self._p('file', required=False, default=[],
                            parser=FileList,
                            parser_args={'basedir': self.basedir}),
        })
        return e

    @property
    def ident(self):
        return self.name

    @property
    def file_groups(self):
        return {f.filename: self.name for f in self.file}

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.ident)


class GroupDefinitionList(SchemaObjectList):
    _objtype = GroupDefinition
    _pass_args = ['basedir']

    @property
    def file_groups(self):
        rval = {}
        for group in self.content:
            rval.update(group.file_groups)
        return rval


class MotifDefinition(NakedSchemaObject):
    pass


class MotifDefinitionList(SchemaObjectMapping):
    _objtype = MotifDefinition


class SJDefinitionList(SchemaObjectMapping):
    pass


class GeneratorDefinitionList(SchemaObjectMapping):
    pass


class TestSuiteDefinition(SchemaObjectMapping):
    pass


class TestProtocolDefinition(SchemaObjectList):
    _objtype = TestSuiteDefinition
