from flask import Blueprint, render_template, session, redirect, request, url_for, send_from_directory, abort
from werkzeug.security import check_password_hash
import json
import os
from pybtex.database import parse_file

bp = Blueprint('main', __name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

INTERNAL_DOCS_DIR = "/srv/tianyu-site-docs"
CONTROL_PASSWORD_HASH = os.getenv("CONTROL_PASSWORD_HASH")
CONTROL_SESSION_KEY = "control_authed"

INTERNAL_DOCS = [
    {
        "filename": "LCO现状.docx",
        "title_zh": "LCO 现状",
        "title_en": "Current Status of LCO",
        "description_zh": "项目内部参考资料，供组内成员下载查阅。",
        "description_en": "Internal reference material for project members.",
        "updated": "2026-04-21"
    }
]

# 多语言文案
lang_map = {
    'zh': {
        'title': '天语计划',
        'home': '首页',

        'project': '项目介绍',

        'about': '关于天语',
        'about_overview': '项目简介',
        'about_lenghu': '冷湖台址',
        'about_optics': '光机系统',
        'about_control': '观测控制',

        'tdli_observatories': '李所天文台',
        'yuanqi_observatory': '源启天文台',
        'muguang_observatory': '慕光天文台',

        'team': '团队成员',
        'team_title': '天语望远镜团队',

        'news': '天语动态',
        'events': '重要事件',
        'education_outreach': '科教活动',
        'gallery': '画廊',
        'research': '科学研究',
        'news_placeholder': '项目最新进展、会议活动、建设动态等将发布于此。',
        'research_placeholder': '论文发表、数据发布、科学成果将在本页面集中展示。',

        'weather': '实时气象',
        'tdli_weather': '源启实时气象',
        'lenghu': '冷湖天文站',

        'yuanqi': '李所天文台',

        'welcome': '欢迎访问天语项目网站',
        'intro': '本网站展示与维护多个天文观测项目，包含实时气象、团队介绍和科研动态。',
        'contact_us': '联系我们',
        'email': '邮箱',
        'phone': '电话',
        'address': '上海市浦东新区李所路1号李政道研究所（201210）',

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
        'title': 'Tianyu Project',
        'home': 'Home',

        'project': 'Projects',

        'about': 'About Tianyu',
        'about_overview': 'Overview',
        'about_lenghu': 'Lenghu Site',
        'about_optics': 'Telescope Optics & Camera',
        'about_control': 'Observation Control',

        'tdli_observatories': 'TDLI Observatories',
        'yuanqi_observatory': 'Yuanqi Observatory',
        'muguang_observatory': 'Muguang Observatory',

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
        'tdli_weather': 'Yuanqi Real-time Weather',
        'lenghu': 'Lenghu Station',

        'yuanqi': 'TDLI Observatory',

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


def is_control_authed():
    return session.get(CONTROL_SESSION_KEY, False) is True


def control_message(key):
    lang = get_lang()
    messages = {
        'zh': {
            'missing_config': '服务器未配置访问口令。',
            'empty_password': '请输入口令。',
            'wrong_password': '口令错误。'
        },
        'en': {
            'missing_config': 'The server access passphrase is not configured.',
            'empty_password': 'Please enter the passphrase.',
            'wrong_password': 'Incorrect passphrase.'
        }
    }
    return messages.get(lang, messages['zh'])[key]


def get_internal_docs():
    lang = get_lang()
    docs = []

    for item in INTERNAL_DOCS:
        path = os.path.join(INTERNAL_DOCS_DIR, item["filename"])
        if not os.path.isfile(path):
            continue

        docs.append({
            "filename": item["filename"],
            "title": item["title_zh"] if lang == "zh" else item["title_en"],
            "description": item["description_zh"] if lang == "zh" else item["description_en"],
            "updated": item["updated"]
        })

    return docs


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
    return render_template(
        'about/control.html',
        strings=strings,
        get_lang=get_lang,
        control_authed=is_control_authed()
    )

@bp.route('/internal/login', methods=['GET', 'POST'])
def internal_login():
    if is_control_authed():
        return redirect(url_for('main.observe_system'))

    strings = lang_map[get_lang()]
    error_message = None

    if request.method == 'POST':
        password = (request.form.get('password') or '').strip()

        if not CONTROL_PASSWORD_HASH:
            error_message = control_message('missing_config')
            session.pop(CONTROL_SESSION_KEY, None)
        elif not password:
            error_message = control_message('empty_password')
            session.pop(CONTROL_SESSION_KEY, None)
        elif check_password_hash(CONTROL_PASSWORD_HASH, password):
            session[CONTROL_SESSION_KEY] = True
            return redirect(url_for('main.observe_system'))
        else:
            error_message = control_message('wrong_password')
            session.pop(CONTROL_SESSION_KEY, None)

    return render_template(
        'internal/login.html',
        strings=strings,
        get_lang=get_lang,
        control_error=error_message
    )

@bp.route('/internal/logout', methods=['POST'])
def internal_logout():
    session.pop(CONTROL_SESSION_KEY, None)
    return redirect(url_for('main.internal_login'))

@bp.route('/about/control/logout', methods=['POST'])
def about_control_logout():
    session.pop(CONTROL_SESSION_KEY, None)
    return redirect(url_for('main.internal_login'))

# === 李所天文台 / TDLI Observatories ===
@bp.route('/tdli_observatories/yuanqi')
def tdli_observatories_yuanqi():
    strings = lang_map[get_lang()]
    return render_template('tdli_observatories/yuanqi.html', strings=strings, get_lang=get_lang)


@bp.route('/tdli_observatories/muguang')
def tdli_observatories_muguang():
    strings = lang_map[get_lang()]
    return render_template('tdli_observatories/muguang.html', strings=strings, get_lang=get_lang)


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


@bp.route('/internal/observe')
def observe_system():
    if not is_control_authed():
       return redirect(url_for('main.internal_login'))

    strings = lang_map[get_lang()]
    internal_docs = get_internal_docs()
    return render_template(
        'observe_system.html',
        strings=strings,
        internal_docs=internal_docs
    )


@bp.route('/internal/docs/<path:filename>')
def download_internal_doc(filename):
    if not is_control_authed():
        return redirect(url_for('main.internal_login'))

    allowed_files = {item["filename"] for item in INTERNAL_DOCS}
    if filename not in allowed_files:
        abort(404)

    file_path = os.path.join(INTERNAL_DOCS_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(INTERNAL_DOCS_DIR, filename, as_attachment=True)


@bp.route('/research')
def research():
    strings = lang_map[get_lang()]
    return render_template('research.html', strings=strings)


# Weather
@bp.route('/weather/yuanqi')
def weather_yuanqi():
    strings = lang_map[get_lang()]
    return render_template('weather/tdli_weather.html', strings=strings)


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
@bp.route('/publications')
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
        authors = ' and '.join(str(person) for person in entry.persons.get('author', []))

        entries.append({
            'title': fields.get('title', ''),
            'authors': authors,
            'journal': fields.get('journal', ''),
            'year': fields.get('year', ''),
            'status': meta.get('status', ''),
            'pdf': meta.get('pdf', '#')
        })

    entries.sort(key=lambda e: e.get('year', ''), reverse=True)

    return render_template('publications.html', entries=entries, strings=strings, get_lang=get_lang)