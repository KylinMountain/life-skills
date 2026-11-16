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
print('Parser checks passed')
