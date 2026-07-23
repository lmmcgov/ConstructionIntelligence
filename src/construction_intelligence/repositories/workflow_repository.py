from construction_intelligence.core.workflow import Workflow

from .base import Repository


class WorkflowRepository(Repository[Workflow]):
    """Repository for Workflow objects."""