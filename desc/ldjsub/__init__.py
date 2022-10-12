import importlib.metadata
__version__ = importlib.metadata.version('desc-ldjsub')

from .version import version
from .version import main_version
from .ldjtest import ldjtest
from .ldjtest import main_ldjtest
from .ldjtest import main_create_ldjtest
from .ldjsub  import main_ldj_create
from .ldjsub  import main_ldj_start
