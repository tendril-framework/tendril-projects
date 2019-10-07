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
Project Configuration Definition
--------------------------------
"""


from six import iteritems
from tendril.conventions.status import Status

from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList
from tendril.schema.helpers import SchemaObjectMapping


class ConfigurationDefinition(NakedSchemaObject):
    handle = 'configname'

    def elements(self):
        e = super(ConfigurationDefinition, self).elements()
        e.update({
            'configname':  self._p('configname', required=True),
            'desc':        self._p('desc',       required=True),
            'grouplist':   self._p('grouplist',  required=True,
                                   parser=SchemaObjectList),
            'motiflist':   self._p('motiflist',  required=False, default={},
                                   parser=SchemaObjectMapping),
            'sjlist':      self._p('sjlist',     required=False, default={},
                                   parser=SchemaObjectMapping),
            'genlist':     self._p('genlist',    required=False, default={},
                                   parser=SchemaObjectMapping),
            'config':      self._p('config',     required=False, default={},
                                   parser=SchemaObjectMapping),
            'testvars':    self._p('testvars',   required=False, default={}),
            'status':      self._p('status',     required=False, default=None,
                                   parser=Status),
            'maintainer':  self._p('maintainer', required=False, default=''),
            'description': self._p('desc',       required=False, default=''),
        })
        return e

    def preprocess(self):
        if 'default' not in self.grouplist:
            self.grouplist.append('default')

    def _apply_default_sjlist(self, sjlist):
        for key, state in iteritems(sjlist):
            if key not in self.sjlist.keys():
                self.sjlist[key] = state

    def _apply_configsections(self, configsections):
        if not len(self.config.keys()):
            return

        for section, sconfig in iteritems(self.config):
            self.grouplist.extend(
                configsections.get_modifier(section, sconfig).groups
            )

    def _apply_status(self, config):
        if not self.status or config.status_forced:
            self.status = config.status

    def apply_defaults(self, config):
        # TODO Motif defaults to be handled

        if not self.maintainer and hasattr(config, 'maintainer'):
            self.maintainer = config.maintainer()

        if not self.description and hasattr(config, 'description'):
            self.description = config.description()

        if hasattr(config, 'status'):
            self._apply_status(config)

        if hasattr(config, 'sjlist'):
            self._apply_default_sjlist(config.sjlist)

        if hasattr(config, 'configsections'):
            self._apply_configsections(config.configsections)

    def postprocess(self):
        while None in self.grouplist:
            self.grouplist.remove(None)

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.configname)


class ConfigurationDefinitionList(SchemaObjectList):
    _objtype = ConfigurationDefinition
