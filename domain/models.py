from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Comment:
    id: int
    author: str
    body: str
    created_at: str

@dataclass
class Review:
    id: int
    reviewer: str
    state: str
    comments: List[Comment]
    submitted_at: str

@dataclass
class PullRequest:
    id: int
    title: str
    author: str
    created_at: str
    closed_at: Optional[str]
    reviews: List[Review]
    pr_comments: List[Comment]
    state: str

@dataclass
class ReportSummary:
    total_prs: int
    total_reviews: int
    total_comments: int 