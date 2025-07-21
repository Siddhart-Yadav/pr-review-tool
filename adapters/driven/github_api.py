import httpx
import asyncio
from datetime import datetime
from domain.models import PullRequest, Review, Comment
from typing import List, Optional

GITHUB_API_URL = "https://api.github.com"

class GitHubAPIClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    async def fetch_pull_requests(self, repo: str, since: str = None, until: str = None) -> List[PullRequest]:
        async with httpx.AsyncClient(headers=self.headers) as client:
            # Fetch all PRs first, then filter by date
            url = f"{GITHUB_API_URL}/repos/{repo}/pulls?state=all"
            prs_resp = await client.get(url)
            prs_resp.raise_for_status()
            prs_data = prs_resp.json()

            # Filter by date range if provided
            if since or until:
                filtered_prs = []
                for pr in prs_data:
                    pr_date = datetime.strptime(pr["created_at"][:10], "%Y-%m-%d")
                    
                    # Check since date
                    if since:
                        since_date = datetime.strptime(since, "%Y-%m-%d")
                        if pr_date < since_date:
                            continue
                    
                    # Check until date
                    if until:
                        until_date = datetime.strptime(until, "%Y-%m-%d")
                        if pr_date > until_date:
                            continue
                    
                    filtered_prs.append(pr)
                prs_data = filtered_prs

            tasks = [self._fetch_pr_details(client, repo, pr) for pr in prs_data]
            return await asyncio.gather(*tasks)

    async def _fetch_pr_details(self, client, repo, pr_data):
        pr_number = pr_data["number"]
        reviews_task = asyncio.create_task(self._fetch_reviews(client, repo, pr_number))
        pr_comments_task = asyncio.create_task(self._fetch_pr_comments(client, repo, pr_number))
        reviews, pr_comments = await asyncio.gather(reviews_task, pr_comments_task)
        return PullRequest(
            id=pr_data["id"],
            title=pr_data["title"],
            author=pr_data["user"]["login"],
            created_at=pr_data["created_at"],
            closed_at=pr_data.get("closed_at"),
            reviews=reviews,
            pr_comments=pr_comments,
            state=pr_data["state"]
        )

    async def _fetch_reviews(self, client, repo, pr_number) -> List[Review]:
        reviews_resp = await client.get(f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/reviews")
        reviews_resp.raise_for_status()
        reviews_data = reviews_resp.json()
        tasks = [self._fetch_review_comments(client, repo, pr_number, review) for review in reviews_data]
        return await asyncio.gather(*tasks)

    async def _fetch_review_comments(self, client, repo, pr_number, review_data):
        # GitHub API does not directly link review comments to a review, so we fetch all review comments for the PR
        comments_resp = await client.get(f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/comments")
        comments_resp.raise_for_status()
        comments_data = comments_resp.json()
        # Filter comments by review_id if available
        review_id = review_data["id"]
        review_comments = [
            Comment(
                id=comment["id"],
                author=comment["user"]["login"],
                body=comment["body"],
                created_at=comment["created_at"]
            ) for comment in comments_data if comment.get("pull_request_review_id") == review_id
        ]
        return Review(
            id=review_id,
            reviewer=review_data["user"]["login"],
            state=review_data["state"],
            comments=review_comments,
            submitted_at=review_data["submitted_at"]
        )

    async def _fetch_pr_comments(self, client, repo, pr_number) -> List[Comment]:
        # PR comments are issue comments on the PR
        comments_resp = await client.get(f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/comments")
        comments_resp.raise_for_status()
        comments_data = comments_resp.json()
        return [
            Comment(
                id=comment["id"],
                author=comment["user"]["login"],
                body=comment["body"],
                created_at=comment["created_at"]
            ) for comment in comments_data
        ] 