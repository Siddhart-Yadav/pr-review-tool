import datetime
import pytest
from domain.models import PullRequest
from application.report_service import filter_prs_by_date, calculate_pr_duration

def make_pr(created, closed=None):
    return PullRequest(
        id=1,
        title="Test PR",
        author="testuser",
        created_at=created.isoformat(),
        closed_at=closed.isoformat() if closed else None,
        reviews=[],
        pr_comments=[],
        state="closed"
    )

def test_filter_prs_by_date_includes_within_range():
    pr1 = make_pr(datetime.datetime(2024, 6, 1))
    pr2 = make_pr(datetime.datetime(2024, 6, 15))
    pr3 = make_pr(datetime.datetime(2024, 7, 1))
    prs = [pr1, pr2, pr3]
    since = datetime.datetime(2024, 6, 1)
    until = datetime.datetime(2024, 6, 30)
    # Convert since/until to isoformat for comparison
    filtered = filter_prs_by_date(prs, since, until)
    assert pr1 in filtered
    assert pr2 in filtered
    assert pr3 not in filtered

def test_calculate_pr_duration_closed():
    created = datetime.datetime(2024, 6, 1, 10, 0, 0)
    closed = datetime.datetime(2024, 6, 3, 12, 0, 0)
    duration = calculate_pr_duration(created, closed)
    assert duration.days == 2
    assert duration.seconds == 2 * 3600  # 2 hours

def test_calculate_pr_duration_open():
    created = datetime.datetime(2024, 6, 1, 10, 0, 0)
    now = datetime.datetime(2024, 6, 5, 10, 0, 0)
    duration = calculate_pr_duration(created, None, now=now)
    assert duration.days == 4

def test_pullrequest_str():
    pr = make_pr(datetime.datetime(2024, 6, 1))
    assert "Test PR" in str(pr)
    assert "testuser" in str(pr) 