# App 成交查询与分页

适用接口：GET `https://soufunappesf.3g.fang.com/http/sf2014.jsp`，`messagename=GetDealList`。协议适用范围为房天下Android 9.139.2的已授权未登录测试会话；其他版本和新会话需重新核对。

## 会话与签名

使用正常客户端取得目标查询的实际url和request_headers，保存到私有本地会话JSON。查询参数包含city、comarea、district、keyword、page、pagesize、wirelesscode。city使用正常客户端在目标城市实际返回的值；先切换城市、再查询小区并捕获会话，同时保留该城市的相关请求头。城市编码、小区代码和学校范围不能跨城市复用。保留实际大小写、顺序、编码和筛选范围，不把其他入口的参数直接套用。

签名材料JSON有prefix_hex与suffix_hex两个十六进制字段，对应32字节初始化段N与64字节派生段K。材料不随Skill分发。仅使用用户已明确授权的设备与材料；缺失时不得猜密钥、读取真实手机或硬编码捕获值。需要提取时，先明确取得对设备、材料、本地保存和用途的授权。

令Q为保持原顺序及百分号编码、移除wirelesscode后的ASCII query串，T为会话请求头p-v-t：

- `W = uppercase_hex(MD5(Q || N || K))`，写入wirelesscode。
- `C = uppercase_hex(MD5(T || K || ASCII(W)))`，写入请求头p-v-c。

`||`为字节拼接，不加分隔符。改变page后重算W和C，不先URL解码Q。其余头沿用获准使用的会话；p-v-h、wirelessCheckCode等的独立生成及有效期没有通用保证。此工具不能替代正常客户端建立全新会话，也不保证每个城市都开放同一接口。

## 执行

```sh
python3 scripts/fetch_app_pages.py \
  --community '用户指定的小区完整名称' \
  --session-file /private/local/session.json \
  --material-file /private/local/signing-material.json \
  --output-dir /private/local/result --page 1 --pages 2
```

路径为参数示例。仅依赖Python标准库和curl。单次仅一个明确小区；--community须与会话keyword一致，空keyword或仅区/城市筛选会被拒绝。每页最多20条，默认2页，单次最多10页；输出各页XML和records.json。CLI通过跨进程锁确保只有一个查询实例，跨页和跨小区相邻请求至少间隔5秒。不要在外部绕过工具并发限制。认证失败、限流、验证码、响应异常或记录ID重复时立即停止整个批次，不自动重试或继续下一小区。会话失效后重新通过正常客户端获取并核对。

会话头、设备标识、签名材料、代理私钥和临时抓包留在私有忽略目录，不放Git或交付包。不得将真实账号会话自动用于此未登录测试工具。

## 响应字段

XML的hits/count是平台声明的当前查询总数，hit是逐条记录。用`python3 scripts/parse_app_sales.py response.xml`离线提取。

| 字段 | 使用方式 |
|---|---|
| houseid | 记录标识，用于页内和页间重复检查 |
| projcode / projname | 小区代码 / 名称 |
| inserttime | 平台列表日期；与界面“签约时间”核对后展示 |
| buildarea | 面积，与界面核对单位 |
| room / hall | 室 / 厅 |
| forwardstr / floor / totalfloor | 朝向 / 楼层分段 / 总层数 |
| dealmoney / avgprice | 原样保留的金额 / 单价样式字段，空值记缺失 |
| companyname | 平台来源标签，不能当作独立核验结论 |

API数值可能与总价、面积、单价之间的计算不一致。分别保留原字段并标注未核验，不自动加减金额或反推“正确价格”。用户要求遮罩原文时，不用API数值替换页面遮罩。作图使用哪个单价字段、单位与缺失处理，必须明确说明。

数据是房天下可查询样本，来源标签可能包括其他中介；不能据此宣称覆盖全部中介、全部个人交易或官方网签。城市参数不证明全国完整覆盖。
