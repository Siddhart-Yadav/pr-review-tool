from rich.console import Console
from rich.table import Table
from datetime import datetime

def calculate_duration(created_at: str, closed_at: str = None) -> tuple:
    """Calculate duration between creation and closure dates."""
    created = datetime.strptime(created_at[:19], "%Y-%m-%dT%H:%M:%S")
    
    if closed_at:
        closed = datetime.strptime(closed_at[:19], "%Y-%m-%dT%H:%M:%S")
        delta = closed - created
        days = delta.days
        return days, format_duration(delta), closed_at[:10]
    else:
        # Still open
        now = datetime.now()
        delta = now - created
        days = delta.days
        return days, format_duration(delta), "Still open"

def format_duration(delta) -> str:
    """Format duration in human readable format."""
    days = delta.days
    if days == 0:
        return "Same day"
    elif days == 1:
        return "1 day"
    elif days < 7:
        return f"{days} days"
    elif days < 30:
        weeks = days // 7
        remaining_days = days % 7
        if remaining_days == 0:
            return f"{weeks} week{'s' if weeks > 1 else ''}"
        else:
            return f"{weeks} week{'s' if weeks > 1 else ''}, {remaining_days} day{'s' if remaining_days > 1 else ''}"
    else:
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"{months} month{'s' if months > 1 else ''}"
        else:
            return f"{months} month{'s' if months > 1 else ''}, {remaining_days} day{'s' if remaining_days > 1 else ''}"

class ConsoleReportWriter:
    def write(self, prs):
        console = Console()
        table = Table(title="Pull Request Report")
        table.add_column("PR Title", style="bold")
        table.add_column("Author")
        table.add_column("State")
        table.add_column("Created At")
        table.add_column("Close Date")
        table.add_column("Days Open")
        table.add_column("Duration")
        table.add_column("# Reviews")
        table.add_column("Reviewers")
        table.add_column("# Review Comments")
        table.add_column("# PR Comments")
        for pr in prs:
            num_review_comments = sum(len(review.comments) for review in pr.reviews)
            reviewers = ", ".join([review.reviewer for review in pr.reviews]) if pr.reviews else "None"
            days_open, duration, close_date = calculate_duration(pr.created_at, pr.closed_at)
            table.add_row(
                pr.title,
                pr.author,
                pr.state,
                pr.created_at[:10],
                close_date,
                str(days_open),
                duration,
                str(len(pr.reviews)),
                reviewers,
                str(num_review_comments),
                str(len(pr.pr_comments))
            )
        console.print(table)
        console.print(f"[bold green]Total PRs:[/bold green] {len(prs)}") 