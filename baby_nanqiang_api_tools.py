#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南墙API工具类
用于与南墙API进行交互，包括证书管理、站点配置等功能

作者: obaby
博客：https://h4ck.org.cn
    https://oba.by
创建时间: 2024-04-16
最后修改时间: 2024-04-16
版本: 1.0.0

功能:
- 证书管理（获取、检查、提交、删除）
- 站点配置（获取、更新）
- 用户认证（登录）

依赖:
- requests
- jwt
- datetime
- json
- os
- urllib3
"""

import requests
import json
import jwt
from datetime import datetime
import os
import urllib3

# 禁用 SSL 验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NanQiangAPI:
    def __init__(self, base_url="https://lang.bi:443"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False  # 忽略SSL证书验证
        self.token = None
        self._setup_headers()

    def _setup_headers(self):
        """设置请求头"""
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': self.base_url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{self.base_url}/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }

    def _update_headers_with_token(self):
        """更新请求头，添加token"""
        if self.token:
            self.headers['Authorization'] = self.token  # 直接使用token，不添加'Bearer '前缀

    def delete_cert(self, cert_id):
        """
        删除指定ID的证书
        :param cert_id: 证书ID
        :return: 删除结果
        """
        if not self.is_logged_in():
            print("请先登录")
            return None

        url = f"{self.base_url}/api/v1/certs/{cert_id}"

        try:
            response = self.session.delete(
                url,
                headers=self.headers
            )
            
            response_data = response.json()
            
            if 'err' in response_data:
                print(f"删除证书失败: {response_data['err']}")
                return None
            
            # 检查删除是否成功
            if response_data.get('result') == 'success' and response_data.get('RowsAffected') > 0:
                print(f"证书 {cert_id} 删除成功")
                return True
            else:
                print(f"证书 {cert_id} 删除失败: 未找到证书或删除操作未生效")
                return False
            
        except requests.exceptions.RequestException as e:
            print(f"删除证书请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

    def parse_cert_list(self, cert_list):
        """
        解析证书列表数据
        :param cert_list: 证书列表数据
        :return: 解析后的证书信息列表
        """
        if not cert_list:
            return None

        parsed_certs = []
        for cert in cert_list:
            try:
                # 解析SNI字段（JSON字符串）
                sni_list = json.loads(cert.get('sni', '[]'))
                
                parsed_cert = {
                    'id': cert.get('id'),
                    'sni': sni_list,
                    'expire_time': cert.get('expire_time'),
                    'update_time': cert.get('update_time')
                }
                parsed_certs.append(parsed_cert)
            except json.JSONDecodeError as e:
                print(f"解析SNI字段失败: {str(e)}")
                continue
            except Exception as e:
                print(f"解析证书数据失败: {str(e)}")
                continue

        return parsed_certs

    def get_cert_list(self):
        """
        获取证书列表
        :return: 证书列表
        """
        if not self.is_logged_in():
            print("请先登录")
            return None

        url = f"{self.base_url}/api/v1/certs/"

        try:
            response = self.session.get(
                url,
                headers=self.headers
            )
            
            response_data = response.json()
            
            if 'err' in response_data:
                print(f"获取证书列表失败: {response_data['err']}")
                return None
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"获取证书列表请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

    def login(self, username, password, otp=""):
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        :param otp: 双因素认证码（可选）
        :return: 登录响应
        """
        url = f"{self.base_url}/api/v1/users/login"
        data = {
            "usr": username,
            "pwd": password,
            "otp": otp
        }

        try:
            response = self.session.post(
                url,
                headers=self.headers,
                json=data
            )
            
            # 获取响应数据
            response_data = response.json()
            
            # 检查是否有错误信息
            if 'err' in response_data:
                print(f"登录失败: {response_data['err']}")
                return None
            
            # 保存token
            if 'token' in response_data:
                self.token = response_data['token']
                self._update_headers_with_token()
                
                # # 解析token信息
                # try:
                #     # 使用 jwt.decode 替代 jwt.decode_complete
                #     token_data = jwt.decode(self.token, options={"verify_signature": False})
                #     exp_timestamp = token_data.get('exp')
                #     if exp_timestamp:
                #         exp_date = datetime.fromtimestamp(exp_timestamp)
                #         print(f"Token 有效期至: {exp_date}")
                # except Exception as e:
                #     print(f"无法解析token信息: {str(e)}")
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"登录请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

    def check_cert(self, cert_content, key_content, mode=0):
        """
        检查证书
        :param cert_content: 证书内容
        :param key_content: 私钥内容
        :param mode: 模式，默认为0
        :return: 检查结果
        """
        if not self.is_logged_in():
            print("请先登录")
            return None

        url = f"{self.base_url}/api/v1/certs/check"
        
        # 准备multipart/form-data数据
        files = {
            'mode': (None, str(mode)),
            'cert': (None, cert_content),
            'key': (None, key_content)
        }

        try:
            # 临时移除content-type，让requests自动设置
            headers = self.headers.copy()
            headers.pop('content-type', None)
            
            response = self.session.post(
                url,
                headers=headers,
                files=files
            )
            
            response_data = response.json()
            
            if 'err' in response_data:
                print(f"证书检查失败: {response_data['err']}")
                return None
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"证书检查请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

    def check_cert_from_files(self, cert_file_path, key_file_path, mode=0):
        """
        从文件检查证书
        :param cert_file_path: 证书文件路径
        :param key_file_path: 私钥文件路径
        :param mode: 模式，默认为0
        :return: 检查结果
        """
        try:
            with open(cert_file_path, 'r') as f:
                cert_content = f.read()
            with open(key_file_path, 'r') as f:
                key_content = f.read()
                
            return self.check_cert(cert_content, key_content, mode)
            
        except FileNotFoundError as e:
            print(f"文件不存在: {str(e)}")
            return None
        except Exception as e:
            print(f"读取文件失败: {str(e)}")
            return None

    def submit_cert_config(self, check_result):
        """
        提交证书配置
        :param check_result: 证书检查的结果数据
        :return: 提交结果
        """
        if not self.is_logged_in():
            print("请先登录")
            return None

        if not check_result:
            print("无效的证书检查结果")
            return None

        url = f"{self.base_url}/api/v1/certs/config"
        
        # 准备提交数据
        data = {
            "id": check_result.get("id", 0),
            "sni": check_result.get("sni", "[]"),
            "cert": check_result.get("cert", ""),
            "key": check_result.get("key", ""),
            "expire_time": check_result.get("expire_time", ""),
            "update_time": check_result.get("update_time", "")
        }

        try:
            response = self.session.post(
                url,
                headers=self.headers,
                json=data
            )
            
            response_data = response.json()
            
            if 'err' in response_data:
                print(f"证书配置提交失败: {response_data['err']}")
                return None
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"证书配置提交请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

    def is_logged_in(self):
        """
        检查是否已登录
        :return: bool
        """
        return self.token is not None

    def parse_site_list(self, site_list):
        """
        解析站点列表数据
        :param site_list: 站点列表数据
        :return: 解析后的站点信息列表
        """
        if not site_list:
            return None

        parsed_sites = []
        for site in site_list:
            try:
                parsed_site = {
                    'id': site.get('id'),
                    'uid': site.get('uid'),
                    'host': site.get('host'),
                    'description': site.get('description'),
                    'mode': site.get('mode'),
                    'type': site.get('type'),
                    'scheme': site.get('scheme'),
                    'servers': site.get('servers', []),
                    'update_time': site.get('update_time')
                }
                parsed_sites.append(parsed_site)
            except Exception as e:
                print(f"解析站点数据失败: {str(e)}")
                continue

        return parsed_sites

    def get_site_list(self):
        """
        获取站点列表
        :return: 站点列表
        """
        if not self.is_logged_in():
            print("请先登录")
            return None

        url = f"{self.base_url}/api/v1/sites/"

        try:
            response = self.session.get(
                url,
                headers=self.headers
            )
            
            response_data = response.json()
            
            if 'err' in response_data:
                print(f"获取站点列表失败: {response_data['err']}")
                return None
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"获取站点列表请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

    def update_site_config(self, ip, port, site_id, uid, description):
        """
        更新网站配置
        :param ip: 服务器IP地址
        :param port: 服务器端口
        :param site_id: 网站ID
        :param uid: 用户ID
        :param description: 网站描述
        :return: 更新结果
        """
        if not self.is_logged_in():
            print("请先登录")
            return None

        url = f"{self.base_url}/api/v1/sites/config"
        
        # 获取当前时间并格式化
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 准备提交数据
        data = {
            "id": site_id,
            "uid": uid,
            "host": "jiuwei.hu",
            "description": description,
            "mode": "1",
            "type": "roundrobin",
            "scheme": "https",
            "rules": {
                "10": 0, "11": 0, "12": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0,
                "21": 0, "22": 0, "24": 0, "25": 0, "27": 0, "28": 0, "29": 0, "41": 0, "43": 0, "44": 0,
                "45": 0, "46": 0, "47": 0, "48": 0, "49": 0, "50": 0, "51": 0, "52": 0, "53": 0, "54": 0,
                "55": 0, "56": 0, "58": 2, "59": 2, "60": 2, "61": 2, "62": 2, "64": 0, "65": 0, "66": 0,
                "68": 0, "71": 0, "72": 0, "73": 0
            },
            "ip_whitelist": [""],
            "url_whitelist": [""],
            "deny_page": "",
            "is_websocket": True,
            "is_ml": False,
            "skip_cache": False,
            "ip_source": "0",
            "ip_order": 2,
            "ip_header": "X-Real-IP",
            "servers": [{"ip": ip, "port": port, "weight": 1}],
            "update_time": current_time
        }

        try:
            response = self.session.put(
                url,
                headers=self.headers,
                json=data
            )
            
            response_data = response.json()
            
            if 'err' in response_data:
                print(f"更新网站配置失败: {response_data['err']}")
                return None
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            print(f"更新网站配置请求失败: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析响应数据失败: {str(e)}")
            return None

