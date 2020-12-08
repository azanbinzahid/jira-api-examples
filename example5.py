from jira import JIRA
from config import _

jira = JIRA({"server": _["server"]},
            basic_auth=(_["email"], _["apiKey"]))

my_list = [
    "XYZ-123",
    "XYZ-786"
]


for issue in my_list:
    jira.transition_issue(issue, "Merged")
    # jira.transition_issue(issue, 131)
