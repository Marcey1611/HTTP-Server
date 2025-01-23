import re

def markdown_to_html(markdown_text):
    markdown_text = re.sub(r"^# (.+)", r"<h1>\1</h1>", markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^## (.+)", r"<h2>\1</h2>", markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^### (.+)", r"<h3>\1</h3>", markdown_text, flags=re.MULTILINE)

    markdown_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", markdown_text)
    markdown_text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", markdown_text)
    markdown_text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", markdown_text)
    markdown_text = re.sub(r"_(.+?)_", r"<em>\1</em>", markdown_text)

    markdown_text = re.sub(r"^\s*[-*] (.+)", r"<li>\1</li>", markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"(<li>.+</li>)", r"<ul>\1</ul>", markdown_text, flags=re.DOTALL)

    markdown_text = re.sub(r"\n\n+", r"</p><p>", markdown_text)
    markdown_text = f"<p>{markdown_text}</p>"

    return markdown_text

def generate_full_html(markdown_text):
    html_body = markdown_to_html(markdown_text)
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Readme</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #121212;
                color: #e0e0e0;
                padding: 20px;
                max-width: 800px;
                margin: auto;
            }}
            h1, h2, h3 {{
                color: #ffcc00;
                border-bottom: 1px solid #444;
                padding-bottom: 5px;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 10px;
            }}
            strong {{
                font-weight: bold;
                color: #ffcc00;
            }}
            em {{
                font-style: italic;
                color: #ff9900;
            }}
            a {{
                color: #42a5f5;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            code {{
                font-family: Consolas, "Courier New", monospace;
                background-color: #1e1e1e;
                color: #d4d4d4;
                padding: 2px 4px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    return html_template
