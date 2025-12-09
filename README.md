# 天语计划官方网站（Tianyu Project Website）

本仓库为“天语计划”（Tianyu Project, JUST-P）官方网站的代码库。  
天语计划是面向时间域天文学与系外行星搜索的大视场高采样频率巡天项目，依托上海交通大学李政道研究所开展。

**线上访问：** https://tianyu.sjtu.edu.cn/
---
## 功能概览

网站主要面向以下两类人群：

- 科研人员与合作方：了解项目科学目标、观测手段与科研成果；
- 公众与学生：浏览项目简介、画廊与科教活动等内容。

当前站点包含（中英文双语）：

- 首页：项目简介、特色与快速链接；
- 关于天语：项目概况、冷湖台址、光机系统、观测控制；
- 实时气象：源启天文台、冷湖天文站观测点的环境数据展示；
- 天语动态：重要事件、画廊、科教活动；
- 科学研究：天语计划的核心科学目标与相关研究方向；
- 团队成员：项目团队与合作者介绍。

---
## 技术栈与架构

- 后端框架：Python + Flask
- 前端：Jinja2 模板 + HTML / CSS / JS
- 部署方式：WSGI（例如 uWSGI / Gunicorn）+ Nginx 反向代理
- 数据文件：
  - `app/data/justp_team.json`：团队成员与机构信息
  - `app/data/publications.bib`：BibTeX 格式论文列表
  - `app/data/pub_meta.json`：论文与出版物元数据（分类、标签等）

---
## 代码结构

当前仓库目录结构示意：

```text
tianyu-website/
  app/
    __init__.py          # Flask 应用初始化
    routes.py            # 各页面路由与视图函数
    data/                # 团队、论文等结构化数据
    static/              # 静态资源：CSS / JS / 图片
    templates/           # Jinja2 模板（页面结构与内容）
  config.py              # 站点配置（环境有关配置建议走 .env）
  wsgi.py                # WSGI 入口文件，用于生产部署
  .env                   # 本地/服务器环境变量（不建议公开仓库跟踪真实密钥）
  .gitignore             # Git 忽略规则
  README.md              # 本说明文件
```

---
## 本地开发与运行

### 1. 克隆仓库

```bash
git clone git@github.com:UmutMahmut/tianyu-website.git
cd tianyu-website
```

### 2. 创建虚拟环境并安装依赖

建议使用 Python 3.10 及以上版本。

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 如果仓库中已有 requirements.txt：
pip install -r requirements.txt

# 如果暂时没有 requirements.txt，可以先手动安装 Flask 等依赖：
pip install flask
```

（推荐在服务器上用 `pip freeze > requirements.txt` 导出依赖，再提交到仓库中。）

### 3. 启动开发服务器

根据 `wsgi.py` 和 `app/__init__.py` 的实现方式，一般有两种常见启动方法：

**方式 A：使用 Flask 命令（推荐开发调试时用）**

```bash
export FLASK_APP=wsgi.py          # Windows: set FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run                         # 默认监听 http://127.0.0.1:5000
```

**方式 B：直接运行 WSGI 入口**

```bash
python wsgi.py
```

然后在浏览器访问：

> http://127.0.0.1:5000

---
## 生产部署概览（简要）

在生产环境（如校内云服务器）可以采用：

- Nginx 作为前端服务器与静态资源托管；
- uWSGI / Gunicorn 作为 WSGI 守护进程，加载 `wsgi.py` 中的应用对象；
- systemd 等方式将 WSGI 服务设置为守护进程，更新代码后通过 `git pull` + 重启服务的方式发布。

一个典型的 uWSGI 配置示例（仅示意）：

```ini
[uwsgi]
chdir = /srv/tianyu-site
module = wsgi:app
virtualenv = /srv/tianyu-site/venv

master = true
processes = 4
socket = 127.0.0.1:8001
vacuum = true
die-on-term = true
```

Nginx 则作为反向代理，把外网访问转发到 `127.0.0.1:8001`，同时直接托管 `app/static/` 下的静态资源。

---
## 相关项目与历史版本

- 早期原型与旧版网站代码：
  - 仓库：`TDLI_observatory`（天语/TDLI 相关网站的前身实现，现作为传统版本和参考归档）

本仓库 `tianyu-website` 为当前天语计划官方网站的主代码库，对应实际部署在  
`https://tianyu.sjtu.edu.cn/` 的线上站点。

---
## 致谢与维护

天语计划由上海交通大学李政道研究所牵头，多单位协作实施，面向时间域天文学和系外行星搜索等前沿科学目标。

- 官方网站：https://tianyu.sjtu.edu.cn/
- 代码维护：天语项目组（Tianyu Team）

欢迎科研合作、学生参与与公众科普交流。
