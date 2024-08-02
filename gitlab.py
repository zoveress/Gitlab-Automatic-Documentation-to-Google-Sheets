import requests
import pygsheets
import os
import time
import traceback
import logging

def _get_all_group_ids(GITLAB_TOKEN):
    headers = {'Authorization': f'Bearer {GITLAB_TOKEN}'}
    group_ids = []
    page = 1
    per_page = 100
    GITLAB_API_URL = f'https://gitlab.com/api/v4/groups'
    while True:
        response = requests.get(GITLAB_API_URL, headers=headers, params={'page': page, 'per_page': per_page})
        response.raise_for_status()
        groups = response.json()
        if not groups:
            break
        for group in groups:
            group_ids.append(group['id'])
        page += 1
    return group_ids

def _get_gitlab_group_repos(GITLAB_TOKEN, GROUP_ID):
    per_page = 500
    GITLAB_API_URL = f'https://gitlab.com/api/v4/groups/{GROUP_ID}/projects'
    headers = {'Authorization': f'Bearer {GITLAB_TOKEN}'}
    response = requests.get(GITLAB_API_URL, headers=headers, params={'per_page': per_page})
    if response.status_code == 200:
        print (response.json())
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

def _format_data(repo_data):
    formatted_output = ""
    group_name       = ""
    if repo_data == []:
        logging.info("[_format_data] - Repo is Empty")
    else:
        formatted_output = []
        formatted_output.append(["Name", "Description", "URL", "Last Activity"])
        for repo in repo_data:
            if repo['description'] == "":
                description = "Not Available Yet"
            else:
                description = repo['description']
            logging.info(f"[_format_data] - {repo['name']} - {description} - {repo['web_url']} - {repo['last_activity_at']}")
            formatted_output.append([repo['name'], description, repo['web_url'], repo['last_activity_at']])
        group_name = repo['namespace']['name']
        logging.info("[_format_data] - All Repos processed successfully")
    return formatted_output, group_name

def _create_worksheet(sh, group_name):
    try:
        worksheet = sh.worksheet_by_title(group_name)
        logging.info(f"Worksheet '{group_name}' found.")
    except pygsheets.WorksheetNotFound:
        logging.info(f"Worksheet '{group_name}' not found. Creating new worksheet.")
        worksheet = sh.add_worksheet(group_name)
    return worksheet

def _add_to_gsheet(sheetname, formatted_output, GOOGLE_SHEET_CREDENTIALS_FILE, group_name):
    if formatted_output == "":
        logging.info("Repo is Empty")
    else:
        gc = pygsheets.authorize(service_file = GOOGLE_SHEET_CREDENTIALS_FILE)
        sh = gc.open(sheetname) 
        worksheet1 = _create_worksheet(sh, group_name)
        original_rows = worksheet1.rows
        original_cols = worksheet1.cols
        worksheet1.resize(rows=1, cols=1)
        worksheet1.resize(rows=original_rows, cols=original_cols)
        try:
            worksheet1.append_table(values=formatted_output)
            worksheet1.delete_rows(1)
        except Exception as e:
            logging.error("An error occurred:")
            traceback.print_exc()

def _main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    GITLAB_TOKEN                    = os.getenv("GITLAB_TOKEN") 
    SLEEP                           = os.getenv("SLEEP")
    SHEET_NAME                      = os.getenv("SHEET_NAME")
    GOOGLE_SHEET_CREDENTIALS_FILE   = os.getenv("GOOGLE_SHEET_CREDENTIALS_FILE")
    GROUP_IDS                       = _get_all_group_ids(GITLAB_TOKEN)
    logging.info(f"[_main] - {GROUP_IDS}")
    while True:
        for GROUP_ID in GROUP_IDS:
            repo_data                       = _get_gitlab_group_repos(GITLAB_TOKEN, GROUP_ID)
            formatted_output, group_name    = _format_data(repo_data)
            _add_to_gsheet(SHEET_NAME, formatted_output, GOOGLE_SHEET_CREDENTIALS_FILE, group_name)
            logging.info(f"[_main] - Data written to Google Sheets successfully!")
        logging.info(f"[_main] - Sleep for {SLEEP} seconds")
        time.sleep(int(SLEEP))

if __name__ == "__main__":
    try:
        _main()         
    except Exception as ex:
        logging.error(ex) 
        