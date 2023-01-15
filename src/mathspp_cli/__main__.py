import typer

from .config import app as config_app

app = typer.Typer()



@app.command()
def new():
    print("Creating something new.")


@app.command()
def stats():
    print("Printing stats.")


app.add_typer(config_app, name="config")


if __name__ == "__main__":
    app()
