# github-enterprise-wechat

## 描述
Github，Jenkins事件自动推送企业微信的服务

## 特性
- 支持Github
    - [x] 支持PR
        - [x] opened, closed, reopened事件
- 支持Jenkins
    - [x] 支持notification插件
    - [x] 支持推送Job失败事件
- [x] 对接微信API
- [x] 消息模板化

## 环境变量
```bash
export WECHAT_CORP_ID=yyyyyyyyy
export WECHAT_BASE_URL=https://qyapi.weixin.qq.com/cgi-bin
export GITHUB_WECHAT_CORP_SECRET=xxxxxxxxxxx
export GITHUB_WECHAT_AGENT_ID=1000002
export CI_WECHAT_CORP_SECRET=xxxxxxxxxxx
export CI_WECHAT_AGENT_ID=1000002
```

## 安装
```bash
pip install -r requirements.txt

```

## 启动
```bash
python rest/endpoint.py

```
