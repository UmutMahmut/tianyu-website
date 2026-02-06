# 天语计划官方网站（Tianyu Project Website）

本仓库为“天语计划”（Tianyu Project, JUST-P）官方网站代码库。  
天语计划是面向时间域天文学与系外行星搜索的大视场、高采样频率巡天项目，依托上海交通大学李政道研究所（TDLI）开展。

- **线上站点：** https://tianyu.sjtu.edu.cn/  
- **仓库：** `UmutMahmut/tianyu-website`

> 说明：站点顶部提供“中文 / EN”切换入口，但目前页面内容以英文为主、部分栏目为中文

---
## 站点现状与主要栏目（以线上版本为准）

首页：项目简介、关键指标、快速入口；

关于天语：项目简介、冷湖台址、光机系统、观测控制；

实时气象：李所天文台（源启）与冷湖天文站的环境与天气展示；

天语动态：重要事件、画廊、科教活动；

科学研究：科学目标与研究方向；

团队成员：团队与合作者信息；

出版物：论文与预印本链接整理（如 arXiv 等）。
---

## 技术栈与架构

- **后端：** Python + Flask  
- **模板：** Jinja2  
- **前端：** 原生 HTML / CSS / JS（少量页面含前端数据请求与展示逻辑）
- **生产部署：** Nginx 反向代理 + WSGI（Gunicorn / uWSGI）  
- **运行目录约定：**
  - 生产部署目录常见为：`/srv/tianyu-site`
  - Git 工作区建议维护为：`/home/umut/tianyu_git/tianyu-website`（通过同步/发布流程更新线上）

---

## 目录结构（示意）

```text
tianyu-website/
  app/
    __init__.py
    routes.py
    static/
      weather_data/          # 运行时气象数据（建议不纳入 Git 跟踪）
    templates/
  wsgi.py
  config.py
  requirements.txt          # 如存在，以其为准
  .env                      # 本地/服务器环境变量（建议仅本地存在）
  .gitignore
  README.md
```

---

## 本地开发

```bash
git clone git@github.com:UmutMahmut/tianyu-website.git
cd tianyu-website

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python wsgi.py
# 或：flask run
```

开发完成后建议走“**Git 提交 → 拉取到服务器 → 重启服务**”的发布方式，尽量避免只在 `/srv/tianyu-site` 里做“不可追溯”的临时修改。

---

## 生产部署（简要）

典型结构：

- Nginx：负责 HTTPS、静态资源与反向代理
- Gunicorn/uWSGI：加载 `wsgi.py` 暴露的 Flask app
- systemd：守护 WSGI 服务并支持平滑重启

（具体配置以服务器实际为准。）

---

## 维护者

天语项目组（Tianyu Team）  
如需协作开发与部署规范（发布流程、systemd/nginx 配置、数据同步脚本等），建议在本仓库补充 `docs/` 文档目录进行沉淀。
