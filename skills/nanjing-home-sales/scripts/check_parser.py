# coding: utf-8
"""Run offline checks against saved, observed Fang responses."""
from pathlib import Path
from parse_sales import parse

root = Path(__file__).resolve().parents[1]
a = parse((root / 'references/evidence/original.html').read_text())
b = parse((root / 'references/evidence/page3.html').read_text())
assert len(a) == 32 and len(b) == 16
assert a[0]['area_sqm'] == 72.87
assert a[0]['contract_date'] == '2026-10-11'
assert a[0]['price_raw'] == '7**万'
assert a[0]['price_status'] == 'masked'
assert all(row['total_price_wan'] is None and row['unit_price_yuan_sqm'] is None for row in a + b)
assert all(row['price_status'] == 'missing' for row in b)
assert b[0]['contract_date'] == '2025-09-06' and b[-1]['contract_date'] == '2025-05-12'
assert parse('<html>验证码</html>') == []
# Synthetic data checks units only, never mixed with observed records.
sample = parse('<li><h3>测试</h3><p>签约价格：100万</p><p>50㎡ 2室1厅 南 高楼层层/6层</p><p>签约时间：2026-01-01</p></li>')[0]
assert sample['unit_price_yuan_sqm'] == 20000
print('48 observed records and price handling checks passed')

from parse_app_sales import parse as parse_app
app = parse_app((root / 'references/evidence/app-beiyuan-page1.xml').read_text())
assert app['declared_count_raw'] == '161' and len(app['records']) == 20
assert app['records'][0]['houseid'] == '2523921'
assert app['records'][0]['dealmoney'] == '73'
assert app['records'][0]['avgprice'] == '10155'
assert app['records'][0]['price_status'] == 'unmasked_unverified'
assert app['records'][3]['dealmoney'] == ''
assert app['records'][3]['price_status'] == 'missing'
try:
    parse_app((root / 'references/evidence/app-page2-replay-error.xml').read_text())
except ValueError:
    pass
else:
    raise AssertionError('authentication failure must not be accepted as sales')
print('20 observed App records preserved; authentication failure rejected')

second = parse_app((root / 'references/evidence/app-beiyuan-page2.xml').read_text())
assert len(second['records']) == 20
assert second['records'][0]['inserttime'] == '2026-01-31'
assert second['records'][-1]['inserttime'] == '2025-06-01'
first_ids = {row['houseid'] for row in app['records']}
second_ids = {row['houseid'] for row in second['records']}
assert len(first_ids | second_ids) == 40 and not first_ids & second_ids
print('Two observed App pages contain 40 distinct record IDs')
