from __future__ import annotations

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from markdown_renderer import render_markdown_to_pdf

app = FastAPI(title="Markdown PDF Renderer")


class MarkdownRequest(BaseModel):
    markdown: str = Field(min_length=1, description="Raw Markdown text to render")


@app.post(
    "/render/pdf",
    response_class=Response,
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF rendering of the provided Markdown",
        }
    },
)
async def render_pdf(body: MarkdownRequest) -> Response:
    """
    Convert Markdown content to a PDF document and return it as a binary response.
    """
    try:
        pdf_bytes = await render_markdown_to_pdf(body.markdown)
    except Exception as exc:  # pragma: no cover - defensive path
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    headers = {"Content-Disposition": 'inline; filename="document.pdf"'}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
