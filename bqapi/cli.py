"""
Command line interface
"""


import json
import os

import click

import bqapi


def _cb_query(ctx, param, value):

    """
    Let query be a string or path to file on disk.
    """

    if os.path.exists(value):
        try:
            with open(value) as f:
                return f.read()
        except IOError:
            raise click.BadParameter(
                "couldn't load query from path: {}".format(value))
    else:
        return value


def _cb_format(ctx, param, value):

    """
    Parse `--format name=value` into:

        {
            name: value
        }
    """

    value = (v.split('=', 1) for v in value)
    return {n: v for n, v in value}


project_id_option = click.option(
    '--project-id', metavar='NAME', required=True,
    help="BigQuery project name.")


@click.group()
def main():

    """
    bqapi command line interface
    """


@main.command()
@click.argument('query', callback=_cb_query)
@click.option(
    '--format', 'query_substitutions', metavar="NAME=VALUE", multiple=True,
    callback=_cb_format,
    help="Format string substitutions in the query.")
@project_id_option
def query(project_id, query_substitutions, query):

    """
    Execute a query and send to GCS or stdout.
    """

    if query_substitutions:
        query = query.format(**query_substitutions)

    for record in bqapi.query(query, project=project_id):
        click.echo(json.dumps(record))
