# 房天下北苑一村实测

采集日期：2026-11-16，Asia/Shanghai。浏览器访问用户完整链接返回 HTTP 200，标题“北苑一村二手房成交价格及成交数量-南京房天下”。原始主文档见 evidence/original.html；分页 HTML 见 evidence/page3.html。保留的是响应正文，不含请求认证头。

## 观察结论

主文档内 `.housecjList li` 首屏 32 条。首条北苑一村，72.87㎡，2室1厅，南，高楼层层/6层，签约时间 2026-10-11（市场信息），签约价格 `7**万`。不是完整价格。部分记录完全缺失价格。主文档该条 HTML 已是遮罩，不是仅 CSS 隐藏；本次未发现可核实的完整成交价。未验证 APP、登录后页面或官方网签，不承诺这些渠道可解锁。

页面 pageConfig：firstPgNum=32，stepByNum=16，allCount=161；searchParam 为 inc_lj=1、orderby=1、page=1、pagesize=32、projcodes=1810510714、district=玄武、keyword=北苑一村。161 仅页面声明，未取完验证。

实际滚动请求（GET，200；随机 r 原样见 evidence/requests.txt）：

`https://m.fang.com/chengjiao/ajaxgetmorefangdeallist/?city=nanjing&inc_lj=1&orderby=1&page=3&pagesize=16&projcodes=1810510714&district=%E7%8E%84%E6%AD%A6&keyword=%E5%8C%97%E8%8B%91%E4%B8%80%E6%9D%91`

返回 HTML 片段而非 JSON，16 条；DOM 32→48。首条 47.39㎡ / 2025-09-06，末条 64.98㎡ / 2025-05-12，均无价格。首屏占了两个16条页，首次追加实际 page=3；不要从 page=2 开始导致重叠。仅验证一次追加，不宣称末页、总数或全量覆盖已验证。

实际加载的前端脚本：`https://static.soufunimg.com/common_m/m_nodejs/js/chengjiao/main_chengjiao_list.js?_20261028001`。其中加载器明确使用该路径，transfer=searchParam 并将 pagesize 改成 stepByNum。证据为浏览器请求及响应，不从名称臆测 API。

## 解析字段

li 内 h3 为小区；p 中“签约价格”旁的 em 为遮罩原文；含㎡的 p 以 space span 分隔面积/户型/朝向/楼层；最后 p 为签约日期与“市场信息”标签。本样本无稳定交易 ID 或可用详情链接（a href 为 javascript:void(0)）。解析脚本保留 raw_text，不把缺失变成零。没有观察到独立 JSON 金额字段。

## 验证边界

本包学区部分验证的是分析流程完整性，未对具体学校招生政策做实查，不能作为北苑一村学区认定。重新使用时必须浏览当年官方文件。网络与网页结构可能变化，每次先小样本复核。

## 价格展示

按页面保留遮罩原文，如 `7**万`、`4**万`。不添加首位分类，不推导金额区间。
