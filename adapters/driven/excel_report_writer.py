from openpyxl import Workbook
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

class ExcelReportWriter:
    def write(self, prs, filename="pr_report.xlsx"):
        wb = Workbook()
        ws = wb.active
        ws.title = "PR Report"
        ws.append(["PR Title", "Author", "State", "Created At", "Close Date", "Days Open", "Duration", "# Reviews", "Reviewers", "# Review Comments", "# PR Comments"])
        for pr in prs:
            num_review_comments = sum(len(review.comments) for review in pr.reviews)
            reviewers = ", ".join([review.reviewer for review in pr.reviews]) if pr.reviews else "None"
            days_open, duration, close_date = calculate_duration(pr.created_at, pr.closed_at)
            ws.append([
                pr.title,
                pr.author,
                pr.state,
                pr.created_at[:10],
                close_date,
                days_open,
                duration,
                len(pr.reviews),
                reviewers,
                num_review_comments,
                len(pr.pr_comments)
            ])
        wb.save(filename)
        print(f"Excel report saved as {filename}") 