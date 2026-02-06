✅ BEGIN README.md
天语计划官方网站（Tianyu Project Website / JUST-P）

本仓库为“天语计划”（Tianyu Project, JUST-P）官方网站代码库，面向时间域天文学与系外行星搜索等科学目标，依托上海交通大学李政道研究所开展。

线上访问： https://tianyu.sjtu.edu.cn/

站点内容与功能

网站主要面向两类人群：

科研人员与合作方：了解项目科学目标、台址条件、光机系统与观测控制思路，查阅论文与进展；

公众与学生：浏览项目介绍、画廊与科教活动内容。

当前站点包含（中英文双语）：

首页：项目简介、关键指标、快速入口；

关于天语：项目简介、冷湖台址、光机系统、观测控制；

实时气象：李所天文台（源启）与冷湖天文站的环境与天气展示；

天语动态：重要事件、画廊、科教活动；

科学研究：科学目标与研究方向；

团队成员：团队与合作者信息；

出版物：论文与预印本链接整理（如 arXiv 等）。

技术栈与整体架构

后端框架：Python + Flask

模板/前端：Jinja2 + HTML / CSS / JS

部署形态：WSGI（Gunicorn/uWSGI 等）+ Nginx 反向代理

数据组织（常见形态）：

app/data/：团队信息、出版物（BibTeX/JSON）等结构化数据

app/static/：静态资源（CSS/JS/图片/观测点快照与 JSON 等）

app/templates/：Jinja2 模板页面

注：本仓库内容已与服务器部署目录的稳定版本完成同步，并作为后续维护的唯一主工作区。历史旧版工作区（如早期 TDLI_observatory/AstronomyInstitute）已不再在本仓库中保留。

代码结构（示意）
tianyu-website/
  app/
    __init__.py          # Flask 应用初始化
    routes.py            # 页面路由与视图函数
    data/                # 团队、论文等结构化数据
    static/              # 静态资源：CSS / JS / 图片 / 观测点数据输出
    templates/           # Jinja2 模板（页面结构与内容）
  config.py              # 站点配置（建议环境相关配置走 .env）
  wsgi.py                # WSGI 入口文件（生产部署入口）
  requirements.txt       # Python 依赖（如已提供）
  .gitignore             # Git 忽略规则
  README.md              # 本说明文件

本地开发与运行
1) 克隆仓库
git clone git@github.com:UmutMahmut/tianyu-website.git
cd tianyu-website

2) 创建虚拟环境并安装依赖

建议 Python 3.10+。

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

3) 启动开发服务器

方式 A（推荐）：

export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run


方式 B：

python wsgi.py


浏览器访问：

http://127.0.0.1:5000

生产部署建议（简要）

推荐典型架构：

Nginx：静态资源托管 + 反向代理

Gunicorn/uWSGI：加载 wsgi.py 中的 app

systemd：守护进程与自启动

uWSGI 配置示例（仅示意）：

[uwsgi]
chdir = /srv/tianyu-site
module = wsgi:app
virtualenv = /srv/tianyu-site/venv

master = true
processes = 4
socket = 127.0.0.1:8001
vacuum = true
die-on-term = true

实时气象数据说明（开发者向）

站点的“实时气象”页面通常包含两类数据来源：

站点本地输出（例如全天天图/最新气象 JSON），以静态文件形式供前端读取；

公共天气 API 的前端请求（用于预报曲线/未来天气等）。

维护建议：

将观测点采集/同步脚本的产物输出到静态目录（例如 static/<site>/latest*.json|jpg），再由页面 JS 定时读取刷新；

保持“页面展示”与“数据采集”解耦，网站仅负责展示与轻量聚合。

配置与安全

不要提交任何真实密钥/账号密码到仓库：

建议仅提供 .env.example 作为模板；

真实 .env、私钥、证书、日志、数据库文件等应被 .gitignore 忽略。

若站点存在内部页面（如观测控制说明/入口），请确保：

服务器侧访问控制到位（口令/反代鉴权/IP 白名单等）；

仓库中不出现任何内部控制口令与敏感地址。

致谢与维护

天语计划由上海交通大学李政道研究所牵头，多单位协作实施，面向时间域天文学与系外行星搜索等前沿科学目标。

官网：https://tianyu.sjtu.edu.cn/

联系：tianyu_team@sjtu.edu.cn

维护：Tianyu Team

欢迎科研合作、学生参与与公众科普交流。

✅ END README.md
