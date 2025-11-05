from __future__ import annotations

import re
from typing import List

from playwright.async_api import async_playwright


def _markdown_to_html_simple(markdown: str) -> str:
    """Simple Markdown-to-HTML converter supporting headings, paragraphs, and tables."""
    lines = markdown.splitlines()
    html_parts: List[str] = []
    in_table = False
    table_rows: List[List[str]] = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("|") and line.endswith("|") and line.count("|") >= 2:
            if not in_table:
                in_table = True
                table_rows = []

            cells = [c.strip() for c in line.split("|")[1:-1]]

            if re.match(r"^\|\s*:?[-]+:?\s*(\|\s*:?[-]+:?\s*)+\|$", line):
                i += 1
                continue

            table_rows.append(cells)
            i += 1
            continue

        if in_table and table_rows:
            html_parts.append("<table>")
            for idx, row in enumerate(table_rows):
                tag = "th" if idx == 0 else "td"
                html_parts.append("<tr>")
                for cell in row:
                    html_parts.append(f"<{tag}>{cell}</{tag}>")
                html_parts.append("</tr>")
            html_parts.append("</table>")
            table_rows = []
            in_table = False

        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            html_parts.append(f"<h{level}>{text}</h{level}>")
        elif line.strip():
            html_parts.append(f"<p>{line}</p>")

        i += 1

    if in_table and table_rows:
        html_parts.append("<table>")
        for idx, row in enumerate(table_rows):
            tag = "th" if idx == 0 else "td"
            html_parts.append("<tr>")
            for cell in row:
                html_parts.append(f"<{tag}>{cell}</{tag}>")
            html_parts.append("</tr>")
        html_parts.append("</table>")

    return "\n".join(html_parts)


async def render_markdown_to_pdf(markdown_text: str) -> bytes:
    """
    Render Markdown as a PDF, using python-markdown when available and
    falling back to a simple parser when not.
    """
    try:
        import markdown  # type: ignore

        md = markdown.Markdown(extensions=["tables", "fenced_code"])
        html_content = md.convert(markdown_text)
    except ImportError:
        html_content = _markdown_to_html_simple(markdown_text)

    html_document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_document)
        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
        )
        await browser.close()
        return pdf_bytes
