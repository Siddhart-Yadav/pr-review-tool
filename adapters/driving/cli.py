import typer
import asyncio
import os
from application.report_service import PRReportApplicationService
from adapters.driven.github_api import GitHubAPIClient
from adapters.driven.report_writers import ConsoleReportWriter
from adapters.driven.excel_report_writer import ExcelReportWriter

app = typer.Typer()

@app.command()
def pr_report(
    repo: str = typer.Argument(..., help="GitHub repository in the form owner/repo"),
    token: str = typer.Option(None, help="GitHub personal access token (or set GITHUB_TOKEN env var)"),
    excel: bool = typer.Option(False, help="Output report to Excel file"),
    filename: str = typer.Option("pr_report.xlsx", help="Excel filename (if --excel)"),
    since: str = typer.Option(None, help="Start date for filtering (YYYY-MM-DD)"),
    until: str = typer.Option(None, help="End date for filtering (YYYY-MM-DD)")
):
    """Generate a PR review report for a GitHub repository."""
    if token is None:
        token = os.environ.get("GITHUB_TOKEN")
    if not token:
        typer.echo("Error: GitHub token must be provided via --token or GITHUB_TOKEN env variable.", err=True)
        raise typer.Exit(code=1)
    github_client = GitHubAPIClient(token=token)
    if excel:
        report_writer = lambda prs: ExcelReportWriter().write(prs, filename)
    else:
        report_writer = ConsoleReportWriter()
    service = PRReportApplicationService(github_client, report_writer)
    asyncio.run(service.generate_report(repo, since=since, until=until))

if __name__ == "__main__":
    app() 