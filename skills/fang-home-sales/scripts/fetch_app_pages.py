# coding: utf-8
"""Fetch bounded Fang GetDealList pages using an authorized local test session."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import parse_qsl, urlsplit, urlunsplit
from parse_app_sales import parse

ENDPOINT = ('soufunappesf.3g.fang.com', '/http/sf2014.jsp')


def signed_request(session, material, page):
    if page < 1:
        raise ValueError('page 必须大于0')
    url = urlsplit(session['url'])
    if url.scheme != 'https' or (url.netloc, url.path) != ENDPOINT:
        raise ValueError('仅接受已验证的房天下成交入口')
    pairs = parse_qsl(url.query, keep_blank_values=True)
    if dict(pairs).get('messagename') != 'GetDealList':
        raise ValueError('仅支持 GetDealList')
    for key in ['page', 'wirelesscode']:
        if sum(k == key for k, v in pairs) != 1:
            raise ValueError('请求参数缺失或重复: ' + key)
    # Preserve observed ordering, escaping and parameter spelling exactly.
    parts = []
    for part in url.query.split('&'):
        key = part.split('=', 1)[0]
        if key == 'wirelesscode':
            continue
        parts.append('page=' + str(page) if key == 'page' else part)
    query = '&'.join(parts)
    prefix = bytes.fromhex(material['prefix_hex'])
    suffix = bytes.fromhex(material['suffix_hex'])
    if len(prefix) != 32 or len(suffix) != 64:
        raise ValueError('本版本实测初始化段应为32和64字节，不能套用其他版本')
    code = hashlib.md5(query.encode('ascii') + prefix + suffix).hexdigest().upper()
    headers = dict(session['request_headers'])
    lowered = {k.lower(): v for k, v in headers.items()}
    if lowered.get('authorization') or lowered.get('cookie'):
        raise ValueError('此工具只支持明确授权的未登录测试会话')
    timestamp = lowered['p-v-t']
    check = hashlib.md5(timestamp.encode('ascii') + suffix + code.encode('ascii')).hexdigest().upper()
    for key in headers:
        if key.lower() == 'p-v-c':
            headers[key] = check
    if 'p-v-c' not in lowered:
        raise ValueError('缺少实际捕获的 p-v-c 头')
    return urlunsplit((url.scheme, url.netloc, url.path, query + '&wirelesscode=' + code, '')), headers


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--session-file', required=True, type=Path, help='已获授权的本地未登录会话捕获JSON')
    ap.add_argument('--material-file', required=True, type=Path, help='仅保存在本地的已验证签名材料JSON')
    ap.add_argument('--output-dir', required=True, type=Path)
    ap.add_argument('--page', type=int, default=1)
    ap.add_argument('--pages', type=int, default=2)
    args = ap.parse_args()
    if args.page < 1 or not 1 <= args.pages <= 10:
        ap.error('page必须大于0；单次pages限制为1至10，默认2')
    session = json.loads(args.session_file.read_text())
    material = json.loads(args.material_file.read_text())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_rows = []
    ids = set()
    for page in range(args.page, args.page + args.pages):
        url, headers = signed_request(session, material, page)
        target = args.output_dir / ('page-' + str(page) + '.xml')
        cmd = ['curl', '-sS', '--compressed', '--max-time', '30', '-o', str(target), '-w', '%{http_code}']
        for key, value in headers.items():
            if key.lower() not in ['host', 'connection', 'content-length', 'accept-encoding']:
                cmd += ['-H', key + ': ' + value]
        response = subprocess.run(cmd + [url], capture_output=True, text=True)
        if response.returncode or response.stdout != '200':
            raise SystemExit('请求失败，停止；HTTP=' + response.stdout + '。请重新捕获正常客户端会话，不循环重试。')
        result = parse(target.read_text(encoding='utf-8'))
        rows = result['records']
        page_ids = [row.get('houseid', '') for row in rows]
        if any(not value for value in page_ids) or len(set(page_ids)) != len(page_ids) or ids.intersection(page_ids):
            raise SystemExit('记录ID缺失或页间重复，停止并保留响应供核对')
        ids.update(page_ids)
        for row in rows:
            row['request_page'] = page
        all_rows.extend(rows)
        print('page=' + str(page) + ' HTTP=200 records=' + str(len(rows)), flush=True)
        (args.output_dir / 'records.json').write_text(json.dumps(all_rows, ensure_ascii=False, indent=2))
        count = result.get('declared_count_raw') or ''
        if count.isdigit() and len(ids) >= int(count):
            break
