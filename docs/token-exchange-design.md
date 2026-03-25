# Token 交易所设计草案（TokenTrader）

## 核心思路
- 把闲置 API 配额转化为执行力供给；
- 用内部 `token_credit` 做统一结算单位；
- 通过价格/质量/时延/可靠性做撮合。

## 当前原型模块
- `src/tokentrader/models.py`：数据模型
- `src/tokentrader/engine.py`：评分撮合
- `src/tokentrader/service.py`：注册登录、会话、业务服务
- `src/tokentrader/server.py`：HTTP API + 静态前端
- `src/tokentrader/web/`：前端页面
