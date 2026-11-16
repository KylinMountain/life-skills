# Android APK 检查（2026-11-16）

## 来源与样本

官方页 https://m.fang.com/clientindex.jsp?city=cn 的房天下主应用下载按钮指向 https://a.app.qq.com/o/simple.jsp?pkgname=com.soufun.app&ckey=CK1358430372554 。该页给出版本 9.139.2、大小 128395542 字节、下载地址 https://imtt.dd.qq.com/sjy.00022/sjy.00004/16891/apk/7D5CAF113E30F90BE1448B24BADA5ABE.apk?fsname=com.soufun.app_9.139.2.apk 。实际下载完成，ZIP 可读，SHA256：549acaa6ff66abe46047db7a3af4defec2515a43a5d5664f5ae814450fe83b35。版本/包名来自下载页，未独立验证 Android 签名。APK 留在调查工作目录，不随 Skill 分发。

## 静态证据与边界

包内含 lib/arm64-v8a/libDexHelper.so 与 libDexHelper-x86.so；classes.dex 大小 93174232，DEX 头部 string_ids_size 仅 1206，而后部仍有大量业务类名和字符串。存在加固迹象，尚未恢复完整业务调用关系。assets/soufun.zip 是加密 ZIP，本次未解密。初次静态检查时未安装或运行 APK，也未做动态抓包。后续运行状态见文末。

classes.dex 可读字符串包括 GetEsfProjLastestTimeDealInfo、GetEsfTuiProjDealHouseInfo、GetDealList、GetHouseDealDetail、EsfDealHouseInfo、EsfDistrictDealHouseList；字段样式字符串包括 DealDateTime、DealMoney、DealSource、sDealPrice。这些仅为候选符号：不能证明其对应当前小区列表，不能据此写请求参数、价格单位、响应 schema 或认证算法。详细偏移见 evidence/apk-candidates.json，偏移相对 APK 解压后的 classes.dex。

静态存在完整入口 https://soufunapp.3g.fang.com/http/sfservice.jsp ，也存在 soufunappesf.3g.fang.com/http/ 主机路径。本次仅对完整入口做无参数 GET，实际 HTTP 411，Content-Type text/xml，响应为 result=0，message=验证失败-invalid vua，见 evidence/app-entry-response.xml。这只证明该次请求因 vua 校验失败，不证明成交 API 可用、不可用、登录要求或完整价格是否存在。没有拼造 vua 或把候选方法名拼成可用接口。

## 后续使用

查询成交仍走已实测的网页流程。本次 Android 调查未取得成交响应，禁止把候选符号写成“已验证 API”。要验证 App 价格，需要在可运行 Android 的设备上正常打开北苑一村成交页面，记录正常客户端请求与响应；再核对请求参数、分页、认证依赖和金额字段。若需登录，由用户在设备上完成，证据中去除令牌、Cookie 与设备标识。只有实际响应确认后才更新可调用接口说明。

## 后续真实运行（同日）

真实 App 已运行、实际成交请求已捕获。详见 [App 请求与价格字段验证](app-api.md)。实际北苑一村请求为 soufunappesf.3g.fang.com/http/sf2014.jsp 的 GetDealList；返回未遮罩数值字段，但存在总价/面积/单价不一致，未验证为真实精确成交价。原样重放第一页成功；早期只改page=2会MD5校验失败，后续同时重算wirelesscode与p-v-c已成功获得第二页，详见app-api.md。静态候选符号不再作为已验证 API 的依据。

仓库位于外置硬盘 /Volumes/mdata/Projects/life-skills；SDK、镜像、APK、设备状态、代理私钥、临时请求只在忽略目录 .local/。Skill 只保留去除客户端认证信息的必要证据。
