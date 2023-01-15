import typer

from .config import app as config_app
from .new import app as new_app

app = typer.Typer()


@app.command()
def stats():
    print("Printing stats.")


app.add_typer(config_app, name="config")
app.add_typer(new_app, name="new")


if __name__ == "__main__":
    app()
