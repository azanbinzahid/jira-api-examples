var jirauser = "";
var jiraauth = "";
var jiraurl  = "";

function whenStatusChnagedToInProgress(issueKey) {
  var parameters = {
    method : "get",
    accept : "application/json",
    headers: {"Authorization" : "Basic " + Utilities.base64Encode( jirauser + ":" + jiraauth )}    
   };
  var final = []
  var jira_url = "https://" + jiraurl + "/rest/api/2/issue/"+ issueKey + "?expand=changelog" ;
  var text = UrlFetchApp.fetch(jira_url, parameters).getContentText();
  var data = JSON.parse(text);


  var noneFlag = false
  var status_change_date = ""
  
  data.changelog.histories = data.changelog.histories.reverse()
  for (var h in data.changelog.histories)
  {
    for (var hi in data.changelog.histories[h].items)
    {
      if (data.changelog.histories[h].items[hi].field == 'status' && data.changelog.histories[h].items[hi].toString == "In Progress")
      {
        noneFlag = true
        status_change_date = Utilities.formatDate(new Date(data.changelog.histories[h].created), "GMT", "MM/dd/yyyy")
        break
      }
    }
    
    if (noneFlag) 
    {
      break
    }
    
  }
  return status_change_date;
}
