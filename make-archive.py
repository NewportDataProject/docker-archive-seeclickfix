import urllib.request
import pandas as pd
import json

def get_issue_page(url):
    # GET a page of a dataset and convert to json object
    rawdata = urllib.request.urlopen(url).read()  # GET the data
    data = json.loads(rawdata)
    return data

def get_issues_by_place(place_url, max_pages=20, archived=False):
    # Get all issues from the seeclickfix api within a specific place_url. max_pages is set to avoid huge huge datasets
    # Returns a flattened pandas dataframe of issues.  Don't pull archived data unless specified.
    url = "http://seeclickfix.com/api/v2/issues?place_url=" + place_url # define the initial api query
    if archived:
        url = url + "&status=open,acknowledged,closed,archived"

    json_response = get_issue_page(url)
    total_pages = json_response['metadata']['pagination']['pages']

    if total_pages > max_pages:
        total_pages = max_pages  # enforce max page limit

    current_page = json_response['metadata']['pagination']['page']  # get current page
    next_url = json_response['metadata']['pagination']['next_page_url']  # get url for next page

    issues = json_response['issues']

    # iterate through pages
    while current_page < total_pages:
        url = next_url
        print("Getting page " + str(current_page) + " of " + str(total_pages))  # be verbose about where we are...
        data = get_issue_page(url)
        current_page = data['metadata']['pagination']['page']
        next_url = data['metadata']['pagination']['next_page_url']
        issues.extend(data['issues'])  # extend the issues

    issuesdf = pd.io.json.json_normalize(issues)  # flatten the issues

    # convert date columns to datetime objects
    date_cols = ['acknowledged_at', 'closed_at',
                 'created_at', 'reopened_at', 'updated_at']  # list date columns
    for col in date_cols:
        issuesdf[col] = pd.to_datetime(issuesdf[col])

    return issuesdf


response = get_issues_by_place('newport_2', max_pages=200, archived=True)

# output to json file
filename = './seeclickfix-archive/newport_2_issues_archive.json'
response.to_json(filename, orient="records")
