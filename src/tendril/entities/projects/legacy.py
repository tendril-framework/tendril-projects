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
Legacy Project Configuration Infrastructure Support
---------------------------------------------------
"""

import warnings


class ProjectConfigLegacyMixin(object):
    # def testvars(self, configname):
    #     rval = {}
    #     for motif in self.motiflist:
    #         for k, v in self._configdata['motiflist'][motif].iteritems():
    #             rval[':'.join([motif, k])] = v
    #     for configuration in self._configdata['configurations']:
    #         if configuration['configname'] == configname:
    #             try:
    #                 rval.update(configuration['testvars'])
    #             except KeyError:
    #                 pass
    #             if "motiflist" in configuration.keys():
    #                 for motif in configuration['motiflist']:
    #                     for k, v in configuration['motiflist'][motif].iteritems():
    #                         rval[':'.join([motif, k])] = v
    #     return rval

    # Legacy Support

    @property
    def indicative_pricing_folder(self):
        warnings.warn("Deprecated Access of indicative_pricing_folder",
                      DeprecationWarning)
        return self.pricingfolder

    @property
    def configdata(self):
        warnings.warn("Deprecated Access of configdata. "
                      "Use rawconfig instead",
                      DeprecationWarning)
        return self.rawconfig

    @property
    def motif_refdeslist(self):
        warnings.warn("Deprecated Access of motif_refdeslist. "
                      "Use motiflist.keys() instead",
                      DeprecationWarning)
        return self.motiflist.keys()

    def motif_baseconf(self, refdes):
        warnings.warn("Deprecated Access of motif_baseconf. "
                      "Use motiflist.get() instead",
                      DeprecationWarning)
        return self.motiflist.get(refdes)

    @property
    def group_names(self):
        warnings.warn("Deprecated Access of group_names. "
                      "Use grouplist.handles instead",
                      DeprecationWarning)
        return self.grouplist.handles

    def _get_group(self, groupname):
        warnings.warn("Deprecated Access of _get_group(). "
                      "Use grouplist.get() instead",
                      DeprecationWarning)
        return self.grouplist.get(groupname)

    def get_group_desc(self, groupname):
        warnings.warn("Deprecated Access of get_group_desc(). "
                      "Use grouplist.get().desc instead",
                      DeprecationWarning)
        return self._get_group(groupname).desc

    @property
    def file_groups(self):
        warnings.warn("Deprecated Access of file_groups(). "
                      "Use grouplist.file_groups instead",
                      DeprecationWarning)
        return self.grouplist.file_groups

    @property
    def configsection_names(self):
        warnings.warn("Deprecated Access of configsection_names. "
                      "Use configsections.handles instead",
                      DeprecationWarning)
        return self.configsections.handles

    def get_configsections(self):
        warnings.warn("Deprecated access of get_configsections."
                      "Use configsections.handles instead",
                      DeprecationWarning)
        return self.configsections.handles

    def configsection(self, sectionname):
        warnings.warn("Deprecated Access of configsection(). "
                      "Use configsections.get instead",
                      DeprecationWarning)
        return self.configsections.get(sectionname)

    def configsection_groups(self, sectionname):
        warnings.warn("Deprecated Access of configsection(). "
                      "Use configsections.get().grouplist instead",
                      DeprecationWarning)
        return self.configsections.get(sectionname).grouplist

    def configsection_configs(self, sectionname):
        warnings.warn("Deprecated Access of configsection(). "
                      "Use configsections.get().configurations instead",
                      DeprecationWarning)
        return self.configsections.get(sectionname).configurations

    def configsection_config(self, sectionname, configname):
        warnings.warn("Deprecated Access of configsection(). "
                      "Use configsections.get_modifier() instead",
                      DeprecationWarning)
        return self.configsections.get_modifier(sectionname, configname)

    def configsection_configgroups(self, sectionname, configname):
        warnings.warn("Deprecated Access of configsection(). "
                      "Use configsections.get_modifier().groups instead",
                      DeprecationWarning)
        return self.configsections.get_modifier(sectionname, configname).groups

    def get_sec_groups(self, sectionname, config):
        warnings.warn("Deprecated access of get_sec_groups",
                      DeprecationWarning)
        return self.configsections.get_modifier(sectionname, config).groups

    def _configmatrix_baseconfigs(self):
        warnings.warn("Deprecated access of configmatrix_baseconfigs."
                      "Use configmatrix.handles instead",
                      DeprecationWarning)
        return self.configmatrices.handles

    def _get_configmatrix(self, baseconfig):
        warnings.warn("Deprecated access of _get_configmatrix()."
                      "Use configmatrix.get() instead",
                      DeprecationWarning)
        return self.configmatrices.get(baseconfig)

    def _expand_configmatrix(self, baseconfig):
        warnings.warn("Deprecated access of _expand_configmatrix()."
                      "Use configmatrix.expand() instead",
                      DeprecationWarning)
        return self.configmatrices.expand(baseconfig)

    @property
    def configuration_names(self):
        warnings.warn("Deprecated access of configuration_names."
                      "Use configurations.handles instead",
                      DeprecationWarning)
        return self.configurations.handles

    def get_configurations(self):
        warnings.warn("Deprecated access of get_configurations. "
                      "Use configurations.handles instead",
                      DeprecationWarning)
        return self.configurations.handles

    def configuration(self, configname):
        warnings.warn("Deprecated access of configuration(). "
                      "Use configurations.get() instead",
                      DeprecationWarning)
        return self.configurations.get(configname)

    # def _configuration_direct_grouplist(self, configname):
    #     warnings.warn("Deprecated access of _configuration_direct_grouplist(). "
    #                   "Use configurations.get().grouplist instead",
    #                   DeprecationWarning)
    #     return self.configurations.get(configname).grouplist

    def get_configuration(self, configname):
        warnings.warn("Deprecated access of get_configuration(). "
                      "Use configurations.get().grouplist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).grouplist

    def configuration_motiflist(self, configname):
        warnings.warn("Deprecated access of configuration_motiflist(). "
                      "Use configurations.get().motiflist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).motiflist

    def get_configuration_motifs(self, configname):
        warnings.warn("Deprecated access of get_configuration_motifs(). "
                      "Use configurations.get().motiflist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).motiflist

    def configuration_genlist(self, configname):
        warnings.warn("Deprecated access of configuration_genlist(). "
                      "Use configurations.get().genlist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).genlist

    def get_configuration_gens(self, configname):
        warnings.warn("Deprecated access of get_configuration_gens"
                      "Use configurations.get().genlist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).genlist

    def configuration_sjlist(self, configname):
        warnings.warn("Deprecated access of configuration_sjlist"
                      "Use configurations.get().sjlist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).sjlist

    def get_configuration_sjs(self, configname):
        warnings.warn("Deprecated access of get_configuration_sjs"
                      "Use configurations.get().sjlist instead",
                      DeprecationWarning)
        return self.configurations.get(configname).sjlist

    def maintainer(self, configname=None):
        warnings.warn("Deprecated access of maintainer()"
                      "Use configurations.get().maintainer instead",
                      DeprecationWarning)
        if configname:
            return self.configurations.get(configname).maintainer
        else:
            return self._maintainer

    def description(self, configname=None):
        warnings.warn("Deprecated access of description()"
                      "Use configurations.get().description instead",
                      DeprecationWarning)
        if configname:
            return self.configurations.get(configname).description
        else:
            return self._description

    def status_config(self, configname):
        warnings.warn("Deprecated access of status_config()"
                      "Use configurations.get().status instead",
                      DeprecationWarning)
        return self.configurations.get(configname).status
