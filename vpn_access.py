import requests
import os
from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_vpn_cookie():
    """
    自动获取VPN登录cookie
    使用Selenium控制浏览器，让用户扫码登录，然后直接从浏览器获取cookie值
    注意：webvpn会先给假cookie，只有用户正确扫码后才能获取到真cookie
    """
    print("\n🔐 正在获取VPN登录cookie...")
    print("请使用企业微信扫码登录VPN")
    
    # 创建会话
    session = requests.Session()
    
    try:
        login_url = "https://webvpn.ujs.edu.cn/login"
        test_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        
        # 配置Selenium
        print("\n正在启动浏览器...")
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        
        # 启动浏览器
        driver = webdriver.Chrome(options=options)
        
        try:
            # 访问VPN登录页面（只加载一次，避免二维码频繁刷新）
            driver.get(login_url)
            print("已打开VPN登录页面，请使用企业微信扫码登录")
            print("系统将持续检测登录状态...")
            print("请在30秒内完成扫码操作")
            
            # 等待用户扫码登录，最多等待120秒
            timeout = 120
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    # 获取浏览器中的cookie（先检查cookie，不刷新页面）
                    cookies = driver.get_cookies()
                    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                    vpn_cookie = cookie_dict.get('wengine_vpn_ticketwebvpn_ujs_edu_cn')
                    
                    # 检查1：通过cookie检测登录成功（优先检查，不刷新页面）
                    if vpn_cookie and len(vpn_cookie) > 20:
                        print("\n✅ VPN登录成功！(通过cookie检测)")
                        print(f"获取到cookie值：{vpn_cookie}")
                        cookie_data = {
                            'show_vpn': '1',
                            'show_fast': '0',
                            'heartbeat': '1',
                            'show_faq': '0',
                            'wengine_vpn_ticketwebvpn_ujs_edu_cn': vpn_cookie
                        }
                        with open('vpn_cookie.json', 'w', encoding='utf-8') as f:
                            json.dump(cookie_data, f, ensure_ascii=False, indent=2)
                        print("\n📁 cookie值已保存到 vpn_cookie.json 文件")
                        return cookie_data
                    
                    # 每5秒尝试一次访问内部页面（减少页面刷新频率）
                    if int((time.time() - start_time) % 5) == 0:
                        # 尝试访问内部页面，检查是否登录成功
                        driver.get(test_url)
                        
                        # 获取当前页面的URL和标题
                        current_url = driver.current_url
                        current_title = driver.title
                        
                        # 检查2：通过页面标题检测登录成功
                        if "电费查询" in current_title or "用电管理" in current_title or "登录成功" in current_title:
                            print("\n✅ VPN登录成功！(通过页面标题检测)")
                            if vpn_cookie:
                                print(f"获取到cookie值：{vpn_cookie}")
                                cookie_data = {
                                    'show_vpn': '1',
                                    'show_fast': '0',
                                    'heartbeat': '1',
                                    'show_faq': '0',
                                    'wengine_vpn_ticketwebvpn_ujs_edu_cn': vpn_cookie
                                }
                                with open('vpn_cookie.json', 'w', encoding='utf-8') as f:
                                    json.dump(cookie_data, f, ensure_ascii=False, indent=2)
                                print("\n📁 cookie值已保存到 vpn_cookie.json 文件")
                                return cookie_data
                        
                        # 检查3：通过URL检测登录成功（如果跳转到内部页面）
                        if "http/77726476706e69737468656265737421" in current_url:
                            print("\n✅ VPN登录成功！(通过URL检测)")
                            if vpn_cookie:
                                print(f"获取到cookie值：{vpn_cookie}")
                                cookie_data = {
                                    'show_vpn': '1',
                                    'show_fast': '0',
                                    'heartbeat': '1',
                                    'show_faq': '0',
                                    'wengine_vpn_ticketwebvpn_ujs_edu_cn': vpn_cookie
                                }
                                with open('vpn_cookie.json', 'w', encoding='utf-8') as f:
                                    json.dump(cookie_data, f, ensure_ascii=False, indent=2)
                                print("\n📁 cookie值已保存到 vpn_cookie.json 文件")
                                return cookie_data
                        
                        # 检查4：通过页面内容检测登录成功
                        try:
                            page_source = driver.page_source
                            if "电费查询" in page_source or "用电管理" in page_source or "欢迎使用" in page_source:
                                print("\n✅ VPN登录成功！(通过页面内容检测)")
                                if vpn_cookie:
                                    print(f"获取到cookie值：{vpn_cookie}")
                                    cookie_data = {
                                        'show_vpn': '1',
                                        'show_fast': '0',
                                        'heartbeat': '1',
                                        'show_faq': '0',
                                        'wengine_vpn_ticketwebvpn_ujs_edu_cn': vpn_cookie
                                    }
                                    with open('vpn_cookie.json', 'w', encoding='utf-8') as f:
                                        json.dump(cookie_data, f, ensure_ascii=False, indent=2)
                                    print("\n📁 cookie值已保存到 vpn_cookie.json 文件")
                                    return cookie_data
                        except Exception:
                            pass
                    else:
                        # 不刷新页面，仅检查cookie
                        pass
                    
                    # 显示倒计时
                    remaining_time = max(0, int(timeout - (time.time() - start_time)))
                    print(f"\r等待扫码登录... (剩余时间: {remaining_time}秒)", end="")
                    time.sleep(1)  # 缩短检查间隔，提高响应速度
                    
                except Exception as e:
                    # 忽略临时错误，继续等待
                    print(f"\r等待扫码登录... (错误: {str(e)[:20]}...)", end="")
                    time.sleep(1)
            
            print("\n❌ 登录超时，请重试")
            return None
            
        finally:
            # 关闭浏览器
            driver.quit()
            print("\n浏览器已关闭")
        
    except Exception as e:
        print(f"\n⚠️ 获取cookie时发生错误：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

def get_session():
    # 尝试从文件中加载cookie
    cookies = None
    if os.path.exists('vpn_cookie.json'):
        try:
            with open('vpn_cookie.json', 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            print("\n📁 从文件加载cookie成功")
        except Exception as e:
            print(f"\n⚠️ 加载cookie文件失败：{str(e)}")
            cookies = None
    
    # 如果没有cookie文件或加载失败，自动获取cookie
    if not cookies:
        cookies = get_vpn_cookie()
        if not cookies:
            print("\n❌ 无法获取cookie，使用默认cookie值")
            # 使用默认cookie值作为 fallback
            cookies = {
                'show_vpn': '1',
                'show_fast': '0',
                'heartbeat': '1',
                'show_faq': '0',
                'wengine_vpn_ticketwebvpn_ujs_edu_cn': '407b4646a249c8ed'  # 关键cookie值
            }
    
    # 从抓包文件中提取的请求头信息
    headers = {
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://webvpn.ujs.edu.cn/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Priority': 'u=0, i',
        'Connection': 'keep-alive'
    }
    
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(headers)
    
    return session

def get_electricity_page(session):
    # 访问电费查询系统页面
    electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
    print(f"正在访问电费查询系统：{electricity_url}")
    
    try:
        response = session.get(electricity_url, verify=False)
        print(f"响应状态码：{response.status_code}")
        
        # 保存响应内容到文件，便于分析
        output_file = "electricity_page.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"电费查询页面已保存到：{os.path.abspath(output_file)}")
        
        return response
        
    except Exception as e:
        print(f"访问失败：{str(e)}")
        return None

def select_campus(session, response, campus_name):
    # 选择校区
    print(f"\n正在选择校区：{campus_name}")
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取表单相关参数
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        
        # 构建表单数据
        data = {
            '__EVENTTARGET': 'ddlXiaoQu',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'ddlXiaoQu': campus_name
        }
        
        # 发送POST请求，选择校区
        electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        response = session.post(electricity_url, data=data, verify=False)
        print(f"选择校区响应状态码：{response.status_code}")
        
        # 保存选择校区后的页面内容到文件，便于分析
        output_file = "campus_selected.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"选择校区后的页面已保存到：{os.path.abspath(output_file)}")
        
        # 检查选择校区后的页面，获取可用的社区选项
        soup = BeautifulSoup(response.text, 'html.parser')
        community_select = soup.find('select', {'name': 'ddlQuYu'})
        if community_select:
            print("\n可用的社区选项：")
            for option in community_select.find_all('option'):
                print(f"- {option.text.strip()}")
        
        return response
        
    except Exception as e:
        print(f"选择校区失败：{str(e)}")
        return None

def select_community(session, response, community_name):
    # 选择社区
    print(f"\n正在选择社区：{community_name}")
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取表单相关参数
        viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
        eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
        
        if not viewstate_input or not eventvalidation_input:
            print("未找到表单参数，无法选择社区")
            return None
        
        viewstate = viewstate_input['value']
        eventvalidation = eventvalidation_input['value']
        
        # 查找社区选择下拉框，获取实际的社区选项值
        community_select = soup.find('select', {'name': 'ddlQuYu'})
        if community_select:
            print("\n实际的社区选项：")
            for option in community_select.find_all('option'):
                print(f"- 文本: '{option.text.strip()}', 值: '{option['value']}'")
                # 找到与目标社区名称匹配的选项
                if option.text.strip() == community_name:
                    community_value = option['value']
                    print(f"找到匹配的社区值：{community_value}")
                    break
            else:
                print(f"未找到匹配的社区选项：{community_name}")
                return None
        else:
            print("未找到社区选择下拉框")
            return None
        
        # 构建表单数据
        data = {
            '__EVENTTARGET': 'ddlQuYu',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'ddlXiaoQu': '校本部',
            'ddlQuYu': community_value
        }
        
        # 发送POST请求，选择社区
        electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        response = session.post(electricity_url, data=data, verify=False)
        print(f"选择社区响应状态码：{response.status_code}")
        
        # 保存选择社区后的页面内容到文件，便于分析
        output_file = "community_selected.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"选择社区后的页面已保存到：{os.path.abspath(output_file)}")
        
        # 检查选择社区后的页面是否显示错误
        soup = BeautifulSoup(response.text, 'html.parser')
        error_message = soup.find('span', {'style': 'color: #800080'})
        if error_message and '出错了' in error_message.text:
            print(f"选择社区失败，页面显示错误：{error_message.text.strip()}")
            return None
        
        return response
        
    except Exception as e:
        print(f"选择社区失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

def select_building(session, response, building_number):
    # 选择楼栋
    print(f"\n正在选择楼栋：{building_number}")
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取表单相关参数
        viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
        eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
        
        if not viewstate_input or not eventvalidation_input:
            print("未找到表单参数，无法选择楼栋")
            return None
        
        viewstate = viewstate_input['value']
        eventvalidation = eventvalidation_input['value']
        
        # 查找楼栋选择下拉框，获取实际的楼栋选项值
        building_select = soup.find('select', {'name': 'ddlLouDong'})
        if building_select:
            print("\n实际的楼栋选项：")
            for option in building_select.find_all('option'):
                print(f"- 文本: '{option.text.strip()}', 值: '{option['value']}'")
                # 找到与目标楼栋编号匹配的选项
                if option.text.strip() == building_number:
                    building_value = option['value']
                    print(f"找到匹配的楼栋值：{building_value}")
                    break
            else:
                print(f"未找到匹配的楼栋选项：{building_number}")
                return None
        else:
            print("未找到楼栋选择下拉框")
            return None
        
        # 构建表单数据
        data = {
            '__EVENTTARGET': 'ddlLouDong',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'ddlXiaoQu': '校本部',
            'ddlQuYu': 'A区                                               ',  # 使用完整的社区值
            'ddlLouDong': building_value
        }
        
        # 发送POST请求，选择楼栋
        electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        response = session.post(electricity_url, data=data, verify=False)
        print(f"选择楼栋响应状态码：{response.status_code}")
        
        # 保存选择楼栋后的页面内容到文件，便于分析
        output_file = "building_selected.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"选择楼栋后的页面已保存到：{os.path.abspath(output_file)}")
        
        # 检查选择楼栋后的页面是否显示错误
        soup = BeautifulSoup(response.text, 'html.parser')
        error_message = soup.find('span', {'style': 'color: #800080'})
        if error_message and '出错了' in error_message.text:
            print(f"选择楼栋失败，页面显示错误：{error_message.text.strip()}")
            return None
        
        # 检查选择楼栋后的页面是否包含房间选择下拉框
        room_select = soup.find('select', {'name': 'ddlFangJian'})
        if room_select:
            print("\n可用的房间选项（前20个）：")
            options = room_select.find_all('option')
            for i, option in enumerate(options[:20]):
                print(f"- 文本: '{option.text.strip()}', 值: '{option['value']}'")
            if len(options) > 20:
                print(f"... 共 {len(options)} 个房间选项")
        else:
            print("未找到房间选择下拉框")
        
        return response
        
    except Exception as e:
        print(f"选择楼栋失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

def query_electricity(session, response, room_number, password, start_date, end_date):
    # 查询电费
    print(f"\n正在查询房间 {room_number} 的电费")
    
    try:
        # 检查响应是否为None
        if response is None:
            print("响应对象为None，无法查询电费")
            return None
        
        # 检查响应状态码
        if hasattr(response, 'status_code') and response.status_code != 200:
            print(f"响应状态码异常：{response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取表单相关参数
        viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
        eventvalidation_input = soup.find('input', {'name': '__EVENTVALIDATION'})
        
        if not viewstate_input or not eventvalidation_input:
            print("未找到表单参数，无法查询电费")
            # 保存响应内容到文件，便于分析
            output_file = "error_response.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"错误响应已保存到：{os.path.abspath(output_file)}")
            return None
        
        viewstate = viewstate_input['value']
        eventvalidation = eventvalidation_input['value']
        
        # 查找房间选择下拉框，获取实际的房间选项值
        room_select = soup.find('select', {'name': 'ddlFangJian'})
        if room_select:
            print("\n查找房间选项：")
            room_value = None
            for option in room_select.find_all('option'):
                print(f"- 文本: '{option.text.strip()}', 值: '{option['value']}'")
                # 找到与目标房间号匹配的选项
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
        
        # 构建表单数据
        data = {
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'ddlXiaoQu': '校本部',
            'ddlQuYu': 'A区                                               ',  # 使用完整的社区值
            'ddlLouDong': '1',  # 楼栋为1栋
            'ddlFangJian': room_value,
            'txtStuPwd': password,
            'btnEnter.x': '1',
            'btnEnter.y': '1'
        }
        
        print("\n构建的表单数据：")
        print(f"- ddlXiaoQu: {data['ddlXiaoQu']}")
        print(f"- ddlQuYu: '{data['ddlQuYu']}'")
        print(f"- ddlLouDong: {data['ddlLouDong']}")
        print(f"- ddlFangJian: {data['ddlFangJian']}")
        print(f"- txtStuPwd: {data['txtStuPwd']}")
        
        # 发送POST请求，查询电费
        electricity_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/"
        response = session.post(electricity_url, data=data, verify=False)
        print(f"查询电费响应状态码：{response.status_code}")
        
        # 保存响应内容到文件
        output_file = "electricity_result.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"电费查询结果已保存到：{os.path.abspath(output_file)}")
        
        # 分析响应内容，提取电费信息
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 检查是否为框架页面
        frameset = soup.find('frameset')
        if frameset:
            print("\n发现框架页面，正在获取stuMainFrame的内容...")
            
            # 查找stuMainFrame
            main_frame = soup.find('frame', {'name': 'stuMainFrame'})
            if main_frame:
                main_frame_src = main_frame.get('src')
                print(f"stuMainFrame的src：{main_frame_src}")
                
                # 构建完整的URL
                if not main_frame_src.startswith('http'):
                    main_frame_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/" + main_frame_src
                else:
                    main_frame_url = main_frame_src
                
                # 发送GET请求，获取stuMainFrame的内容
                main_frame_response = session.get(main_frame_url, verify=False)
                print(f"获取stuMainFrame响应状态码：{main_frame_response.status_code}")
                
                # 保存stuMainFrame的内容到文件
                output_file = "stu_main_frame.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(main_frame_response.text)
                print(f"stuMainFrame内容已保存到：{os.path.abspath(output_file)}")
                
                # 分析stuMainFrame的内容，提取电费信息
                main_frame_soup = BeautifulSoup(main_frame_response.text, 'html.parser')
                
                # 查找包含电费信息的表格或段落
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
                
                # 检查是否存在"用电信息"标签，并模拟点击
                print("\n正在检查是否存在'用电信息'标签...")
                
                # 首先尝试获取stuTopFrame的内容，因为导航栏可能在那里
                print("\n正在获取stuTopFrame的内容...")
                top_frame_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/stuTop.htm"
                top_frame_response = session.get(top_frame_url, verify=False)
                print(f"获取stuTopFrame响应状态码：{top_frame_response.status_code}")
                
                # 保存stuTopFrame的内容到文件
                output_file = "stu_top_frame.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(top_frame_response.text)
                print(f"stuTopFrame内容已保存到：{os.path.abspath(output_file)}")
                
                # 分析stuTopFrame的内容，查找导航栏和"用电信息"链接
                top_frame_soup = BeautifulSoup(top_frame_response.text, 'html.parser')
                electricity_info_link = None
                
                # 查找导航栏中的"用电信息"链接
                # 方法1：通过href属性查找
                for link in top_frame_soup.find_all('a', href=True):
                    if link['href'] == 'HouseElec.aspx':
                        electricity_info_link = link['href']
                        print(f"找到'用电信息'链接：{electricity_info_link}")
                        break
                
                # 如果找不到链接，尝试方法2：通过索引位置查找
                if not electricity_info_link:
                    nav_table = top_frame_soup.find('table')
                    if nav_table:
                        nav_links = nav_table.find_all('a', href=True)
                        if len(nav_links) >= 2:
                            # 第二个链接是"用电信息"
                            electricity_info_link = nav_links[1]['href']
                            print(f"通过索引找到'用电信息'链接：{electricity_info_link}")
                
                # 如果找到"用电信息"链接，模拟点击
                if electricity_info_link:
                    print("\n正在模拟点击'用电信息'标签...")
                    
                    # 构建完整的URL
                    if not electricity_info_link.startswith('http'):
                        electricity_info_url = "https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/" + electricity_info_link
                    else:
                        electricity_info_url = electricity_info_link
                    
                    # 发送GET请求，获取用电信息页面的内容
                    electricity_info_response = session.get(electricity_info_url, verify=False)
                    print(f"获取用电信息页面响应状态码：{electricity_info_response.status_code}")
                    
                    # 保存用电信息页面的内容到文件
                    output_file = "electricity_info_page.html"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(electricity_info_response.text)
                    print(f"用电信息页面已保存到：{os.path.abspath(output_file)}")
                    
                    # 分析用电信息页面的内容
                    electricity_info_soup = BeautifulSoup(electricity_info_response.text, 'html.parser')
                    
                    # 初始化存储所有用电记录的列表
                    all_electricity_records = []
                    headers = []
                    
                    # 解析日期范围
                    start_year, start_month = map(int, start_date.split('-'))
                    end_year, end_month = map(int, end_date.split('-'))
                    
                    print(f"\n开始收集{start_date}到{end_date}的电费记录...")
                    
                    # 遍历日期范围内的每个年月
                    current_year = start_year
                    current_month = start_month
                    
                    while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
                        # 格式化为YYYY-MM格式
                        current_date = f"{current_year}-{current_month:02d}"
                        print(f"\n正在处理月份：{current_date}")
                        
                        # 构建表单数据，选择当前年月
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
                        
                        # 发送POST请求，选择年月
                        month_response = session.post("https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/HouseElec.aspx", 
                                                   data=data, verify=False)
                        
                        # 处理当前月份的分页
                        current_page_response = month_response
                        has_next_page = True
                        
                        while has_next_page:
                            # 分析当前页面的内容
                            page_soup = BeautifulSoup(current_page_response.text, 'html.parser')
                            
                            # 查找用电信息表格
                            table = page_soup.find('table', {'id': 'gvElecInfo'})
                            if table:
                                # 提取表头
                                if not headers:
                                    headers = [th.text.strip() for th in table.find('tr').find_all('th')]
                                
                                # 提取数据行
                                rows = table.find_all('tr')[1:]
                                for row in rows:
                                    # 检查是否是分页行
                                    if row.find('a') and '下一页' in row.text:
                                        continue
                                    
                                    cells = row.find_all('td')
                                    if cells and len(cells) >= 5:
                                        record = [cell.text.strip() for cell in cells]
                                        # 过滤掉日用电量为空的记录
                                        if record[3] not in ['', ' ']:
                                            all_electricity_records.append(record)
                            
                            # 检查是否有下一页
                            has_next_page = False
                            next_page_link = None
                            
                            # 查找下一页链接
                            for link in page_soup.find_all('a'):
                                if '下一页' in link.text:
                                    has_next_page = True
                                    break
                            
                            # 如果有下一页，模拟点击
                            if has_next_page:
                                print("正在获取下一页...")
                                # 提取表单参数
                                viewstate = page_soup.find('input', {'name': '__VIEWSTATE'})['value']
                                eventvalidation = page_soup.find('input', {'name': '__EVENTVALIDATION'})['value']
                                
                                # 构建分页请求数据
                                pagination_data = {
                                    '__VIEWSTATE': viewstate,
                                    '__EVENTVALIDATION': eventvalidation,
                                    'ddlYear': str(current_year),
                                    'ddlMonth': f"{current_month:02d}",
                                    '__EVENTTARGET': 'gvElecInfo',
                                    '__EVENTARGUMENT': 'Page$Next'
                                }
                                
                                # 发送POST请求，获取下一页
                                current_page_response = session.post("https://webvpn.ujs.edu.cn/http/77726476706e69737468656265737421f8e6429b3e296c1e6b029ae29d51367b6885/HouseElec.aspx", 
                                                                   data=pagination_data, verify=False)
                        
                        # 移动到下一个月
                        current_month += 1
                        if current_month > 12:
                            current_month = 1
                            current_year += 1
                    
                    # 计算总用电量
                    total_electricity = 0
                    for record in all_electricity_records:
                        if len(record) > 3 and record[3].strip():
                            try:
                                total_electricity += float(record[3])
                            except ValueError:
                                pass
                    
                    # 整理数据到txt文件
                    if all_electricity_records:
                        print(f"\n成功收集到{len(all_electricity_records)}条电费记录")
                        print(f"周期内总用电量：{total_electricity} 度")
                        
                        # 生成文件名
                        txt_filename = f"electricity_records_{start_date}_{end_date}.txt"
                        
                        # 写入数据到txt文件
                        with open(txt_filename, 'w', encoding='utf-8') as f:
                            f.write(f"电费记录 ({start_date} 到 {end_date})\n")
                            f.write("=" * 80 + "\n")
                            
                            # 写入表头
                            if headers:
                                f.write(' | '.join(headers) + "\n")
                                f.write("-" * 80 + "\n")
                            
                            # 写入记录
                            for record in all_electricity_records:
                                f.write(' | '.join(record) + "\n")
                            
                            f.write("=" * 80 + "\n")
                            f.write(f"总记录数：{len(all_electricity_records)}\n")
                            f.write(f"周期内总用电量：{total_electricity} 度\n")
                        
                        print(f"\n电费记录已保存到：{os.path.abspath(txt_filename)}")
                        print(f"共保存了{len(all_electricity_records)}条记录")
                    else:
                        print(f"\n在{start_date}到{end_date}范围内未找到电费记录")
                else:
                    print("\n未找到'用电信息'标签，可能需要手动点击。")
            else:
                print("未找到stuMainFrame")
        else:
            # 查找包含电费信息的表格或段落
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
        
        return response
        
    except Exception as e:
        print(f"查询电费失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    try:
        # 获取会话
        session = get_session()
        
        # 访问电费查询系统
        response = get_electricity_page(session)
        
        if response:
            # 选择校区为校本部
            response = select_campus(session, response, '校本部')
            
            if response:
                # 选择社区为A区
                response = select_community(session, response, 'A区')
                
                if response:
                    # 选择楼栋为1栋
                    response = select_building(session, response, '1')
                    
                    if response:
                        # 用户输入开始年月和结束年月
                        start_date = input("请输入开始年月（格式：YYYY-MM，例如：2026-01）：").strip()
                        end_date = input("请输入结束年月（格式：YYYY-MM，例如：2026-02）：").strip()
                        
                        # 查询校本部A区1栋404宿舍的电费，初始密码为111
                        query_electricity(session, response, '404', '111', start_date, end_date)
                    
    except Exception as e:
        print(f"操作失败：{str(e)}")

if __name__ == "__main__":
    main()
