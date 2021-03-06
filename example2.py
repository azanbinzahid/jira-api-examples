from jira import JIRA
import pandas as pd

from config import server, email, apiKey

jira = JIRA({"server": server},
            basic_auth=(email, apiKey))

startAt = 0
num_fetched = 0
total = 5000
final = []


while(num_fetched < total):
    JQL = "JQL QUERY HERE"

    data = jira.search_issues(jql_str=JQL, expand="changelog", startAt=startAt)

    total = data.total
    num_fetched += len(data)
    startAt = num_fetched

    # show total
    # print(data.total)
    # break

    for issue in data:
        noneFlag = False
        status_change_date = ""
        for history in reversed(issue.changelog.histories):
            for item in history.items:
                if item.field == 'status' and item.toString == "In Progress":
                    noneFlag = True
                    status_change_date = history.created
                    break
            if noneFlag:
                break

        if (noneFlag):
            row = []
            row.append(issue)
            row.append(status_change_date)
            row.append(issue.fields.issuetype)
            row.append(issue.fields.priority)
            row.append(issue.fields.status)
            row.append(issue.fields.created)
            row.append(issue.fields.project)
            final.append(row)

df = pd.DataFrame(final)
df.to_csv("status_changed_to_inprogress.csv", index=False, header=[
    "ID", "Status Change Date", "Type", "Priority", "Status", "Created", "Project"])
