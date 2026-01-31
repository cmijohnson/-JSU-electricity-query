<img width="1805" height="1033" alt="image" src="https://github.com/user-attachments/assets/b8cf983a-5db4-4540-a675-0fb4a470ba58" /># 江苏大学宿舍电费查询系统

## 项目简介

江苏大学宿舍电费查询系统是一个基于Python和Tkinter开发的GUI应用程序，用于查询江苏大学学生宿舍的用电情况。系统支持自动获取VPN cookie、手动输入cookie、按月/按日统计用电量、生成用电趋势图表等功能。

## 功能特性

- 🎯 **VPN Cookie管理**：支持自动获取和手动输入VPN cookie
- 🏠 **宿舍信息管理**：绑定宿舍信息（校区、社区、楼栋、房间号）
- 📊 **用电数据统计**：支持按月/按日统计用电量
- 📈 **数据可视化**：生成美观的用电趋势图表
- 🔄 **自动Selenium安装**：首次使用时自动安装所需依赖
- 🚀 **ChromeDriver自动管理**：自动下载匹配的ChromeDriver
- 📖 **详细的使用指南**：内置帮助文档和操作指南
- 🌐 **跨平台支持**：支持Windows、macOS、Linux系统

## 技术栈

- **Python 3.7+**：核心编程语言
- **Tkinter**：GUI界面框架
- **Selenium**：浏览器自动化（用于获取VPN cookie）
- **webdriver-manager**：自动管理ChromeDriver
- **Matplotlib**：数据可视化图表
- **Requests**：HTTP请求处理
- **BeautifulSoup4**：HTML解析

## 安装指南

### 方法1：直接运行源码

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/electricity-query.git
   cd electricity-query
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python electricity_gui.py
   ```

### 方法2：使用打包版本

1. **下载打包文件**：从GitHub Releases页面下载对应系统的打包文件
2. **解压文件**：解压到任意目录
3. **运行程序**：双击`electricity_gui.exe`（Windows）或对应系统的可执行文件

## 使用方法

### 首次使用

1. **注册账号**：点击"注册"按钮创建新账号
2. **绑定VPN Cookie**：
   - 方法1（推荐）：点击"刷新Cookie"按钮，系统会自动打开Chrome浏览器，使用企业微信扫码登录VPN
   - 方法2：手动获取cookie并粘贴到输入框
3. **绑定宿舍信息**：填写校区、社区、楼栋、房间号和查询密码
4. **设置房间密码**：首次使用时系统会提示设置房间密码和信息
   <img width="1805" height="1033" alt="image" src="https://github.com/user-attachments/assets/2c698710-e5be-4dd6-9e7f-c4981c6ef7b6" />
   <img width="1012" height="775" alt="image" src="https://github.com/user-attachments/assets/d11e193c-1b6b-4116-b93e-4f5c704554b6" />
<img width="960" height="731" alt="image" src="https://github.com/user-attachments/assets/ab7de2af-cbf1-4a39-ad34-aa30498d6be3" />


### 日常使用

1. **登录账号**：使用注册的账号登录
2. **进入电费查询**：点击"电费查询"按钮
3. **选择统计方式**：选择"按月"或"按日"统计
4. **输入查询日期**：输入开始和结束日期（格式：YYYY-MM）
5. **点击查询**：系统会自动获取用电数据
6. **查看结果**：查看查询结果和用电趋势图表
   <img width="1874" height="800" alt="image" src="https://github.com/user-attachments/assets/5d9bd806-f63e-4c5d-b192-ceea2b761837" />


### 手动获取VPN Cookie

1. **登录VPN**：打开浏览器访问`https://webvpn.ujs.edu.cn/login`，使用企业微信扫码登录
2. **打开开发者工具**：按F12打开浏览器开发者工具
3. **切换到控制台**：点击"控制台"（Console）选项卡
4. **输入命令**：在控制台中输入`document.cookie`并按回车
5. **复制cookie**：复制输出的完整cookie字符串
6. **粘贴到系统**：将复制的cookie粘贴到系统的VPN Cookie输入框中

**Cookie示例**：
```
{"show_vpn": "1", "show_fast": "0", "heartbeat": "1", "show_faq": "0", "wengine_vpn_ticketwebvpn_ujs_edu_cn": "xxxxxxxxxxxx"}
```

## 开发指南

### 项目结构

```
electricity-query/
├── electricity_gui.py     # 主程序文件
├── requirements.txt        # 依赖文件
├── README.md              # 项目文档
└── SourceHanSansSC-Bold.otf  # 中文字体文件
```

### 主要模块

1. **ElectricityQuery类**：核心查询逻辑
   - `get_vpn_cookie()`：获取VPN cookie
   - `query_electricity()`：查询电费数据
   - `select_campus()`：选择校区
   - `select_community()`：选择社区
   - `select_building()`：选择楼栋

2. **ElectricityGUI类**：GUI界面管理
   - `create_login_frame()`：登录界面
   - `create_main_frame()`：主界面
   - `create_profile_frame()`：个人中心
   - `create_electricity_frame()`：电费查询界面
   - `show_chart()`：显示图表

### 开发环境搭建

1. **安装Python**：下载并安装Python 3.7+
2. **安装依赖**：
   ```bash
   pip install selenium webdriver-manager matplotlib requests beautifulsoup4
   ```
3. **运行开发版本**：
   ```bash
   python electricity_gui.py
   ```

## 常见问题

### 1. VPN Cookie获取失败

**解决方案**：
- 确保已安装Chrome浏览器
- 检查网络连接是否正常
- 尝试手动获取cookie
- 确保企业微信扫码登录成功

### 2. ChromeDriver相关错误

**解决方案**：
- 系统会自动尝试安装webdriver-manager
- 如果失败，请手动安装：`pip install webdriver-manager`
- 确保Chrome浏览器版本与ChromeDriver兼容

### 3. 首次使用设置失败

**解决方案**：
- 确保VPN连接正常
- 按照系统提示在浏览器中完成设置
- 设置完成后点击"设置完成，继续"按钮

### 4. 图表显示乱码

**解决方案**：
- 确保已安装SourceHanSansSC-Bold.otf字体文件
- 或修改代码中的字体设置为系统可用的中文字体

## 贡献指南

1. **Fork项目**：在GitHub上Fork本项目
2. **创建分支**：创建功能分支
   ```bash
   git checkout -b feature/your-feature
   ```
3. **提交更改**：提交代码更改
   ```bash
   git commit -m "Add your feature"
   ```
4. **推送到远程**：推送代码到远程仓库
   ```bash
   git push origin feature/your-feature
   ```
5. **创建Pull Request**：在GitHub上创建Pull Request

## 许可证

本项目采用MIT许可证

## 致谢

- **原作者**：cmijohnson
- **依赖库**：Selenium、Matplotlib、Requests、BeautifulSoup4等

## 联系方式

- **项目地址**：https://github.com/yourusername/electricity-query
- **问题反馈**：在GitHub Issues中提交问题

---

**江苏大学宿舍电费查询系统** - 让用电管理更智能 🎉
