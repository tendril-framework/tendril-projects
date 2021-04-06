

import importlib
from six import iteritems

from tendril.validation.base import ValidationContext
from tendril.utils.versions import get_namespace_package_names
from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


class ProjectLibraryManager(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._validation_context = ValidationContext(self.__module__)
        self._index = {}
        self._libraries = {}
        self._exc_classes = {}
        self._load_libraries()
        self._generate_index()

    def _load_libraries(self):
        logger.debug("Loading project library modules from {0}".format(self._prefix))
        modules = list(get_namespace_package_names(self._prefix))
        for m_name in modules:
            if m_name == __name__:
                continue
            m = importlib.import_module(m_name)
            m.load(self)
        logger.debug("Done loading project library modules from {0}".format(self._prefix))

    def install_library(self, name, library):
        logger.debug("Installing project library {0}".format(name))
        self._libraries[name] = library

    def install_exc_class(self, name, exc_class):
        self._exc_classes[name] = exc_class

    def __getattr__(self, item):
        if item in self._libraries.keys():
            return self._libraries[item]
        if item in self._exc_classes.keys():
            return self._exc_classes[item]
        raise AttributeError('No attribute {0} in {1}!'
                             ''.format(item, self.__class__.__name__))

    def export_audits(self):
        for name, library in iteritems(self._libraries):
            library.export_audit(name)

    def regenerate(self):
        for name, library in iteritems(self._libraries):
            log.info("Regenerating Project library '{0}'".format(name))
            library.regenerate()
        self._generate_index()

    def _generate_index(self):
        self.index = {}

        for lname, library in iteritems(self._libraries):
            for ident, projects in iteritems(library.index):
                if ident in self.index:
                    self.index[ident].extend(projects)
                else:
                    self.index[ident] = projects

    @property
    def idents(self):
        return self.index.keys()

    def is_recognized(self, ident):
        if ident in self.idents:
            return True
        return False

    def get_project(self, ident, get_all=False):
        if not ident.strip():
            raise self.nosymbolexception(
                "Ident cannot be left blank")

        if self.is_recognized(ident):
            if not get_all:
                return self.index[ident][0]
            else:
                return self.index[ident]

        raise self.noprojectexception(
            'Project {0} not found in project library'.format(ident))

    @property
    def noprojectexception(self):
        return self._exc_classes['ProjectNotFoundError']
