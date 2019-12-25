

from tendril.validation.base import ValidatableBase
from tendril.schema import ProjectConfig


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
            self._config_obj = self._config_class(self._project_folder)
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
    def modules(self):
        raise NotImplementedError

    def _validate(self):
        _ = self.config
