"""
Classes representing BigQuery objects.
"""


from __future__ import division

import datetime


def ts2datetime(stamp):
    if isinstance(stamp, datetime.datetime):
        return stamp
    else:
        return datetime.datetime.fromtimestamp(int(stamp) / 1000)


class Table(object):

    def __init__(
            self, project, dataset, id, schema, url, num_rows, size,
            date_created, date_modified):

        self.project = project
        self.dataset = dataset
        self.id = id
        self.schema = schema
        self.url = url
        self.size = int(size)
        self.date_created = ts2datetime(date_created)
        self.date_modified = ts2datetime(date_modified)

        self._num_rows = int(num_rows)

    def __len__(self):
        return self._num_rows

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.path)

    @classmethod
    def from_response(cls, resp):
        return cls(
            project=resp['tableReference']['projectId'],
            dataset=resp['tableReference']['datasetId'],
            id=resp['tableReference']['tableId'],
            schema=resp['schema'],
            url=resp['selfLink'],
            num_rows=int(resp['numRows']),
            size=int(resp['numBytes']),
            date_created=ts2datetime(int(resp['creationTime'])),
            date_modified=ts2datetime(int(resp['lastModifiedTime'])))

    @property
    def path(self):
        return '{project}:{dataset}.{id}'.format(
            project=self.project,
            dataset=self.dataset,
            id=self.id)

    @property
    def fields(self):
        return [fld['name'] for fld in self.schema]
