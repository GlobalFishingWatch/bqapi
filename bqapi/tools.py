from bqapi._api import _default_api


def list_projects():

    resp = _default_api().projects().list().execute()
    while resp is not None:
        for item in resp['projects']:
            yield item['projectReference']['projectId']
        next_page = resp.get('nextPageToken')
        if next_page:
            resp = _default_api().projects().list(pageToken=next_page).execute()
        else:
            resp = None


def job_info(project, job):
    api = _default_api()
    return api.jobs().get(projectId=project, jobId=job).execute()


def get_results(project, job):
    api = _default_api()
    return api.jobs().getQueryResults(projectId=project, jobId=job, maxResults=1000).execute()
