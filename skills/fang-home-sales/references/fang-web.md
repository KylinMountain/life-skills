# 房天下网页查询

入口路径为`https://m.fang.com/chengjiao/{city_code}/`。city_code从站点城市切换结果或用户实际链接取得，不凭城市拼音猜测。在目标城市页面搜索小区，核对城市、行政区、名称、地址和返回的projcode，再打开成交页。不同城市可用性和页面结构先做小样本核对；不支持或无数据时明确说明。

## 提取与分页

首屏记录可能直接在主文档HTML中，无需另找JSON。记录节点为`.housecjList li`：h3是小区名，含㎡的p提供面积、户型、朝向与楼层，含“签约时间”的p提供日期和平台来源标签。价格节点可能带星号或完全缺失。

保存实际HTML后运行：

```sh
python3 scripts/parse_sales.py response.html \
  --source-url '实际页面或分页URL' --captured-at 'ISO格式采集时间' > records.json
```

滚动页面并记录实际触发的请求。分页路径为`/chengjiao/ajaxgetmorefangdeallist/`，响应为HTML片段；参数必须沿用当前页面实际返回值。关注pageConfig中的firstPgNum、stepByNum、allCount和searchParam。首屏条数与追加页大小可能不同，首次追加未必是page=2。

每页核对记录数、日期边界与重复项。取得用户时间窗口之前的记录后，在确认日期降序的前提下停止；错误、验证码、重复页或达到上限时停止并报告截断。页面总数不代表已取全，也不代表全市场交易量。

价格按页面原文展示，如`7**万`；无价格记缺失，不记零。不能用星号数量或首位推算价格区间。保留“市场信息”等标签，不改称官方网签。
