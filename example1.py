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

    # print(data.total)
    # break

    for issue in data:
        noneFlag = False
        for history in reversed(issue.changelog.histories):
            for item in history.items:
                if item.field == 'FILED_NAME_HERE':
                    if (item.fromString == None):
                        noneFlag = True
                        break
            if noneFlag:
                break

        if (noneFlag):
            issue.fields.labels.append(u"label-name")

            # update label
            # issue.update(fields={"labels": issue.fields.labels})

            row = []
            row.append(issue)
            row.append(issue.fields.issuetype)
            row.append(issue.fields.priority)
            row.append(issue.fields.status)
            row.append(issue.fields.created)
            row.append(issue.fields.project)
            final.append(row)

df = pd.DataFrame(final)
df.to_csv("platform_l3_chnaged_from_none.csv", index=False, header=[
          "ID", "Type", "Priority", "Status", "Created", "Project"])
