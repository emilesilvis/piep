#!/usr/bin/env python3
from config import SITE_NAME 
from pathlib import Path
from datetime import datetime
import shutil, re, html
import markdown  # only external dependency


ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
OUT = ROOT / "out"
TEMPL = (ROOT / "template.html").read_text(encoding="utf-8")


def render(markdown_text):
    """convert md → html using python-markdown"""
    return markdown.markdown(
        markdown_text,
        extensions=[
            "fenced_code",
            "codehilite",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "codehilite",
                "use_pygments": True,
                "noclasses": False,
            }
        }
    )


def apply_template(title, body_html):
    return (TEMPL.replace("{{title}}", html.escape(title))
            .replace("{{content}}", body_html)
            .replace("{{year}}", str(datetime.now().year))
            .replace("{{site_name}}", SITE_NAME))


def build_post(md_path):
    raw = md_path.read_text(encoding="utf-8")
    h1, _, body = raw.partition("\n")
    title = h1.lstrip("# ").strip() or md_path.stem
    html_body = render(body)
    return title, apply_template(title, html_body)


def main():
    # clean & recreate output dir
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()

    # copy static assets
    for asset in ("style.css", ):
        src = ROOT / asset
        if src.exists(): shutil.copy(src, OUT / asset)

    # collect posts
    posts = sorted(POSTS.glob("*.md"), reverse=True)
    index_items = []

    for md in posts:
        title, full_html = build_post(md)
        slug = md.stem.split("-", 3)[-1]  # after the date
        fname = f"{slug}.html"
        (OUT / fname).write_text(full_html, encoding="utf-8")
        date = "-".join(md.stem.split("-", 3)[:3])
        index_items.append(
            f"<li><a href='{fname}'>{title}</a> <small>{date}</small></li>")

    index_html = apply_template(
        "Home", "\n<ul>\n" + "\n".join(index_items) + "\n</ul>")
    (OUT / "index.html").write_text(index_html, encoding="utf-8")


if __name__ == "__main__":
    main()
