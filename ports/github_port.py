from abc import ABC, abstractmethod
from typing import List

class GitHubPort(ABC):
    @abstractmethod
    async def fetch_pull_requests(self, repo: str) -> List:
        pass 