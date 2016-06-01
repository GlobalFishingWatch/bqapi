$ bqapi
=======

Command line interface.

.. code-block:: console

    $ bqapi --help                                                                                                                                                                                  ⏎
    Usage: bqapi [OPTIONS] COMMAND [ARGS]...

      bqapi command line interface

    Options:
      --help  Show this message and exit.

    Commands:
      query  Execute a query and send to GCS or stdout.


query
-----

.. code-block:: console

    $ bqapi query --help                                                                                                                                                                            ⏎
    Usage: bqapi query [OPTIONS] QUERY

      Execute a query and send to GCS or stdout.

    Options:
      --format NAME=VALUE  Format string substitutions in the query.
      --project-id NAME    BigQuery project name.  [required]
      --help               Show this message and exit.


Given a ``query.sql`` file like (note the ``{mmsi}`` string substitution):

.. code-block:: sql

    SELECT
        mmsi,
        STRING(timestamp) as timestamp,
        lat AS latitude,
        lon AS longitude,
        course AS cog,
        speed AS sog
    FROM
        TABLE_QUERY(table, 'true')

    WHERE
        mmsi = {mmsi}
        AND lon IS NOT NULL

    ORDER BY timestamp ASC

    LIMIT 10

We can do:

.. code-block:: console

    $ bqapi query query.sql --project-id NAME --format mmsi=123456789
    {"timestamp": "2014-01-01 00:06:12.000000", "latitude": 9.3740367889, "mmsi": 123456789, "cog": 43.2000007629, "longitude": -79.9022445679, "sog": 0.200000003}
    {"timestamp": "2014-01-01 00:12:38.000000", "latitude": 10.7150583267, "mmsi": 123456789, "cog": 65.4000015259, "longitude": -60.5835876465, "sog": 0.0}
    {"timestamp": "2014-01-01 00:21:15.000000", "latitude": 27.941942215, "mmsi": 123456789, "cog": 88.0, "longitude": -12.9348535538, "sog": 1.3999999762}
    {"timestamp": "2014-01-01 00:24:44.000000", "latitude": 37.655254364, "mmsi": 123456789, "cog": 288.299987793, "longitude": 120.3245620728, "sog": 0.0}
    {"timestamp": "2014-01-01 00:29:22.000000", "latitude": 20.8058891296, "mmsi": 123456789, "cog": 20.8999996185, "longitude": 111.0894622803, "sog": 4.0999999046}
    {"timestamp": "2014-01-01 00:37:03.000000", "latitude": 38.0097732544, "mmsi": 123456789, "cog": 112.0999984741, "longitude": 119.0266571045, "sog": 7.5999999046}
    {"timestamp": "2014-01-01 00:41:23.000000", "latitude": 20.8178291321, "mmsi": 123456789, "cog": 24.3999996185, "longitude": 111.0945968628, "sog": 3.4000000954}
    {"timestamp": "2014-01-01 00:49:06.000000", "latitude": 91.0, "mmsi": 123456789, "cog": 360.0, "longitude": 181.0, "sog": 102.3000030518}
    {"timestamp": "2014-01-01 00:59:20.000000", "latitude": 20.9188137054, "mmsi": 123456789, "cog": 22.7999992371, "longitude": 110.5520935059, "sog": 7.0}
    {"timestamp": "2014-01-01 00:59:52.000000", "latitude": -8.6019029617, "mmsi": 123456789, "cog": 132.8000030518, "longitude": 136.8265075684, "sog": 3.5999999046}
