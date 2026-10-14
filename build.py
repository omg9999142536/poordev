#!/usr/bin/env python3
"""poor-dev-pack: README.md -> index.html (套3d28风格)"""
import re, html, pathlib

SRC = pathlib.Path('/home/agentuser/poor-dev-pack/README.md')
DST = pathlib.Path('/home/agentuser/AIHOT/deploy/downloads/poor-dev-pack/index.html')

def md2h(s):
    lines = s.split('\n'); out = []; in_table = False
    num_re = re.compile(r'^\d+\. ')
    for l in lines:
        e = html.escape(l)
        if l.startswith('|'):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if set(cells[0]) <= set('- :'):
                continue
            tag = 'th' if not in_table else 'td'
            if not in_table:
                out.append('<table>')
            out.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
            in_table = True
            continue
        if in_table:
            out.append('</table>'); in_table = False
        if l.startswith('### '):
            out.append(f'<h3>{e[4:]}</h3>')
        elif l.startswith('## '):
            out.append(f'<h2>{e[3:]}</h2>')
        elif l.startswith('> '):
            out.append(f'<blockquote>{e[2:]}</blockquote>')
        elif l.startswith('- '):
            out.append(f'<li>{e[2:]}</li>')
        elif num_re.match(l):
            out.append('<li>' + num_re.sub('', e) + '</li>')
        elif l.strip():
            out.append(f'<p>{e}</p>')
    if in_table:
        out.append('</table>')
    return '\n'.join(out)

body = md2h(SRC.read_text())
page = f'''<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>穷鬼开发者套餐 · 26格0元起</title><style>body{{font-family:-apple-system,"PingFang SC",sans-serif;background:#f4f1ea;color:#333;max-width:800px;margin:0 auto;padding:16px}}h1{{font-size:22px}}h2{{margin-top:24px;border-left:4px solid #d4b96a;padding-left:8px}}table{{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;font-size:13px}}th{{background:#2d2a26;color:#fff;padding:8px}}td{{padding:8px;border-bottom:1px solid #eee}}blockquote{{background:#fff;border-left:4px solid #8a4fd3;padding:10px;border-radius:0 8px 8px 0;font-size:14px}}li{{margin:6px 0;font-size:14px}}p{{font-size:14px;line-height:1.6}}</style></head><body>{body}<p style="text-align:center;color:#999;font-size:12px;margin-top:32px"><a href="/downloads/needs/index.html" style="color:#8a4fd3">← 需求库</a> · <a href="/downloads/market/index.html" style="color:#8a4fd3">AI产物市场</a></p></body></html>'''
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(page)
print('written', DST, len(page))
