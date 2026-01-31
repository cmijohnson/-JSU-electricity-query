#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江苏大学宿舍电费查询系统 - 命令行版

使用方法：
python electricity_cli.py

功能：
- 获取VPN cookie（自动/手动）
- 查询宿舍电费
- 统计用电量
- 显示用电数据
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import os
import pickle
from datetime import datetime, timedelta
import sys

class ElectricityQuery:
    def __init__(self, vpn_cookie=None):
        self.session = requests.Session()
        if vpn_cookie:
            self.session.cookies.update(json.loads(vpn_cookie))
        
        self.headers = {
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive'
        }
        self.session.headers.update(self.headers)
    
    def get_vpn_cookie(self):
        """
        获取VPN登录cookie
        检查是否存在Chrome浏览器，若有则自动获取cookie，否则指导用户手动获取
        若selenium库未安装，尝试自动安装
        """
        login_url = "https://webvpn.ujs.edu.cn/login"
        test_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        
        print("\n🔐 正在获取VPN登录cookie...")
        
        # 检查并尝试安装selenium库
        selenium_available = False
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            selenium_available = True
        except ImportError:
            print("\n⚠️ Selenium库未安装，正在尝试自动安装...")
            
            # 尝试自动安装selenium
            try:
                import subprocess
                print("正在安装Selenium库...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
                print("✅ Selenium库安装成功！")
                # 重新导入
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                selenium_available = True
            except Exception as e:
                print(f"\n❌ 自动安装Selenium库失败：{str(e)}")
                print("请手动安装Selenium库：pip install selenium")
        
        # 检查是否存在Chrome浏览器
        chrome_available = False
        if selenium_available:
            try:
                # 检查Chrome是否安装
                try:
                    # 尝试创建Chrome浏览器实例
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--disable-gpu")
                    chrome_options.add_argument("--ignore-certificate-errors")
                    
                    # 尝试启动Chrome
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.quit()
                    chrome_available = True
                except Exception as e:
                    print(f"\n⚠️ Chrome浏览器检测失败：{str(e)}")
                    
                    # 检查是否是ChromeDriver缺失的错误
                    if "Unable to obtain driver for chrome" in str(e) or "chromedriver" in str(e).lower():
                        print("⚠️ ChromeDriver缺失，正在尝试自动安装...")
                        
                        # 尝试自动安装ChromeDriver
                        try:
                            import subprocess
                            import os
                            
                            # 安装webdriver-manager
                            print("正在安装webdriver-manager...")
                            subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])
                            
                            # 测试webdriver-manager
                            from webdriver_manager.chrome import ChromeDriverManager
                            from selenium.webdriver.chrome.service import Service
                            
                            print("正在下载ChromeDriver...")
                            service = Service(ChromeDriverManager().install())
                            
                            # 再次尝试启动Chrome
                            driver = webdriver.Chrome(service=service, options=chrome_options)
                            driver.quit()
                            chrome_available = True
                            print("✅ ChromeDriver安装成功，Chrome浏览器检测成功")
                        except Exception as e3:
                            print(f"⚠️ ChromeDriver安装失败：{str(e3)}")
                    
                    # 检查系统路径中的Chrome可执行文件
                    if not chrome_available:
                        try:
                            import os
                            import platform
                            
                            system = platform.system()
                            chrome_paths = []
                            
                            if system == "Windows":
                                # Windows系统可能的Chrome路径
                                chrome_paths = [
                                    os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"), r"Google\Chrome\Application\chrome.exe"),
                                    os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), r"Google\Chrome\Application\chrome.exe"),
                                    os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Default\AppData\Local"), r"Google\Chrome\Application\chrome.exe")
                                ]
                            elif system == "Darwin":
                                # macOS系统可能的Chrome路径
                                chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
                            elif system == "Linux":
                                # Linux系统可能的Chrome路径
                                chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]
                            
                            # 检查路径是否存在
                            for path in chrome_paths:
                                if os.path.exists(path):
                                    print(f"✅ 找到Chrome可执行文件：{path}")
                                    chrome_available = True
                                    break
                            
                            if chrome_available:
                                print("✅ Chrome浏览器检测成功（通过路径检查）")
                            else:
                                print("❌ 未找到Chrome可执行文件")
                        except Exception as e2:
                            print(f"⚠️ 路径检查失败：{str(e2)}")
            except Exception as e:
                print(f"\n⚠️ Selenium使用失败：{str(e)}")
        
        # 命令行模式获取cookie
        return self._get_vpn_cookie_cli(login_url, test_url, chrome_available)
    
    def _get_vpn_cookie_cli(self, login_url, test_url, chrome_available):
        """
        命令行模式获取VPN cookie
        """
        # 如果Chrome可用，询问用户是否使用自动获取
        if chrome_available:
            print("\n检测到Chrome浏览器可用，您可以选择：")
            print("1. 自动获取cookie（推荐）")
            print("2. 手动获取cookie")
            
            choice = input("请输入您的选择（1/2）：").strip()
            
            if choice == "1":
                print("\n正在使用Chrome自动获取cookie...")
                print("系统将打开Chrome浏览器访问VPN登录页面")
                print("请使用企业微信扫码登录VPN")
                print("登录成功后，系统将自动获取cookie")
                
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    from selenium.webdriver.common.by import By
                    
                    # 尝试使用webdriver-manager
                    try:
                        from webdriver_manager.chrome import ChromeDriverManager
                        from selenium.webdriver.chrome.service import Service
                        
                        # 创建Chrome浏览器实例（使用webdriver-manager）
                        chrome_options = Options()
                        chrome_options.add_argument("--start-maximized")
                        chrome_options.add_argument("--disable-notifications")
                        
                        service = Service(ChromeDriverManager().install())
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                    except ImportError:
                        # 如果webdriver-manager不可用，使用默认方式
                        chrome_options = Options()
                        chrome_options.add_argument("--start-maximized")
                        chrome_options.add_argument("--disable-notifications")
                        
                        driver = webdriver.Chrome(options=chrome_options)
                    
                    # 访问VPN登录页面
                    driver.get(login_url)
                    
                    # 等待用户扫码登录，最多等待120秒
                    print("\n请在120秒内完成扫码登录...")
                    
                    # 等待页面跳转或特定元素出现
                    WebDriverWait(driver, 120).until(
                        lambda driver: "webvpn.ujs.edu.cn" in driver.current_url and "login" not in driver.current_url
                    )
                    
                    # 登录成功后，访问测试页面确保cookie有效
                    driver.get(test_url)
                    
                    # 获取cookie
                    cookies = driver.get_cookies()
                    driver.quit()
                    
                    # 查找wengine_vpn_ticket
                    vpn_cookie = None
                    for cookie in cookies:
                        if cookie['name'] == 'wengine_vpn_ticketwebvpn_ujs_edu_cn':
                            vpn_cookie = cookie['value']
                            break
                    
                    if vpn_cookie:
                        print("\n✅ 成功自动获取VPN cookie！")
                        print(f"获取到的cookie值：{vpn_cookie[:20]}...")
                        cookie_data = {
                            'show_vpn': '1',
                            'show_fast': '0',
                            'heartbeat': '1',
                            'show_faq': '0',
                            'wengine_vpn_ticketwebvpn_ujs_edu_cn': vpn_cookie
                        }
                        return json.dumps(cookie_data)
                    else:
                        print("\n❌ 未找到有效的VPN cookie，请重试")
                        # 回退到手动模式
                except Exception as e:
                    print(f"\n⚠️ 自动获取cookie失败：{str(e)}")
                    print("\n将回退到手动获取模式...")
        
        # 手动获取cookie模式
        print("\n请按照以下详细步骤操作：")
        print("\n步骤1: 登录VPN")
        print("   - 系统将打开默认浏览器访问VPN登录页面")
        print("   - 使用企业微信扫码登录VPN")
        print("   - 确保登录成功并保持登录状态")
        
        print("\n步骤2: 获取Cookie")
        print("   - 在登录成功的页面，按F12打开浏览器开发者工具")
        print("   - 切换到'控制台'(Console)选项卡")
        print("   - 在控制台中输入以下命令并按回车：")
        print("     document.cookie")
        print("   - 复制输出的完整cookie字符串")
        
        print("\n步骤3: 粘贴Cookie")
        print("   - 将复制的cookie字符串粘贴到下方输入框中")
        print("   - 按Enter键确认")
        
        print("\nCookie示例：")
        print("   show_vpn=1; show_fast=0; heartbeat=1; show_faq=0; wengine_vpn_ticketwebvpn_ujs_edu_cn=xxxxxxxxxxxx")
        print("   ")
        print("注意：")
        print("   - 请复制完整的cookie字符串")
        print("   - 确保包含wengine_vpn_ticketwebvpn_ujs_edu_cn部分")
        print("   - 不要包含任何额外的空格或换行符")
        
        # 打开系统浏览器
        import webbrowser
        webbrowser.open(login_url)
        
        # 等待用户输入cookie
        print("\n请输入从浏览器复制的cookie字符串（按Enter确认）：")
        cookie_input = input().strip()
        
        if cookie_input:
            # 从输入的cookie中提取wengine_vpn_ticket
            import re
            match = re.search(r'wengine_vpn_ticketwebvpn_ujs_edu_cn=([^;]+)', cookie_input)
            if match:
                vpn_cookie = match.group(1)
                print("\n✅ 成功获取VPN cookie！")
                print(f"获取到的cookie值：{vpn_cookie[:20]}...")
                cookie_data = {
                    'show_vpn': '1',
                    'show_fast': '0',
                    'heartbeat': '1',
                    'show_faq': '0',
                    'wengine_vpn_ticketwebvpn_ujs_edu_cn': vpn_cookie
                }
                return json.dumps(cookie_data)
            else:
                print("\n❌ 未找到有效的VPN cookie，请重试")
                print("请确保复制了完整的cookie字符串，包含wengine_vpn_ticketwebvpn_ujs_edu_cn部分")
                return None
        else:
            print("\n❌ 未输入cookie，请重试")
            return None
    
    def get_electricity_page(self):
        electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        print(f"正在访问电费查询系统：{electricity_url}")
        
        try:
            response = self.session.get(electricity_url, verify=False)
            print(f"响应状态码：{response.status_code}")
            return response
        except Exception as e:
            print(f"访问失败：{str(e)}")
            return None
    
    def select_campus(self, response, campus_name):
        print(f"\n正在选择校区：{campus_name}")
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
            eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
            
            data = {
                '__EVENTTARGET': 'ddlXiaoQu',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                'ddlXiaoQu': campus_name
            }
            
            electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
            response = self.session.post(electricity_url, data=data, verify=False)
            print(f"选择校区响应状态码：{response.status_code}")
            return response
        except Exception as e:
            print(f"选择校区失败：{str(e)}")
            return None
    
    def select_community(self, response, community_name):
        print(f"\n正在选择社区：{community_name}")
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
            eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
            
            if not viewstate_input or not eventvalidation_input:
                print("未找到表单参数，无法选择社区")
                return None
            
            viewstate = viewstate_input['value']
            eventvalidation = eventvalidation_input['value']
            
            community_select = soup.find('select', {'name': 'ddlQuYu'})
            if community_select:
                community_value = None
                for option in community_select.find_all('option'):
                    if option.text.strip() == community_name:
                        community_value = option['value']
                        print(f"找到匹配的社区值：{community_value}")
                        break
                if not community_value:
                    print(f"未找到匹配的社区选项：{community_name}")
                    return None
            else:
                print("未找到社区选择下拉框")
                return None
            
            data = {
                '__EVENTTARGET': 'ddlQuYu',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                'ddlXiaoQu': '校本部',
                'ddlQuYu': community_value
            }
            
            electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
            response = self.session.post(electricity_url, data=data, verify=False)
            print(f"选择社区响应状态码：{response.status_code}")
            return response
        except Exception as e:
            print(f"选择社区失败：{str(e)}")
            return None
    
    def select_building(self, response, building_number):
        print(f"\n正在选择楼栋：{building_number}")
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
            eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
            
            if not viewstate_input or not eventvalidation_input:
                print("未找到表单参数，无法选择楼栋")
                return None
            
            viewstate = viewstate_input['value']
            eventvalidation = eventvalidation_input['value']
            
            building_select = soup.find('select', {'name': 'ddlLouDong'})
            if building_select:
                building_value = None
                for option in building_select.find_all('option'):
                    if option.text.strip() == building_number:
                        building_value = option['value']
                        print(f"找到匹配的楼栋值：{building_value}")
                        break
                if not building_value:
                    print(f"未找到匹配的楼栋选项：{building_number}")
                    return None
            else:
                print("未找到楼栋选择下拉框")
                return None
            
            data = {
                '__EVENTTARGET': 'ddlLouDong',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                'ddlXiaoQu': '校本部',
                'ddlQuYu': 'D区                                               ',
                'ddlLouDong': building_value
            }
            
            electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
            response = self.session.post(electricity_url, data=data, verify=False)
            print(f"选择楼栋响应状态码：{response.status_code}")
            return response
        except Exception as e:
            print(f"选择楼栋失败：{str(e)}")
            return None
    
    def query_electricity(self, response, room_number, password, start_date, end_date):
        print(f"\n正在查询房间 {room_number} 的电费")
        
        try:
            if response is None:
                print("响应对象为None，无法查询电费")
                return None
            
            if hasattr(response, 'status_code') and response.status_code != 200:
                print(f"响应状态码异常：{response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
            eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
            
            if not viewstate_input or not eventvalidation_input:
                print("未找到表单参数，无法查询电费")
                return None
            
            viewstate = viewstate_input['value']
            eventvalidation = eventvalidation_input['value']
            
            room_select = soup.find('select', {'name': 'ddlFangJian'})
            if room_select:
                room_value = None
                for option in room_select.find_all('option'):
                    if option.text.strip() == room_number:
                        room_value = option['value']
                        print(f"找到匹配的房间值：{room_value}")
                        break
                if not room_value:
                    print(f"未找到房间 {room_number}")
                    return None
            else:
                print("未找到房间选择下拉框")
                return None
            
            data = {
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                'ddlXiaoQu': '校本部',
                'ddlQuYu': 'D区                                               ',
                'ddlLouDong': '1',
                'ddlFangJian': room_value,
                'txtStuPwd': password,
                'btnEnter.x': '1',
                'btnEnter.y': '1'
            }
            
            electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
            response = self.session.post(electricity_url, data=data, verify=False)
            print(f"查询电费响应状态码：{response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查是否是初次使用，需要系统设置
            if "系统设置" in response.text or "初次登录" in response.text:
                print("\n⚠️ 检测到初次使用，需要设置房间密码和信息")
                
                # 获取表单参数
                viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
                eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
                
                if not viewstate_input or not eventvalidation_input:
                    print("未找到表单参数，无法进行系统设置")
                    return None
                
                viewstate = viewstate_input['value']
                eventvalidation = eventvalidation_input['value']
                
                # 命令行模式下，提示用户手动设置
                print("\n请在浏览器中完成初次使用设置：")
                print("1. 系统将打开设置页面")
                print("2. 请设置房间密码")
                print("3. 填写宿舍代表和手机号码")
                print("4. 点击确定按钮完成设置")
                
                # 打开系统浏览器
                import webbrowser
                setup_url = f"https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/HouseInfo.aspx?ID={room_value}"
                webbrowser.open(setup_url)
                
                input("\n请完成设置后按Enter键继续...")
                
                # 重新查询
                return self.query_electricity(response, room_number, password, start_date, end_date)
            
            frameset = soup.find('frameset')
            if frameset:
                print("\n发现框架页面，正在获取stuMainFrame的内容...")
                
                main_frame = frameset.find('frame', {'name': 'stuMainFrame'})
                if main_frame:
                    main_frame_src = main_frame.get('src')
                    print(f"stuMainFrame的src：{main_frame_src}")
                    
                    if not main_frame_src.startswith('http'):
                        main_frame_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/" + main_frame_src
                    else:
                        main_frame_url = main_frame_src
                    
                    main_frame_response = self.session.get(main_frame_url, verify=False)
                    print(f"获取stuMainFrame响应状态码：{main_frame_response.status_code}")
                    
                    main_frame_soup = BeautifulSoup(main_frame_response.text, 'html.parser')
                    
                    electricity_info = []
                    for table in main_frame_soup.find_all('table'):
                        for row in table.find_all('tr'):
                            cells = row.find_all('td')
                            if cells:
                                info = [cell.text.strip() for cell in cells]
                                electricity_info.append(info)
                    
                    if electricity_info:
                        print("\n电费查询结果：")
                        for info in electricity_info:
                            print(' | '.join(info))
                    else:
                        print("\n未找到电费信息，请手动检查stuMainFrame内容文件。")
                    
                    print("\n正在检查是否存在'用电信息'标签...")
                    
                    print("\n正在获取stuTopFrame的内容...")
                    top_frame_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/stuTop.htm"
                    top_frame_response = self.session.get(top_frame_url, verify=False)
                    print(f"获取stuTopFrame响应状态码：{top_frame_response.status_code}")
                    
                    top_frame_soup = BeautifulSoup(top_frame_response.text, 'html.parser')
                    electricity_info_link = None
                    
                    for link in top_frame_soup.find_all('a', href=True):
                        if link['href'] == 'HouseElec.aspx':
                            electricity_info_link = link['href']
                            print(f"找到'用电信息'链接：{electricity_info_link}")
                            break
                    
                    if not electricity_info_link:
                        nav_table = top_frame_soup.find('table')
                        if nav_table:
                            nav_links = nav_table.find_all('a', href=True)
                            if len(nav_links) >= 2:
                                electricity_info_link = nav_links[1]['href']
                                print(f"通过索引找到'用电信息'链接：{electricity_info_link}")
                    
                    if electricity_info_link:
                        print("\n正在模拟点击'用电信息'标签...")
                        
                        if not electricity_info_link.startswith('http'):
                            electricity_info_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/" + electricity_info_link
                        else:
                            electricity_info_url = electricity_info_link
                        
                        electricity_info_response = self.session.get(electricity_info_url, verify=False)
                        print(f"获取用电信息页面响应状态码：{electricity_info_response.status_code}")
                        
                        electricity_info_soup = BeautifulSoup(electricity_info_response.text, 'html.parser')
                        
                        all_electricity_records = []
                        headers = []
                        
                        start_year, start_month = map(int, start_date.split('-'))
                        end_year, end_month = map(int, end_date.split('-'))
                        
                        print(f"\n开始收集{start_date}到{end_date}的电费记录...")
                        
                        # 计算总月数
                        total_months = (end_year - start_year) * 12 + (end_month - start_month) + 1
                        current_month_count = 0
                        
                        current_year = start_year
                        current_month = start_month
                        
                        while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
                            current_date = f"{current_year}-{current_month:02d}"
                            print(f"\n正在处理月份：{current_date}")
                            
                            page_soup = BeautifulSoup(electricity_info_response.text, 'html.parser')
                            viewstate = page_soup.find('input', {'name': '__VIEWSTATE'})['value']
                            eventvalidation = page_soup.find('input', {'name': '__EVENTVALIDATION'})['value']
                            
                            data = {
                                '__VIEWSTATE': viewstate,
                                '__EVENTVALIDATION': eventvalidation,
                                'ddlYear': str(current_year),
                                'ddlMonth': f"{current_month:02d}",
                                'btnSelect': '查 看'
                            }
                            
                            month_response = self.session.post("https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/HouseElec.aspx", 
                                                       data=data, verify=False)
                            
                            current_page_response = month_response
                            has_next_page = True
                            
                            while has_next_page:
                                page_soup = BeautifulSoup(current_page_response.text, 'html.parser')
                                
                                table = page_soup.find('table', {'id': 'gvElecInfo'})
                                if table:
                                    if not headers:
                                        headers = [th.text.strip() for th in table.find('tr').find_all('th')]
                                    
                                    rows = table.find_all('tr')[1:]
                                    for row in rows:
                                        if row.find('a') and '下一页' in row.text:
                                            continue
                                        
                                        cells = row.find_all('td')
                                        if cells and len(cells) >= 5:
                                            record = [cell.text.strip() for cell in cells]
                                            if record[3] not in ['', ' ']:
                                                all_electricity_records.append(record)
                                
                                has_next_page = False
                                next_page_link = None
                                
                                for link in page_soup.find_all('a'):
                                    if '下一页' in link.text:
                                        has_next_page = True
                                        break
                                
                                if has_next_page:
                                    print("正在获取下一页...")
                                    viewstate = page_soup.find('input', {'name': '__VIEWSTATE'})['value']
                                    eventvalidation = page_soup.find('input', {'name': '__EVENTVALIDATION'})['value']
                                    
                                    pagination_data = {
                                        '__VIEWSTATE': viewstate,
                                        '__EVENTVALIDATION': eventvalidation,
                                        'ddlYear': str(current_year),
                                        'ddlMonth': f"{current_month:02d}",
                                        '__EVENTTARGET': 'gvElecInfo',
                                        '__EVENTARGUMENT': 'Page$Next'
                                    }
                                    
                                    current_page_response = self.session.post("https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/HouseElec.aspx", 
                                                               data=pagination_data, verify=False)
                            
                            current_month += 1
                            if current_month > 12:
                                current_month = 1
                                current_year += 1
                        
                        total_electricity = 0
                        for record in all_electricity_records:
                            if len(record) > 3 and record[3].strip():
                                try:
                                    total_electricity += float(record[3])
                                except ValueError:
                                    pass
                        
                        return {
                            'records': all_electricity_records,
                            'headers': headers,
                            'total_electricity': total_electricity
                        }
                else:
                    print("未找到stuMainFrame")
            else:
                electricity_info = []
                for table in soup.find_all('table'):
                    for row in table.find_all('tr'):
                        cells = row.find_all('td')
                        if cells:
                            info = [cell.text.strip() for cell in cells]
                            electricity_info.append(info)
                
                if electricity_info:
                    print("\n电费查询结果：")
                    for info in electricity_info:
                        print(' | '.join(info))
                else:
                    print("\n未找到电费信息，请手动检查查询结果文件。")
            
            return None
            
        except Exception as e:
            print(f"查询电费失败：{str(e)}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """
    命令行主函数
    """
    print("=" * 60)
    print("江苏大学宿舍电费查询系统 - 命令行版")
    print("=" * 60)
    
    # 获取VPN cookie
    print("\n1. 获取VPN Cookie")
    print("-" * 40)
    eq = ElectricityQuery()
    vpn_cookie = eq.get_vpn_cookie()
    
    if not vpn_cookie:
        print("\n❌ 获取VPN cookie失败，程序退出")
        return
    
    print("\n✅ VPN cookie获取成功！")
    
    # 输入宿舍信息
    print("\n2. 输入宿舍信息")
    print("-" * 40)
    campus = input("请输入校区（默认：校本部）：").strip() or "校本部"
    community = input("请输入社区（例如：A区）：").strip()
    building = input("请输入楼栋（例如：1）：").strip()
    room = input("请输入房间号（例如：101）：").strip()
    password = input("请输入查询密码（默认：111）：").strip() or "111"
    
    if not all([community, building, room]):
        print("\n❌ 宿舍信息不完整，程序退出")
        return
    
    # 输入查询日期
    print("\n3. 输入查询日期")
    print("-" * 40)
    start_date = input("请输入开始日期（格式：YYYY-MM，例如：2026-01）：").strip()
    end_date = input("请输入结束日期（格式：YYYY-MM，例如：2026-01）：").strip()
    
    if not all([start_date, end_date]):
        print("\n❌ 日期输入不完整，程序退出")
        return
    
    # 初始化查询对象
    eq = ElectricityQuery(vpn_cookie)
    
    # 开始查询
    print("\n4. 开始查询电费")
    print("-" * 40)
    
    # 访问电费查询系统
    response = eq.get_electricity_page()
    if not response:
        print("\n❌ 无法访问电费查询系统，程序退出")
        return
    
    # 选择校区
    response = eq.select_campus(response, campus)
    if not response:
        print("\n❌ 无法选择校区，程序退出")
        return
    
    # 选择社区
    response = eq.select_community(response, community)
    if not response:
        print("\n❌ 无法选择社区，程序退出")
        return
    
    # 选择楼栋
    response = eq.select_building(response, building)
    if not response:
        print("\n❌ 无法选择楼栋，程序退出")
        return
    
    # 查询电费
    result = eq.query_electricity(response, room, password, start_date, end_date)
    
    if result:
        print("\n5. 查询结果")
        print("-" * 40)
        print(f"查询结果：{start_date} 至 {end_date}")
        print(f"总用电量：{result['total_electricity']:.2f} 度")
        print(f"记录条数：{len(result['records'])} 条")
        
        if result['headers']:
            print("\n表头：")
            print('\t'.join(result['headers']))
            print("-" * 80)
        
        print("\n用电详情：")
        for i, record in enumerate(result['records'][:10]):  # 只显示前10条
            print(f"{i+1}.\t" + '\t'.join(record))
        
        if len(result['records']) > 10:
            print(f"... 共 {len(result['records'])} 条记录，仅显示前10条")
        
        print("\n✅ 查询完成！")
    else:
        print("\n❌ 查询失败，请检查网络连接和输入信息")
    
    print("\n" + "=" * 60)
    print("程序执行完毕")
    print("=" * 60)

if __name__ == "__main__":
    main()
