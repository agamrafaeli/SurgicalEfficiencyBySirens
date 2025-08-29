"""Render HTML reports using Jinja2 templates."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader


def render_report(template: Path, out: Path, context: Dict) -> None:
    env = Environment(loader=FileSystemLoader(str(template.parent)))
    html = env.get_template(template.name).render(**context)
    out.write_text(html, encoding="utf-8")
