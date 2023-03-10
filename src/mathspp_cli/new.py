"""Module containing the command `mathspp new`."""

import datetime
import string

import typer
from jinja2 import Environment, PackageLoader, select_autoescape

from .config import get_blog_path


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
    site_prefix: str = "",
):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    slug = slug if slug else to_slug(title)
    tags = sorted(set(tags))
    categories = sorted(set(categories + ["blogpost"]))

    blog_path = get_blog_path()
    article_path = blog_path / path_prefix / slug
    article_path.mkdir()

    frontmatter = env.get_template("frontmatter.yaml.template")
    frontmatter_path = article_path / "frontmatter.yaml"
    with open(frontmatter_path, "w") as f:
        f.write(
            frontmatter.render(
                categories=categories,
                date=date,
                description=description,
                site_prefix=site_prefix,
                slug=slug,
                tags=tags,
                title=title,
            )
        )

    item = env.get_template("item.md.template")
    item_path = article_path / "item.md"
    with open(item_path, "w") as f:
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
        categories=category,
        description=description,
        slug=slug,
        tags=tag,
        title=title,
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
        categories=categories,
        description=description,
        path_prefix="01.pydonts/",
        site_prefix="pydonts/",
        slug=slug,
        tags=tags,
        title=title,
    )
