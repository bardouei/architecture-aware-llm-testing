from dataclasses import dataclass
from typing import List


@dataclass
class RepositoryMetadata:

    files: List[str]

    modules: List[str]