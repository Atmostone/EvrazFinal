import click


def create_cli(load_books, publisher):

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def load(tags):
        load_books(tags, publisher)

    return cli
