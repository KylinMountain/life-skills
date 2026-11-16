# 房天下 Android 成交请求与分页实测

2026-11-16，在独立 Google ARM Android 11 / API30 中运行官方入口下载的房天下9.139.2（com.soufun.app），未登录账号。用户明确同意在该临时设备接受协议、观察请求、提取并仅在本地保存签名初始化材料及验证分页。证据不适用于其他账号、设备或未来版本的授权。

## 实际入口与参数

GET `https://soufunappesf.3g.fang.com/http/sf2014.jsp`

本次北苑一村实际参数依次为：city=南京、comarea=月苑、district=玄武、keyword=北苑一村、messagename=GetDealList、page=1、pagesize=20、wirelesscode=客户端计算值。保持大小写、顺序与原始URL编码；不要把另一个全市入口 soufunapp.3g.fang.com/http/sfservice.jsp 的请求直接套过来。具体结构见 evidence/app-request-shape.json，只有头名称，没有认证/设备值。

## 已验证的签名计算

从 APK 的 libSouFunSec.so 定位 SouFunSec.getSec、getVerify 及 MD5 计算；在独立测试进程中只读核对初始化状态。定义：

- Q：保持原顺序和百分号编码、移除wirelesscode后的ASCII query参数串；改变page后重新组成Q。
- N：本次客户端初始化段，32字节。
- K：本次原生库派生段，64字节。
- T：已有请求头p-v-t的时间戳字符串。
- W：`uppercase_hex(MD5(Q || N || K))`，作为query中的wirelesscode。
- C：`uppercase_hex(MD5(T || K || ASCII(W)))`，作为请求头p-v-c。

`||`是字节拼接，不加分隔符。该公式在本地复现已捕获北苑一村请求的两个校验值，并通过实际第一页、第二页请求验证。Q本身已是ASCII百分号编码串，不能先URL解码再签名。N/K的值未写入仓库、交付包或聊天，不能用随意常量替代。

这不是完整的全新会话生成方案：p-v-h、wirelessCheckCode等其余头沿用该授权测试会话，尚未独立还原其构造、有效期和必需性；初始化段的跨设备/版本稳定性未验证。不要把“本会话分页成功”夸大成完全不需要App、长期通用或所有版本通用。

## 分页验证结果

早期仅改page=2复用原wirelesscode：HTTP412/MD5验证失败。重算wirelesscode但沿用原p-v-c：HTTP412/invalid request；移除三项p-v头也未成功。按上述规则同时重算W和C后：

| 页 | HTTP | 记录数 | 首条日期 | 末条日期 |
|---|---|---|---|---|
| 1 | 200 | 20 | 2026-10-11 | 2026-02-04 |
| 2 | 200 | 20 | 2026-01-31 | 2025-06-01 |

两页40个houseid无重复，响应声明count=161；未读取全部161条。证据见 evidence/app-beiyuan-page1.xml、app-beiyuan-page2.xml、app-pagination-verification.json。XML证据仅摘取count/keywordtype/hit，不改写记录值；请求会话与签名材料不在这些文件中。

## 查询工具

脚本只依赖Python标准库与curl，且仅支持已验证GetDealList入口。使用已明确获准使用的本地未登录测试会话JSON（url/request_headers）与本地材料JSON（prefix_hex/suffix_hex）：

```sh
python3 scripts/fetch_app_pages.py \
  --session-file /private/local/session.json \
  --material-file /private/local/signing-material.json \
  --output-dir /private/local/result --page 1 --pages 2
```

路径是参数示例，不是本包内置文件。默认只查2页，单次最多10页；认证失败、响应异常、ID重复即停止，不无限重试。输出XML与records.json只含响应数据，不导出请求认证值。会话可能失效，不能靠重复重放来恢复；需重新用正常客户端捕获并核验。初始化材料缺失时不要猜密钥或读取真实手机；如需重新提取，先明确取得用户对该设备、材料、本地保存及用途的授权。将材料、会话、代理私钥仅放私有忽略目录。

## 字段和价格限制

`hit`包含houseid、projcode、projname、inserttime、buildarea、room、hall、forwardstr、floor、totalfloor、dealmoney、avgprice、companyname。inserttime与本次界面“签约时间”一致；不是据此证实官方交易日期。

首条72.87㎡、2026-10-11，页面为`7**万`，API返回dealmoney=`73`、avgprice=`10155`。第二条47.27㎡、2026-10-08，返回`76`和`16289`。以页面“万”的单位解释，首条73万元除面积约10017.84，和返回10155不一致；按单价乘面积约74万元。第二条亦约77万元而原字段为76。原因未验证，不得自动加1、用单价反推修复或称为真实精确成交价。

主表仍按用户要求保留页面价格遮罩原文；API数值仅作为明确标注的未核验附加字段，不能自动替换遮罩。scripts/parse_app_sales.py原样保留XML字段并标记unmasked_unverified，拒绝把认证错误当成记录。未登录页面显示“登录查看成交价”，见evidence/app-beiyuan-masked.png；登录后与详情页数据未验证。

## 数据来源与覆盖范围

本次北苑一村两页40条的companyname均为“贝壳”。因此实际样本至少包括平台标注来源为贝壳的数据，不能说只有房天下自营成交；也未独立核实贝壳原始记录或平台采集方式。companyname是记录来源标签，不等于完整的授权、同步频率或市场覆盖证明。

没有证据表明房天下覆盖南京所有中介、所有个人交易或全部官方网签；count=161仅是当前查询返回总数，不是全市场成交量。接口有city参数，本次只实测南京，不能外推全国所有城市/全部二手房。做分析时明确“房天下可查询样本”，不据此计算全市场成交量或中介市占率。
