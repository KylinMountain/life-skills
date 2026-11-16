"""Parse saved Fang transaction HTML; no network or external dependencies."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

class SalesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.parts = None
    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.parts = []
        if self.parts is not None and tag in ('p', 'h3', 'span'):
            self.parts.append(' ')
    def handle_data(self, data):
        if self.parts is not None:
            self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == 'li' and self.parts is not None:
            raw = ' '.join(''.join(self.parts).split())
            self.parts = None
            if '签约时间' not in raw or '㎡' not in raw:
                return
            date = re.search(r'签约时间[：:]\s*(\d{4}-\d{2}-\d{2})', raw)
            area = re.search(r'(\d+(?:\.\d+)?)㎡', raw)
            price = re.search(r'签约价格[：:]\s*([\d.*＊]+)\s*万', raw)
            room = re.search(r'\d+室\d+厅', raw)
            floor = re.search(r'\S*楼层\S*', raw)
            value = price.group(1) if price else None
            exact = bool(value and re.fullmatch(r'\d+(?:\.\d+)?', value))
            amount = float(value) if exact else None
            size = float(area.group(1)) if area else None
            orientation = raw[room.end():floor.start()].strip() if room and floor else None
            self.rows.append(dict(community=raw.split()[0], contract_date=date.group(1) if date else None,
                area_sqm=size, layout=room.group() if room else None, orientation=orientation,
                floor_raw=floor.group() if floor else None,
                price_raw=value+'万' if value else None,
                price_status='exact' if exact else 'masked' if value else 'missing',
                total_price_wan=amount, unit_price_yuan_sqm=round(amount*10000/size,2) if exact and size and size>0 else None,
                source_label='市场信息' if '市场信息' in raw else None, raw_text=raw))

def parse(text):
    parser = SalesParser()
    parser.feed(text)
    return parser.rows

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html', type=Path)
    ap.add_argument('--source-url', required=True)
    ap.add_argument('--captured-at', required=True)
    args = ap.parse_args()
    rows = parse(args.html.read_text(encoding='utf-8'))
    if not rows:
        ap.error('未识别到成交记录，请检查页面结构、验证码或错误响应')
    for row in rows:
        row.update(source_url=args.source_url, captured_at=args.captured_at)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
