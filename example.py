from jira import JIRA
import pandas as pd

jira = JIRA({"server": 'url'},
            basic_auth=("username", "pass"))

startAt = 0
num_fetched = 0
total = 5000
final = []

while(num_fetched < total):
    JQL = "JQL QUERY HERE"
    data = jira.search_issues(jql_str=JQL, fields=[
        'Keys'], maxResults=5000, expand="changelog", startAt=startAt)

    total = data.total
    num_fetched += len(data)
    startAt = num_fetched

    for issue in data:
        change = []
        for history in reversed(issue.changelog.histories):
            for item in history.items:
                if item.field == 'Key':
                    change.append(item.fromString)
                    change.append(item.toString)
        row = []
        row.append(issue)
        row.append(", ".join(change))
        final.append(row)

df = pd.DataFrame(final)
df.to_csv("test.csv", index=False, header=["Ticket ID", "Chnage in Keys"])
