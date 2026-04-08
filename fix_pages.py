from pathlib import Path
import re
root = Path('.')
files = list(root.glob('*.html')) + list(root.glob('pages/**/*.html'))
for path in files:
    if 'components' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    orig = text
    body_header_match = re.search(r'(<body[^>]*>)([\s\S]*?<header[\s\S]*?</header>)(\s*<section|\s*<main|\s*<div id="header-placeholder"|\s*<script)', text, re.IGNORECASE)
    if body_header_match and 'menu-hamburguer' in body_header_match.group(2) and 'nav-menu-container' in body_header_match.group(2):
        suffix_start = body_header_match.group(3)
        text = text[:body_header_match.start(2)] + '\n    <div id="header-placeholder"></div>\n' + suffix_start + text[body_header_match.end(2):]
    footer_match = re.search(r'<footer class="footer-elegante"[\s\S]*?</footer>', text, re.IGNORECASE)
    if footer_match:
        text = text[:footer_match.start()] + '    <div id="footer-placeholder"></div>\n' + text[footer_match.end():]
    if '<div id="footer-placeholder"></div>' not in text:
        script_match = list(re.finditer(r'<script[^>]*src=["\"][^"\"]*src/js/script\.js["\"][^>]*></script>', text, re.IGNORECASE))
        if script_match:
            m = script_match[-1]
            insert_pos = m.start()
            text = text[:insert_pos] + '    <div id="footer-placeholder"></div>\n\n' + text[insert_pos:]
    if '<div id="header-placeholder"></div>' not in text:
        body_open = re.search(r'<body[^>]*>', text, re.IGNORECASE)
        if body_open:
            insert_pos = body_open.end()
            text = text[:insert_pos] + '\n    <div id="header-placeholder"></div>\n' + text[insert_pos:]
    if text != orig:
        path.write_text(text, encoding='utf-8')
        print('Updated', path)
