from jira import JIRA
from config import _

jira = JIRA({"server": _["server"]},
            basic_auth=(_["email"], _["apiKey"]))

issue_keys = [
    "XYZ-123",
    "XYZ-127"
    ]


for issue_key in issue_keys:
    jira.add_comment(issue_key, "new comment")
    
