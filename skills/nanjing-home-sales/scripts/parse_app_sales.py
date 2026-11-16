# coding: utf-8
"""Read observed Fang App XML without interpreting raw prices as verified sales."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def parse(text):
    root = ET.fromstring(text)
    if root.tag != 'hits' or root.find('hit') is None:
        raise ValueError('不是含成交记录的 hits XML，可能是认证失败或空响应')
    rows = []
    for hit in root.findall('hit'):
        row = {element.tag: element.text or '' for element in hit}
        row['price_status'] = 'unmasked_unverified' if row.get('dealmoney') else 'missing'
        rows.append(row)
    return {'declared_count_raw': root.findtext('count'), 'records': rows}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('xml', type=Path)
    args = ap.parse_args()
    try:
        result = parse(args.xml.read_text(encoding='utf-8'))
    except (ET.ParseError, ValueError) as error:
        ap.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))