def main():
    # 使用示例
    api = NanQiangAPI()
    
    # 登录信息
    username = "obaby"
    password = "12345678"
    
    # 执行登录
    result = api.login(username, password)
    
    if result:
        print("登录成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Token: {api.token}")
        
        # 获取证书列表
        cert_list = api.get_cert_list()
        if cert_list:
            # 解析证书列表
            parsed_certs = api.parse_cert_list(cert_list)
            if parsed_certs:
                print("解析后的证书列表:")
                print(json.dumps(parsed_certs, indent=2, ensure_ascii=False))
                
                # # 删除证书示例
                # cert_id = 4  # 要删除的证书ID
                # delete_result = api.delete_cert(cert_id)
                # if delete_result:
                #     print(f"证书 {cert_id} 删除成功")
                # else:
                #     print(f"证书 {cert_id} 删除失败")
        
        # 证书检查示例
        cert_file = "path/to/cert.pem"
        key_file = "path/to/key.pem"
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            return
            # 先检查证书
            cert_result = api.check_cert_from_files(cert_file, key_file)
            if cert_result:
                print("证书检查结果:")
                print(json.dumps(cert_result, indent=2, ensure_ascii=False))
                
                # 提交证书配置
                submit_result = api.submit_cert_config(cert_result)
                if submit_result:
                    print("证书配置提交成功:")
                    print(json.dumps(submit_result, indent=2, ensure_ascii=False))
                else:
                    print("证书配置提交失败")
    else:
        print("登录失败")

if __name__ == "__main__":
    main() 