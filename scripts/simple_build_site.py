import os
from pathlib import Path

try:
    import markdown
except Exception:
    markdown = None

ROOT = Path('.')
DOCS = ROOT / 'docs'
OUT = ROOT / 'site_fallback'
OUT.mkdir(exist_ok=True)

TEMPLATE = '''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>body{{font-family:Segoe UI,Roboto,Arial,Helvetica,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}}nav a{{margin-right:1rem}}</style>
</head>
<body>
<nav>{nav}</nav>
<hr/>
{content}
</body>
</html>'''

def render(md_text):
    if markdown:
        return markdown.markdown(md_text, extensions=['fenced_code','tables','admonition'])
    else:
        return '<pre>'+md_text.replace('<','&lt;').replace('>','&gt;')+'</pre>'

def build():
    pages = []
    for md in sorted(DOCS.glob('*.md')):
        pages.append(md.name)

    nav = ' | '.join(f"<a href='{p.replace('.md','.html')}'>{p.replace('.md','')}</a>" for p in pages)

    for md in pages:
        p = DOCS / md
        text = p.read_text(encoding='utf-8')
        html = render(text)
        out_file = OUT / md.replace('.md','.html')
        out_file.write_text(TEMPLATE.format(title=md.replace('.md',''), nav=nav, content=html), encoding='utf-8')

    # copy assets if any
    print('Built fallback site to', OUT)

if __name__ == '__main__':
    build()
