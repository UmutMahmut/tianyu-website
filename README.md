# 天语计划官方网站（Tianyu Project Website）

本仓库为 “天语计划”（Tianyu Project, JUST-P）官方网站的代码库。  
天语计划是面向时间域天文学与系外行星搜索的大视场高采样频率巡天项目，依托上海交通大学李政道研究所开展。  

**线上访问：** https://tianyu.sjtu.edu.cn/   

---

## 功能概览

网站主要面向以下两类人群：

- **科研人员与合作方**：了解项目科学目标、观测手段与科研成果；
- **公众与学生**：浏览项目简介、画廊与科教活动等内容。

当前站点包含（中英文双语）：  

- 首页：项目简介、特色与快速链接；
- 关于天语：项目概况、冷湖台址、光机系统、观测控制；
- 实时气象：源启天文台、冷湖天文站观测点的环境数据展示；
- 天语动态：重要事件、画廊、科教活动；
- 科学研究：天语计划的核心科学目标与相关研究方向；
- 团队成员：项目团队与合作者介绍。

---

## 技术栈与架构

- **后端框架**：Python + Flask
- **前端**：Jinja2 模板 + HTML / CSS / JS
- **部署方式**：WSGI（例如 uWSGI / Gunicorn）+ Nginx 反向代理
- **数据文件**：  
  - `app/data/justp_team.json`：团队成员与机构信息  
  - `app/data/publications.bib`：BibTeX 格式论文列表  
  - `app/data/pub_meta.json`：论文/出版物元数据（分类、标签等）

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
