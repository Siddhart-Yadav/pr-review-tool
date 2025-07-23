import datetime

def filter_prs_by_date(prs, since, until):
    """Filter PRs by creation date range (inclusive)."""
    if since is None and until is None:
        return prs
    filtered = []
    for pr in prs:
        if since and pr.created_at < since:
            continue
        if until and pr.created_at > until:
            continue
        filtered.append(pr)
    return filtered

def calculate_pr_duration(created_at, closed_at, now=None):
    """Calculate the duration a PR was open. If closed_at is None, use now."""
    if closed_at is None:
        closed_at = now or datetime.datetime.now(created_at.tzinfo)
    return closed_at - created_at

class PRReportApplicationService:
    def __init__(self, github_client, report_writer):
        self.github_client = github_client
        self.report_writer = report_writer

    async def generate_report(self, repo: str, since: str = None, until: str = None):
        prs = await self.github_client.fetch_pull_requests(repo, since=since, until=until)
        # Support both callable (lambda) and class-based writers
        if callable(self.report_writer):
            self.report_writer(prs)
        else:
            self.report_writer.write(prs) 