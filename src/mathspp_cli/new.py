"""Module containing the command `mathspp new`."""

import datetime
import string
from typing import Optional

import typer
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("mathspp_cli"),
    autoescape=select_autoescape(),
)

app = typer.Typer()


def to_slug(title: str) -> str:
    """Turn a blog post title into its slug."""
    allow = set(string.ascii_lowercase + string.digits + "-_")
    slug = "".join(char for char in title.lower().replace(" ", "-") if char in allow)
    return slug

env.filters["to_slug"] = to_slug


@app.command()
def article(
    title: str = typer.Argument(..., help="The title for the blog article"),
    tag: Optional[list[str]] = typer.Option(None, help="Tags for the article.", metavar="tag"),
    category: Optional[list[str]] = typer.Option(None, help="Categories for the article.", metavar="category"),
):
    frontmatter = env.get_template("frontmatter.yaml.template")
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    with open("C:/tmp/test.yaml", "w") as f:
        f.write(frontmatter.render(title=title, date=date, tags=tag, categories=category))
