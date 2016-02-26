bqapi
=====

Experimental BigQuery interface for Python.


Installing
----------

.. code-block:: console

    $ pip install https://github.com/GlobalFishingWatch/bqapi

Or:

.. code-block:: console

    $ git clone https://github.com/GlobalFishingWatch/bqapi
    $ python bqapi/setup.py install


Example
-------

.. code-block:: python

    import bqapi

    with bqapi.connect('project-name') as conn:
        cur = conn.execute("""SELECT * FROM [dataset.table] LIMIT 1000""")
        for row in cur.fetchall():
            pas

Alternatively:

.. code-block:: python

    import bqapi

    sql = """SELECT * FROM [dataset.table] LIMIT 1000"""

    with bqapi.query(sql, project='project-name') as records:
        for row in records:
            pass