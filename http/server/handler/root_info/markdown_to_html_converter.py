import re

def markdown_to_html(markdown_text):
    # Überschriften
    markdown_text = re.sub(r"^# (.+)", r"<h1>\1</h1>", markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^## (.+)", r"<h2>\1</h2>", markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r"^### (.+)", r"<h3>\1</h3>", markdown_text, flags=re.MULTILINE)

    # Links
    markdown_text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', markdown_text)

    # Listen (zwei Ebenen)
    def replace_lists(match):
        lines = match.group(0).split("\n")
        html = []
        in_sublist = False

        for line in lines:
            if line.startswith("- - "):  # Zweite Ebene
                if not in_sublist:
                    html.append("<ul>")  # Starte neue Unterliste
                    in_sublist = True
                html.append(f"<li>{line[4:].strip()}</li>")
            elif line.startswith("- "):  # Erste Ebene
                if in_sublist:
                    html.append("</ul>")  # Schließe vorherige Unterliste
                    in_sublist = False
                html.append(f"<li>{line[2:].strip()}</li>")
        
        if in_sublist:
            html.append("</ul>")  # Schließe offene Unterliste am Ende

        return "<ul>" + "".join(html) + "</ul>"

    # Suche nach Listenblöcken und ersetze sie
    markdown_text = re.sub(r"(?:(?:^[-].+)(?:\n[-].*)*)", replace_lists, markdown_text, flags=re.MULTILINE)

    # Absätze
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
