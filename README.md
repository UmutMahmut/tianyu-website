# 天语计划官方网站（Tianyu Project Website）

本仓库为“天语计划”（Tianyu Project, JUST-P）官方网站代码库。  
天语计划是面向时间域天文学与系外行星搜索的大视场、高采样频率巡天项目，依托上海交通大学李政道研究所（TDLI）开展。

- **线上站点：** https://tianyu.sjtu.edu.cn/  
- **仓库：** `UmutMahmut/tianyu-website`

> 说明：站点顶部提供“中文 / EN”切换入口；当前中文页面已基本可用，英文页面仍在持续补充与调整。

---

## 站点现状与主要栏目（以当前线上版本为准）

首页：项目概述、关键指标、快速入口；

关于天语：项目简介、冷湖台址、光机系统、观测控制；

李所天文台：源启天文台、慕光天文台；

实时气象：源启实时气象、冷湖天文站；

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
    data/
    static/
      css/
      images/
      js/
      tdli/
      yuanqi/               # 运行时气象图像与 JSON 数据
    templates/
      about/
      news/
      team/
      weather/
      tdli_observatories/
      _partials/
      _macros/
  wsgi.py
  config.py
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

开发完成后建议走“**Git 提交 → 同步到服务器 → 重启服务**”的发布方式，尽量避免只在 `/srv/tianyu-site` 中做不可追溯的临时修改。

---

## 生产部署与同步流程（当前维护方式）

当前维护中，通常区分两个目录：

- **线上运行目录：** `/srv/tianyu-site/`
- **Git 工作区：** `/home/umut/tianyu_git/tianyu-website/`

建议流程：

1. 在 `/srv/tianyu-site/` 完成页面修改与线上验证；
2. 将当前可运行版本同步到 Git 工作区；
3. 在 Git 工作区执行 `git status`、`git add`、`git commit`；
4. 推送到 GitHub 仓库。

同步示例：

```bash
rsync -av \
  --delete \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.bak.*' \
  /srv/tianyu-site/ /home/umut/tianyu_git/tianyu-website/
```

---

## 运行与重启

如果站点由 systemd 管理，可使用：

```bash
sudo systemctl restart tianyu
sudo systemctl status tianyu
```

查看最近日志：

```bash
sudo journalctl -u tianyu -n 100 --no-pager
```

---

## 维护说明

- 页面结构和栏目设置仍在持续完善中；
- 李所天文台相关页面当前已完成首轮上线，后续将继续补充资料与图片；
- 实时气象页面依赖 `/static/yuanqi/` 下的运行时图像与 JSON 数据；
- `.env`、运行时缓存、备份文件与 `__pycache__` 不建议纳入 Git 跟踪；
- 如后续继续扩展内容，建议逐步补充英文页面与维护文档。

---

## 维护者

天语项目组（Tianyu Team）  

如需进一步规范协作开发与部署流程（发布步骤、systemd/nginx 配置、数据同步脚本、页面维护约定等），建议在本仓库补充 `docs/` 文档目录进行沉淀。
