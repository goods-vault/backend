import asyncio

import typer
from services.parser import fetch_categories

cli = typer.Typer()


@cli.command()
def load_categories():
    """
    Парсит категории и сохраняет их в базу данных.
    """
    result = asyncio.run(fetch_categories())
    # TODO: write categories to db
    print(result)


if __name__ == "__main__":
    cli()
