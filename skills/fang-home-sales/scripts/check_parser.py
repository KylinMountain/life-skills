# coding: utf-8
"""Offline parser checks with synthetic inputs; no captured transaction fixtures."""
from parse_sales import parse
from parse_app_sales import parse as parse_app

html = '<li><h3>测试小区</h3><p>签约价格：7**万</p><p>50㎡ 2室1厅 南 高楼层层/6层</p><p>签约时间：2026-01-01（市场信息）</p></li>'
masked = parse(html)[0]
assert masked['price_raw'] == '7**万' and masked['price_status'] == 'masked'
assert masked['total_price_wan'] is None and masked['unit_price_yuan_sqm'] is None
missing = parse(html.replace('签约价格：7**万', '下载APP查看'))[0]
assert missing['price_status'] == 'missing' and missing['total_price_wan'] is None
numeric = parse(html.replace('7**万', '100万'))[0]
assert numeric['unit_price_yuan_sqm'] == 20000
assert parse('<html>验证码</html>') == []
xml = '<hits><count>2</count><hit><houseid>a</houseid><dealmoney>73</dealmoney><avgprice>10155</avgprice></hit><hit><houseid>b</houseid><dealmoney/></hit></hits>'
rows = parse_app(xml)['records']
assert rows[0]['dealmoney'] == '73' and rows[0]['avgprice'] == '10155'
assert rows[0]['price_status'] == 'unmasked_unverified'
assert rows[1]['price_status'] == 'missing'
try:
    parse_app('<root><result>0</result><message>验证失败</message></root>')
except ValueError:
    pass
else:
    raise AssertionError('Authentication failure must not become a transaction')
assert parse_app('<hits><count>0</count></hits>') == {'declared_count_raw': '0', 'records': []}
try:
    parse_app('<hits><count>20</count></hits>')
except ValueError:
    pass
else:
    raise AssertionError('Missing nonempty records must not become an empty success')
print('Parser checks passed')

from fetch_app_pages import signed_request
from urllib.parse import urlencode, parse_qs, urlsplit
# Synthetic sessions check that pagination preserves the selected city and filters.
material = {'prefix_hex': (b'n' * 32).hex(), 'suffix_hex': (b'k' * 64).hex()}
for city in ['北京', '上海']:
    session = {'url': 'https://soufunappesf.3g.fang.com/http/sf2014.jsp?' + urlencode([('city', city), ('keyword', '测试小区'), ('messagename', 'GetDealList'), ('page', '1'), ('pagesize', '20'), ('wirelesscode', 'placeholder')]), 'request_headers': {'p-v-t': '1000000000000', 'p-v-c': 'placeholder'}}
    first_url, first_headers = signed_request(session, material, 1, '测试小区')
    second_url, second_headers = signed_request(session, material, 2, '测试小区')
    first, second = parse_qs(urlsplit(first_url).query), parse_qs(urlsplit(second_url).query)
    assert first['city'] == second['city'] == [city]
    assert first['keyword'] == second['keyword'] == ['测试小区']
    assert first['page'] == ['1'] and second['page'] == ['2']
    assert first['wirelesscode'] != second['wirelesscode']
    assert first_headers['p-v-c'] != second_headers['p-v-c']
    assert session['request_headers']['p-v-c'] == 'placeholder'
print('City and filter preservation checks passed')

# Explicit community scope is required before any request can be built.
import copy
for keyword, requested, page_size in [('', '测试小区', '20'), ('测试小区', '其他小区', '20'), ('测试小区', '测试小区', '100')]:
    scoped = copy.deepcopy(session)
    scoped['url'] = 'https://soufunappesf.3g.fang.com/http/sf2014.jsp?' + urlencode([('city', '北京'), ('keyword', keyword), ('messagename', 'GetDealList'), ('page', '1'), ('pagesize', page_size), ('wirelesscode', 'placeholder')])
    try:
        signed_request(scoped, material, 1, requested)
    except ValueError:
        pass
    else:
        raise AssertionError('Expanded or ambiguous query scope must be rejected')
print('Community scope and page-size checks passed')

# Check cross-process exclusion and throttling across successive community runs.
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import fetch_app_pages as client

with tempfile.TemporaryDirectory() as temp_dir:
    env = os.environ.copy()
    env['TMPDIR'] = temp_dir
    env['PYTHONPATH'] = str(Path(__file__).resolve().parent)
    with patch.object(client.tempfile, 'gettempdir', return_value=temp_dir):
        with client.serial_queries():
            child = subprocess.run([sys.executable, '-B', '-c', 'from fetch_app_pages import serial_queries\nwith serial_queries():\n print("unexpected")'], env=env, capture_output=True, text=True)
            assert child.returncode != 0 and '已有房天下查询' in child.stderr
        with patch.object(client.time, 'time', side_effect=[100.0, 101.0, 105.0, 106.0, 110.0]), patch.object(client.time, 'sleep') as sleep:
            with client.serial_queries() as wait:
                wait()
                wait()
            with client.serial_queries() as wait:
                wait()
            assert [call.args[0] for call in sleep.call_args_list] == [4.0, 4.0]
print('Cross-process exclusion and cross-run throttle checks passed')
