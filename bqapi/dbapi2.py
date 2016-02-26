"""
Python DBAPI 2.0-ish interface to BigQuery.
"""


from __future__ import unicode_literals

import logging
import uuid

from bqapi import _g_api
from bqapi import bqobjects


logger = logging.getLogger('bqpi')


RETRIES = 3


class Cursor(object):

    """
    Database cursor.
    """

    def __init__(self, resp):
        self._jbos_api = _g_api._default_api().jobs()
        self._resp = resp

    @property
    def job(self):
        return self._resp['jobReference']['jobId']

    @property
    def project(self):
        return self._resp['jobReference']['projectId']

    def fetchone(self):
        return next(self.fetchall())

    def fetchall(self):
        return _g_api.iter_query_results(job=self.job, project=self.project)


class Connection(object):

    """
    Connection attached to a BigQuery project.
    """

    def __init__(self, project):

        """
        Parameters
        ----------
        project : str
            BigQuery project name.
        """

        self.project = project
        self._api = _g_api._default_api()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self):
        return "{cname}(project={project})".format(
            cname=self.__class__.__name__, project=self.project)

    @property
    def datasets(self):

        """
        List of datasets in this project.
        """

        resp = self._api.datasets().list(projectId=self.project).execute()
        return [d['datasetReference']['datasetId'] for d in resp['datasets']]

    def table_info(self, dataset, table):

        """
        Get information about a table.

        Parameters
        ----------
        dataset : str
            Dataset name.
        table : str
            Table name.

        Returns
        -------
        bqapi.bqobjects.Table
        """

        resp = self._api.tables().get(projectId=self.project, datasetId=dataset, tableId=table).execute()
        return bqobjects.Table.from_response(resp)

    def tables(self, dataset):

        """
        List tables contained in `dataset`.
        """

        resp = self._api.tables().list(
            projectId=self.project, datasetId=dataset).execute()
        return [t['tableReference']['tableId'] for t in resp['tables']]

    def execute(self, query, **kwargs):

        """
        Execute a query through the `bigquery.jobs.insert()` API.

        https://cloud.google.com/bigquery/docs/reference/v2/jobs

        Parameters
        ----------
        query : str
            SQL statement to execute.
        kwargs : **kwargs, optional
            Additional arguments for `configuration` parameter of the API
            call.  See URL above.

        Returns
        -------
        Cursor
        """

        kwargs.update(query=query)
        # Generate a unique job_id so retries
        # don't accidentally duplicate query
        job_id = str(uuid.uuid4())
        body = {
            'jobReference': {
                'projectId': self.project,
                'job_id': job_id
            },
            'configuration': kwargs
        }

        logger.debug("Submitting query with job ID '%s': %s", job_id, query)

        resp = self._api.jobs().insert(
            projectId=self.project,
            body=body).execute(RETRIES)

        return Cursor(resp)


def connect(*args):

    """
    Connect to a BigQuery project.  See `Connection()` for docs.
    """

    return Connection(*args)
