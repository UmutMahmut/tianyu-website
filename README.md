# 天语计划官方网站（Tianyu Project Website）

<p align="center">
  <img src="app/static/images/logo.jpg" alt="Tianyu Project Logo" width="140" />
</p>

<p align="center">
  <strong>JUST-P（天语计划）官方网站代码库</strong><br/>
  面向时间域天文学与系外行星搜索的大视场高采样频率巡天项目
</p>

<p align="center">
  <a href="https://tianyu.sjtu.edu.cn/">线上站点</a> ·
  <a href="#本地开发与运行">本地运行</a> ·
  <a href="#生产部署概览">生产部署</a> ·
  <a href="#目录结构">目录结构</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.12%2B-informational">
  <img alt="Flask" src="https://img.shields.io/badge/flask-3.x-informational">
  <img alt="License" src="https://img.shields.io/badge/license-TBD-lightgrey">
</p>

---

## 项目简介

本仓库为“天语计划”（Tianyu Project, JUST-P）官方网站的主代码库。  
天语计划依托上海交通大学李政道研究所开展，聚焦**时间域天文学**与**系外行星搜索**等前沿方向。

- **线上访问**：https://tianyu.sjtu.edu.cn/
- **仓库地址**：https://github.com/UmutMahmut/tianyu-website

---

## 功能概览

网站主要面向两类受众：

- **科研人员与合作方**：了解项目科学目标、观测系统与科研成果；
- **公众与学生**：浏览项目简介、画廊与科教活动等内容。

当前站点（中英文双语）包含：

- 首页：项目简介、特色与快速链接；
- 关于天语：项目概况、冷湖台址、光机系统、观测控制；
- 实时气象：源启天文台、冷湖天文站观测点的环境数据展示；
- 天语动态：重要事件、画廊、科教活动；
- 科学研究：核心科学目标与相关研究方向；
- 团队成员：项目团队与合作者介绍。

---

## 技术栈与架构

- **后端**：Python + Flask（Jinja2 模板渲染）
- **前端**：HTML / CSS / JavaScript（静态资源由 Flask + Nginx 托管）
- **数据驱动内容**：
  - `app/data/justp_team.json`：团队成员与机构信息
  - `app/data/publications.bib`：BibTeX 格式论文列表
  - `app/data/pub_meta.json`：论文与出版物元数据（分类、标签等）
- **生产部署**：WSGI（Gunicorn / uWSGI）+ Nginx 反向代理（建议 systemd 守护）

---

## 目录结构

```text
tianyu-website/
  app/
    __init__.py          # Flask 应用初始化
    routes.py            # 各页面路由与视图函数
    data/                # 团队、论文等结构化数据
    static/              # 静态资源：CSS / JS / 图片
    templates/           # Jinja2 模板（页面结构与内容）
  config.py              # 站点配置（环境相关配置建议走 .env）
  wsgi.py                # WSGI 入口文件（生产部署入口）
  requirements.txt       # Python 依赖（建议保持最新）
  .env.example           # 环境变量示例（请按需复制为 .env）
  .gitignore             # Git 忽略规则
  README.md              # 本说明文件
  legacy/                # 历史/迁移过程中的归档（如保留）
```

> **注意**：生产环境通常会有一个**部署目录**（例如 `/srv/tianyu-site`）。  
> 推荐工作流是：**在 Git 仓库中开发与提交 → 再同步到部署目录 → 重启服务**，避免在部署目录直接“热改”。

---

## 本地开发与运行

### 1) 克隆仓库

```bash
git clone git@github.com:UmutMahmut/tianyu-website.git
cd tianyu-website
```

### 2) 创建虚拟环境并安装依赖

建议 Python **3.12+**（与当前服务器环境保持一致更省事）。

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3) 启动开发服务器

**方式 A：Flask 命令（推荐）**

```bash
export FLASK_APP=wsgi.py          # Windows: set FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run                         # http://127.0.0.1:5000
```

**方式 B：直接运行 WSGI 入口（兼容）**

```bash
python wsgi.py
```

---

## 生产部署概览

> 下面给出可用的“参考模板”，实际参数请按服务器路径/端口/域名调整。

### Nginx（示意）

- 静态资源：直接由 Nginx 托管（`/static/`）
- 动态请求：反代到 Gunicorn / uWSGI 的监听端口或 Unix Socket

### Gunicorn + systemd（示意）

`/etc/systemd/system/tianyu-website.service`：

```ini
[Unit]
Description=Tianyu Website (Gunicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/tianyu-site
EnvironmentFile=/srv/tianyu-site/.env
ExecStart=/srv/tianyu-site/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 wsgi:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

启用与重启：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now tianyu-website
sudo systemctl restart tianyu-website
sudo systemctl status tianyu-website
```

---

## 配置与安全建议

- **不要提交真实密钥/Token** 到仓库：
  - 使用 `.env.example` 提供示例；
  - 真实 `.env` 仅在服务器/本机保存，并加入 `.gitignore`。
- 建议开启最小权限与常规安全措施（Nginx 仅暴露必要端口，Gunicorn 监听本地回环或 Unix Socket）。

---

## 更新与发布流程（推荐）

> 典型流程：仓库提交 → 同步到部署目录 → 重启服务。

```bash
# 在仓库工作区
git pull
git add -A
git commit -m "Update site"
git push

# 在服务器部署目录（或由 CI/CD / rsync 完成）
rsync -a --delete /home/umut/tianyu_git/tianyu-website/ /srv/tianyu-site/

# 重启服务
sudo systemctl restart tianyu-website
```

---

## 历史版本说明

- `legacy/`：用于保留迁移过程中的旧版本或历史结构（如需可继续精简）。
- 早期原型项目（已弃用/不再维护）：`TDLI_observatory/AstronomyInstitute`（已在本机备份后可删除）。

---

## 维护与联系

- 官方网站：https://tianyu.sjtu.edu.cn/
- 维护：天语项目组（Tianyu Team）

欢迎科研合作、学生参与与公众科普交流。
