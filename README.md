# TokenTrader

TokenTrader 是一个「模型 Token 兑换与任务执行撮合」项目原型。包含：

- 邮箱注册/登录
- 报价与模拟执行
- Web 前端交易台

## 启动

```bash
PYTHONPATH=src python -m tokentrader.server
```

浏览器打开：http://127.0.0.1:8080

## 测试

```bash
pytest -q
```
