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