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
  - Git 工作区建议维护为：`/home/umut/tianyu_git/tianyu-website`（通过安全同步脚本生成筛选快照并推送到 GitHub）

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

当前维护方式中，`/srv/tianyu-site/` 是实际运行和日常微调目录；Git 工作区用于生成筛选后的备份快照和对外展示。

---

## 生产部署与同步流程（当前维护方式）

当前维护中，通常区分两个目录：

- **线上运行目录 / 日常编辑目录：** `/srv/tianyu-site/`
- **Git 工作区 / GitHub 快照仓库：** `/home/umut/tianyu_git/tianyu-website/`

两者职责不同：

| 目录 | 作用 | 说明 |
|---|---|---|
| `/srv/tianyu-site/` | 实际运行网站服务 | 生产环境目录；日常页面微调、内容更新、线上验证主要在这里完成 |
| `/home/umut/tianyu_git/tianyu-website/` | GitHub 备份与对外展示 | 只保存筛选后的项目代码、模板、结构化数据与维护文档，不作为完整生产目录镜像 |

本仓库不是 `/srv/tianyu-site/` 的完整镜像；它是经过过滤的代码快照仓库。

### 推荐流程

1. 在 `/srv/tianyu-site/` 完成页面修改与线上验证；
2. 在 `/home/umut/tianyu_git/` 运行安全同步脚本；
3. 脚本将允许进入仓库的内容同步到 Git 工作区；
4. 人工确认 staged diff；
5. 提交并推送到 GitHub 仓库。

推荐命令：

```bash
cd /home/umut/tianyu_git
./sync_tianyu.sh
```

安全同步脚本应遵循以下原则：

- 不使用 `rsync --delete` 将 `/srv/tianyu-site/` 镜像覆盖 Git 工作区；
- 不删除仓库维护文件，例如 `README.md`、`.gitignore`、`requirements.txt`；
- 不提交 `.env`、`__pycache__/`、`*.pyc`、日志、备份文件；
- 不提交图片、PDF、Word、PPT、Excel、压缩包等二进制资源；
- 默认只同步网站代码、模板、样式脚本与结构化数据。


## Git 快照内容策略

本仓库建议纳入：

- Flask 应用代码：`app/__init__.py`、`app/routes.py`
- Jinja2 模板：`app/templates/`
- 样式与脚本：`app/static/css/`、`app/static/js/`
- 结构化数据：`app/data/*.json`、`app/data/*.bib`
- 项目入口与配置模板：`config.py`、`wsgi.py`、`requirements.txt`
- 维护文档：`README.md`、`.gitignore`

仓库不纳入：

- `.env`、密钥、服务器私有配置；
- `__pycache__/`、`*.pyc`、运行缓存；
- 日志文件、临时备份文件；
- 图片与媒体文件：`*.jpg`、`*.jpeg`、`*.png`、`*.gif`、`*.webp`、`*.svg`、`*.ico`；
- 文档与附件：`*.pdf`、`*.doc`、`*.docx`、`*.ppt`、`*.pptx`、`*.xls`、`*.xlsx`；
- 压缩包：`*.zip`、`*.tar`、`*.tar.gz`、`*.tgz`、`*.7z`、`*.rar`；
- 运行时气象输出：`app/static/yuanqi/`。

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
- 实时气象页面依赖生产目录中的运行时图像与 JSON 数据；相关输出通常不进入 GitHub 快照仓库；
- `.env`、运行时缓存、备份文件与 `__pycache__` 不建议纳入 Git 跟踪；
- 如后续继续扩展内容，建议逐步补充英文页面与维护文档。

---

## 维护者

天语项目组（Tianyu Team）  

如需进一步规范协作开发与部署流程（发布步骤、systemd/nginx 配置、数据同步脚本、页面维护约定等），建议在本仓库补充 `docs/` 文档目录进行沉淀。
