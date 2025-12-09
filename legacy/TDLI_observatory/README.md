天语项目官方网站（Tianyu Project Website）

本项目为“天语项目”官方网站，基于 Flask 框架构建，展示了实时气象、团队介绍、新闻动态、科研成果与画廊等内容。支持中英文切换，适配科研展示与对公众开放。


项目结构：
AstronomyInstitute/
  app/
    __init__.py
    routes.py          - 所有页面路由和语言管理
    templates/         - 所有 HTML 页面模板
    static/            - 静态资源：CSS / JS / 图片
    data/              - JSON/BibTeX 数据
  run.py               - 启动入口
  requirements.txt     - 所需依赖列表
  README.txt           - 本说明文件

本地运行方式：
1. 安装依赖：
   建议使用 Python 3.8 及以上版本和虚拟环境：

   python -m venv venv
   source venv/bin/activate （Windows: venv\Scripts\activate）
   pip install -r requirements.txt

2. 启动服务器：
   python run.py
   启动后访问 http://127.0.0.1:5000

语言切换：
网站支持中英文切换，通过页面右上角按钮实现，当前语言保存在用户会话中。

页面内容简介：
- 实时气象：展示多个站点的实时气象观测数据
- 团队成员：从 justp_team.json 动态加载
- 画廊：从 static/images/gallery 目录加载项目照片
- 科学研究：自动读取 publications.bib 文件，展示已发表论文
- 白皮书链接：跳转至 ArXiv 页面

云部署建议：
可选平台包括 Render、Vercel 或 Railway。注意部署环境需包含 setuptools，否则 pybtex 无法运行。

致谢：
本项目由上海交通大学李政道研究所“天语计划”项目组维护。如有合作意向欢迎联系。
