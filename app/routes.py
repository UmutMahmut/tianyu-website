from flask import Blueprint, render_template, session, redirect, request, url_for
import json
import os
from pybtex.database import parse_file

bp = Blueprint('main', __name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# 多语言文案
lang_map = {
    'zh': {
        # 站点名字（用在 LOGO 旁边和 <title>）
        'title': '天语计划',
        'home': '首页',

        # 旧的“项目介绍”文本先保留，避免模板里还有引用
        'project': '项目介绍',

        # 新的“关于天语”主栏目及子栏目
        'about': '关于天语',
        'about_overview': '项目简介',
        'about_lenghu': '冷湖台址',
        'about_optics': '光机系统',          # 导航上的中文标签
        'about_control': '观测控制',

        'team': '团队成员',
        'team_title': '天语望远镜团队',     # 团队页大标题

        'news': '天语动态',
        'events': '重要事件',
        'education_outreach': '科教活动',
        'gallery': '画廊',
        'research': '科学研究',
        'news_placeholder': '项目最新进展、会议活动、建设动态等将发布于此。',
        'research_placeholder': '论文发表、数据发布、科学成果将在本页面集中展示。',
        'weather': '实时气象',
        'yuanqi': '李所天文台',
        'lenghu': '冷湖天文站',
        'welcome': '欢迎访问天语项目网站',
        'intro': '本网站展示与维护多个天文观测项目，包含实时气象、团队介绍和科研动态。',
        'contact_us': '联系我们',
        'email': '邮箱',
        'phone': '电话',
        'address': '上海市浦东新区李所路1号李政道研究所（201210）',

        # 列表用的“标题”列名
        'title_col': '标题',

        'authors': '作者',
        'year': '年份',
        'whitepaper': '白皮书',
        'whitepaper_title': '《天语项目白皮书》',
        'whitepaper_description': '已公开，概述了总体科学任务设计',
        'publications': '已发表论文',
        'publications_link': '📄 本项目的发表论文情况 →',
        'status': '状态',
        'published': '已发表',
        'accepted': '已接收',
        'under_review': '审稿中',
        'data_policy': '数据开放计划',
        'data_policy_description': '天语项目计划在未来建设完毕后开放观测数据，并提供 API 和数据处理平台',
        'outreach_placeholder': '该部分内容尚在开发中，敬请期待！'
    },
    'en': {
        # Site title
        'title': 'Tianyu Project',
        'home': 'Home',

        # Legacy key
        'project': 'Projects',

        # “About Tianyu” menu and submenus
        'about': 'About Tianyu',
        'about_overview': 'Overview',
        'about_lenghu': 'Lenghu Site',
        'about_optics': 'Telescope Optics & Camera',
        'about_control': 'Observation Control',

        'team': 'Team',
        'team_title': 'Tianyu Telescope Team',

        'news': 'Tianyu News',
        'events': 'Major Events',
        'education_outreach': 'Education Outreach',
        'gallery': 'Gallery',
        'research': 'Research',
        'news_placeholder': 'Latest updates, events, and construction progress will be published here.',
        'research_placeholder': 'Scientific publications and data releases will be featured here.',
        'weather': 'Weather',
        'yuanqi': 'TDLI Observatory',
        'lenghu': 'Lenghu Station',
        'welcome': 'Welcome to Tianyu Project Website',
        'intro': 'This site presents ongoing astronomical projects, weather data, and team updates.',
        'contact_us': 'Contact Us',
        'email': 'Email',
        'phone': 'Phone',
        'address': 'Tsung-Dao Lee Institute, 1 Lisuo Road, Pudong New Area, Shanghai, 201210',

        'title_col': 'Title',

        'authors': 'Authors',
        'year': 'Year',
        'whitepaper': 'Whitepaper',
        'whitepaper_title': 'Tianyu Project Whitepaper',
        'whitepaper_description': 'has been published, outlining the overall scientific mission design',
        'publications': 'Publications',
        'publications_link': '📄 Click here for publications →',
        'status': 'Status',
        'published': 'Published',
        'accepted': 'Accepted',
        'under_review': 'Under Review',
        'data_policy': 'Data Sharing Policy',
        'data_policy_description': 'The Tianyu Project plans to open observation data after completion, providing API and data processing platforms',
        'outreach_placeholder': 'This section is under development. Stay tuned!'
    }
}


def get_lang():
    lang = session.get('lang', 'zh')
    if lang not in lang_map:
        lang = 'zh'
        session['lang'] = lang
    return lang

@bp.route('/lang/<lang>')
def set_lang(lang):
    if lang not in lang_map:
        lang = 'zh'
    session['lang'] = lang
    return redirect(request.referrer or '/')


@bp.route('/')
def index():
    strings = lang_map[get_lang()]
    return render_template('index.html', strings=strings)


# === 关于天语 / About Tianyu ===
@bp.route('/about')
def about_overview():
    strings = lang_map[get_lang()]
    return render_template('about/overview.html', strings=strings, get_lang=get_lang)


@bp.route('/about/lenghu')
def about_lenghu():
    strings = lang_map[get_lang()]
    return render_template('about/lenghu.html', strings=strings, get_lang=get_lang)


@bp.route('/about/optics')
def about_optics():
    strings = lang_map[get_lang()]
    return render_template('about/optics.html', strings=strings, get_lang=get_lang)


@bp.route('/about/control')
def about_control():
    strings = lang_map[get_lang()]
    return render_template('about/control.html', strings=strings, get_lang=get_lang)


# 旧 /project URL：做兼容，重定向到新的关于天语首页
@bp.route('/project')
def project():
    return redirect(url_for('main.about_overview'))


# News split
@bp.route('/news/events')
def news_events():
    strings = lang_map[get_lang()]
    return render_template('news/events.html', strings=strings, get_lang=get_lang)


@bp.route('/news/gallery')
def news_gallery():
    strings = lang_map[get_lang()]
    images = [
        {'filename': 'glry_1.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_2.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_3.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_4.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_5.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_6.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_7.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_8.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_9.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_10.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_11.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_12.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_13.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_14.jpg', 'caption': strings.get('', '')},
        {'filename': 'glry_15.jpg', 'caption': strings.get('', '')},
    ]
    return render_template('news/gallery.html', strings=strings, images=images)


@bp.route('/news/outreach')
def news_outreach():
    strings = lang_map[get_lang()]
    return render_template('news/outreach.html', strings=strings, get_lang=get_lang)


# 暂时保留内部观测控制入口（/about/control 里 iframe 还在用）
@bp.route('/internal/observe')
def observe_system():
    return render_template('observe_system.html', strings=lang_map[get_lang()])


@bp.route('/research')
def research():
    strings = lang_map[get_lang()]
    return render_template('research.html', strings=strings)


# Weather
@bp.route('/weather/yuanqi')
def weather_yuanqi():
    strings = lang_map[get_lang()]
    return render_template('weather/TDLI.html', strings=strings)


@bp.route('/weather/lenghu')
def weather_lenghu():
    strings = lang_map[get_lang()]
    return render_template('weather/lenghu.html', strings=strings)


@bp.route('/team')
def team():
    team_file = os.path.join(DATA_DIR, 'justp_team.json')
    if os.path.exists(team_file):
        with open(team_file, encoding='utf-8') as f:
            members = json.load(f)
    else:
        members = []

    lang = get_lang()
    strings = lang_map[lang]

    return render_template(
        'team/members.html',
        members=members,
        strings=strings,
        title=strings.get('team_title', '天语望远镜团队')
    )


# Publications
@bp.route("/publications")
def publications():
    lang = get_lang()
    strings = lang_map[lang]

    bib_path = os.path.join(DATA_DIR, 'publications.bib')
    meta_path = os.path.join(DATA_DIR, 'pub_meta.json')

    bib_data = parse_file(bib_path)

    with open(meta_path, encoding='utf-8') as meta_file:
        meta_data = json.load(meta_file)

    entries = []
    for key, entry in bib_data.entries.items():
        meta = meta_data.get(key, {})
        fields = entry.fields
        authors = " and ".join(str(person) for person in entry.persons.get("author", []))

        entries.append({
            "title": fields.get("title", ""),
            "authors": authors,
            "journal": fields.get("journal", ""),
            "year": fields.get("year", ""),
            "status": meta.get("status", ""),
            "pdf": meta.get("pdf", "#")
        })

    # 年份倒序
    entries.sort(key=lambda e: e.get("year", ""), reverse=True)

    return render_template("publications.html", entries=entries, strings=strings, get_lang=get_lang)