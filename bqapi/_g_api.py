"""
Tools for interacting with the Google API and its responses.
"""


import functools
import logging
import sys
import time

import oauth2client
from googleapiclient import discovery


logger = logging.getLogger('bqapi')


if sys.version_info[0] == 2:
    str_type = unicode
else:
    str_type = str


_DEFAULT_API = None


def _default_api():

    global _DEFAULT_API
    if _DEFAULT_API is None:
        cred = oauth2client.client.GoogleCredentials.get_application_default()
        _DEFAULT_API = discovery.build('bigquery', 'v2', credentials=cred)

    return _DEFAULT_API


def nullable(val, cast):

    """
    Allow for null fields when casting to Python types.
    """

    if val is None:
        return val
    else:
        return cast(val)


BQ_PY_TYPE_MAP = {
    'STRING': functools.partial(nullable, cast=str_type),
    'INTEGER': functools.partial(nullable, cast=int),
    'FLOAT': functools.partial(nullable, cast=float),
    'BOOLEAN': functools.partial(nullable, cast=bool),
    'TIMESTAMP': functools.partial(nullable, cast=float)
}


def poll_job(request, retries=2, wait=1):

    """
    Poll an `googleapi.job()` until it produces a result or times out.
    """

    while True:

        response = request.execute(num_retries=retries)

        job_complete = response.get('jobComplete')

        # All records fit in a single page OR the job just finished
        if job_complete is None or job_complete:
            return response
        else:
            logger.debug("Polling job ...")
            time.sleep(wait)


def parse_records(fields, types, records):
    for row in records:
        yield {f: BQ_PY_TYPE_MAP[t](v['v'])
               for f, t, v in zip(fields, types, row['f'])}


def iter_query_results(job, project):
    api = _default_api().jobs()

    kwargs = {'jobId': job, 'projectId': project}
    first = poll_job(api.getQueryResults(**kwargs))
    schema = first['schema']['fields']
    fields = [f['name'] for f in schema]
    types = [f['type'] for f in schema]

    records = first['rows']

    while True:
        for row in parse_records(fields=fields, types=types, records=records):
            yield row

        page_token = first.get('pageToken')
        if page_token:
            kwargs.update(pageToken=page_token)
        else:
            raise StopIteration

        records = poll_job(api.getQueryResults(**kwargs))['rows']
