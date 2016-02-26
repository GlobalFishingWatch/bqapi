"""
Alternate interface.
"""


import bqapi


def query(statement, project, **kwargs):

    """
    Quickly execute a query and get all results back.

    Parameters
    ----------
    statement : str
        SQL statement.
    project : str
        BigQuery project name.
    kwargs : **kwargs
        Additional arguments for `bqapi.dbapi2.Connectione.execute()`.

    Yields
    ------
    dict
        Results
    """

    with bqapi.connect(project) as conn:
        return conn.execute(statement, **kwargs).fetchall()
