# 南墙 API 工具

一个基于 Python 的南墙 API 交互工具，提供证书管理、站点配置和用户认证等功能。

## 南墙 WAF 介绍

南墙 WEB 应用防火墙（简称：uuWAF）是有安科技推出的一款全方位网站防护产品，率先实现了流量层、系统层、运行时层 3 层纵深防御功能。通过有安科技专有的 WEB 入侵异常检测等技术，结合有安科技团队多年应用安全的攻防理论和应急响应实践经验积累的基础上自主研发而成。协助各级政府、企/事业单位全面保护 WEB 应用安全，实现 WEB 服务器的全方位防护解决方案。

官网地址：[https://waf.uusec.com/#/?id=main](https://waf.uusec.com/#/?id=main)

## 功能特性

- 证书管理
  - 获取证书列表
  - 检查证书
  - 提交证书配置
  - 删除证书
- 站点配置
  - 获取站点列表
  - 更新站点配置
- 用户认证
  - 用户名密码登录
  - 支持双因素认证（OTP）

## 环境要求

- Python 3.x
- 必需的 Python 包：
  - requests
  - jwt
  - urllib3

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/obaby/baby-nanqiang-waf-api-tools.git
cd baby-nanqiang-waf-api-toos
```

2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 使用说明

### 基础用法

```python
from baby_nanqiang_api_tools import NanQiangAPI

# 初始化 API 客户端
api = NanQiangAPI(base_url="https://lang.bi:443")

# 登录
result = api.login(username="your_username", password="your_password")
if result:
    print("登录成功")
    
    # 获取证书列表
    cert_list = api.get_cert_list()
    if cert_list:
        parsed_certs = api.parse_cert_list(cert_list)
        print("证书列表:", parsed_certs)
```

### 证书管理

```python
# 从文件检查证书
cert_result = api.check_cert_from_files("cert.pem", "key.pem")
if cert_result:
    # 提交证书配置
    submit_result = api.submit_cert_config(cert_result)
    
# 删除证书
delete_result = api.delete_cert(cert_id=123)
```

### 站点配置

```python
# 获取站点列表
site_list = api.get_site_list()
if site_list:
    parsed_sites = api.parse_site_list(site_list)
    print("站点列表:", parsed_sites)

# 更新站点配置
update_result = api.update_site_config(
    ip="192.168.1.1",
    port=443,
    site_id=123,
    uid=456,
    description="我的网站"
)
```

## 安全说明

- 默认情况下，API 客户端禁用了 SSL 验证，这仅适用于开发环境。在生产环境中，建议正确配置 SSL 证书。
- 请妥善保管凭证信息，切勿将其提交到版本控制系统中。

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。

## 作者信息

- 作者：obaby
- 博客：[https://h4ck.org.cn](https://h4ck.org.cn)
- 博客：[https://oba.by](https://oba.by)

## 版本信息

当前版本：1.0.0 