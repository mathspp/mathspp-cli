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


def _create_article(
    title: str,
    slug: str,
    description: str,
    tags: list[str],
    categories: list[str],
    path_prefix: str = "",
):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    tags = sorted(set(tags))
    categories = sorted(set(categories + ["blogpost"]))

    frontmatter = env.get_template("frontmatter.yaml.template")
    with open("C:/tmp/test.yaml", "w") as f:
        f.write(
            frontmatter.render(
                categories=categories,
                date=date,
                description=description,
                path_prefix=path_prefix,
                tags=tags,
                title=title,
                slug=slug,
            )
        )

    item = env.get_template("item.md.template")
    with open("C:/tmp/item_test.yaml", "w") as f:
        f.write(
            item.render(
                description=description,
            )
        )


@app.command()
def article(
    title: str = typer.Argument(..., help="The title for the blog article"),
    slug: str = typer.Option("", help="Article slug."),
    description: str = typer.Option("TODO", help="Article description.", prompt=True),
    tag: list[str] = typer.Option(list, help="Tags for the article."),
    category: list[str] = typer.Option(list, help="Categories for the article."),
):
    _create_article(
        title=title,
        slug=slug,
        description=description,
        tags=tag,
        categories=category,
    )


@app.command()
def pydont(
    title: str = typer.Argument(..., help="The Pydon't title."),
    slug: str = typer.Option("", help="Pydon't slug."),
    description: str = typer.Option("TODO", help="Pydon't description.", prompt=True),
    tag: list[str] = typer.Option(list, help="Tags for the Pydon't."),
    category: list[str] = typer.Option(list, help="Categories for the Pydon't."),
):
    categories = category + ["pydont"]
    tags = tag + ["python"]
    _create_article(
        title=title,
        slug=slug,
        description=description,
        tags=tags,
        categories=categories,
    )
