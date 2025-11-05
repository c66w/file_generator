## Markdown PDF Renderer API

### Base URL
```
http://<host>:6424
```

---

### POST `/render/pdf`

Render Markdown content to a PDF document.

#### Request
- **Headers**
  - `Content-Type: application/json`
- **Body**
  ```json
  {
    "markdown": "# Title\n\nSome text in *Markdown*."
  }
  ```
  - `markdown` *(string, required)*: Markdown source to convert.

#### Responses
- **200 OK**
  - Content-Type: `application/pdf`
  - Body: Binary PDF stream. Suggested filename: `document.pdf`.

- **400 Bad Request**
  - Returned if the payload is missing or invalid.
  - Example:
    ```json
    {
      "detail": [
        {
          "type": "string_too_short",
          "loc": ["body", "markdown"],
          "msg": "String should have at least 1 characters",
          "input": ""
        }
      ]
    }
    ```

- **500 Internal Server Error**
  - Returned when rendering fails.
  - Example:
    ```json
    {
      "detail": "Detailed error message"
    }
    ```

---

### Usage Example

```bash
curl -X POST "http://localhost:6424/render/pdf" \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello\n\nThis is a PDF."}' \
  --output document.pdf
```
