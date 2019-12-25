

from .config import ProjectConfig


def load(manager):
    manager.load_schema('ProjectConfig', ProjectConfig,
                        doc="Base Schema for Tendril "
                            "Project Configuration Files")
