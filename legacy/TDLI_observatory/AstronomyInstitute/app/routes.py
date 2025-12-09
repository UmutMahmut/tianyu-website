from flask import Blueprint, render_template, session, redirect, request
import json
import os
from pybtex.database import parse_file

main = Blueprint('main', __name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# 中英文文案映射字典
lang_map = {
    'zh': {
        'title': '天语项目',
        'home': '首页',
        'project': '项目介绍',
        'team': '团队成员',
        'news': '天语动态',
        'research': '科学研究',
        'news_placeholder': '项目最新进展、会议活动、建设动态等将发布于此。',
        'research_placeholder': '论文发表、数据发布、科学成果将在本页面集中展示。',
        'weather': '实时气象',
        'yuanqi': '源启天文台',
        'lenghu': '冷湖天文站',
        'welcome': '欢迎访问天语项目网站',
        'intro': '本网站展示与维护多个天文观测项目，包含实时气象、团队介绍和科研动态。',
        'contact_us': '联系我们',
        'email': '邮箱',
        'phone': '电话',
        'address': '上海市浦东新区李所路1号李政道研究所（201210）',
        'wechat': '微信',
        'weibo': '微博',
        'linkedin': '领英',
        'title': '标题',
        'authors': '作者',
        'year': '年份',
        'whitepaper': '白皮书',
        'whitepaper_title': '《天语项目白皮书》',
        'whitepaper_description': '已公开，概述了总体科学任务设计',
	'publications_link': '📄 本项目的发表论文情况 →',
        'status': '状态',
        'published': '已发表',
        'accepted': '已接收',
        'under_review': '审稿中',
        'data_policy': '数据开放计划',
        'data_policy_description': '天语项目计划在未来建设完毕后开放观测数据，并提供 API 和数据处理平台',
        'major_events': '重要事件',
        'education_outreach': '科教活动',
        'gallery': '画廊',
	'gallery_caption_1': '2025年春季团队合影',
	'gallery_caption_2': '天语计划的COSMOS66相机完成交付与测试',
	'gallery_caption_3': '与学生及同事共赴青海冷湖赛什腾山之行',
	'gallery_caption_4': '高中生们通过HD8望远镜仰望星空',
	'gallery_caption_5': '天语先导项目获交大2030 B类项目支持，计划于2023年正式启动，并计划于2025年开始凌星与时域巡天',
	'gallery_caption_6': '2022年2月21日，上海市委书记李强参观李政道研究所，天语项目（冷湖四台1米望远镜阵列及高精度多目标光谱仪）有望获得支持',

        'outreach_placeholder': '该部分内容尚在开发中，敬请期待！',
    },
    'en': {
        'title': 'Tianyu Project',
        'home': 'Home',
        'project': 'Projects',
        'team': 'Team',
        'news': 'Tianyu News',
        'research': 'Research',
        'news_placeholder': 'Latest updates, events, and construction progress will be published here.',
        'research_placeholder': 'Scientific publications and data releases will be featured here.',
        'weather': 'Weather',
        'yuanqi': 'Yuanqi Observatory',
        'lenghu': 'Lenghu Station',
        'welcome': 'Welcome to Tianyu Project Website',
        'intro': 'This site presents ongoing astronomical projects, weather data, and team updates.',
        'contact_us': 'Contact Us',
        'email': 'Email',
        'phone': 'Phone',
        'address': 'Tsung-Dao Lee Institute, 1 Lisuo Road, Pudong New Area, Shanghai, 201210',
        'wechat': 'WeChat',
        'weibo': 'Weibo',
        'linkedin': 'LinkedIn',
        'title': 'Title',
        'authors': 'Authors',
        'year': 'Year',
        'whitepaper': 'Whitepaper',
        'whitepaper_title': 'Tianyu Project Whitepaper',
        'whitepaper_description': 'has been published, outlining the overall scientific mission design',
	'publications_link': '📄 Click here for publications →',
        'status': 'Status',
        'published': 'Published',
        'accepted': 'Accepted',
        'under_review': 'Under Review',
        'data_policy': 'Data Sharing Policy',
        'data_policy_description': 'The Tianyu Project plans to open observation data after completion, providing API and data processing platforms',
        'major_events': 'Major Events',
        'education_outreach': 'Education Outreach',
        'gallery': 'Gallery',
        'gallery_caption_1': 'Our group photo in 2025 spring',
        'gallery_caption_2': 'The COSMOS66 Camera for Tianyu has been delivered and tested',
        'gallery_caption_3': 'A wonderful trip to Saishiteng Mountain in Lenghu, Qinghai, with the students and colleagues.',
        'gallery_caption_4': 'High school students view stars with HD8',
        'gallery_caption_5': 'Tianyu pathfinder will be funded by Jiaoda 2030 Type-B grant. The Tianyu project will be formally launched in 2023 and will start to do transit and time-domain survey in 2024',
        'gallery_caption_6': 'Shanghai party chief Qiang Li visited TDLI on Feb. 21, 2022, and hopefully the Tianyu project (a multi-object high precision spectrograph connected to four 1-meter sized telescope array located in Qinghai Lenghu) would be funded soon',
        'outreach_placeholder': 'This section is under development. Stay tuned!',
    }
}


def get_lang():
    if 'lang' not in session:
        session['lang'] = 'zh'  # 默认语言设为中文
    return session['lang']


@main.route('/lang/<lang>')
def set_lang(lang):
    session['lang'] = lang
    return redirect(request.referrer or '/')


@main.route('/')
def index():
    strings = lang_map[get_lang()]
    return render_template('index.html', strings=strings)


@main.route('/project')
def project():
    strings = lang_map[get_lang()]
    return render_template('project.html', strings=strings)


@main.route('/news/events')
def news_events():
    strings = lang_map[get_lang()]
    return render_template('news/events.html', strings=strings, get_lang=get_lang)


@main.route('/news/outreach')
def news_outreach():
    strings = lang_map[get_lang()]
    return render_template('news/outreach.html', strings=strings, get_lang=get_lang)


@main.route('/news/gallery')
def gallery():
    strings = lang_map[get_lang()]
    images = [
        {'filename': 'glry_1.jpg', 'caption': strings['gallery_caption_1']},
        {'filename': 'glry_2.jpg', 'caption': strings['gallery_caption_2']},
        {'filename': 'glry_3.jpg', 'caption': strings['gallery_caption_3']},
        {'filename': 'glry_4.jpg', 'caption': strings['gallery_caption_4']},
        {'filename': 'glry_5.jpg', 'caption': strings['gallery_caption_5']},
        {'filename': 'glry_6.jpg', 'caption': strings['gallery_caption_6']},
    ]
    return render_template('news/gallery.html', strings=strings, images=images)


@main.route('/research')
def research():
    strings = lang_map[get_lang()]
    return render_template('research.html', strings=strings)


@main.route('/weather/yuanqi')
def weather_yuanqi():
    strings = lang_map[get_lang()]
    return render_template('weather/yuanqi.html', strings=strings)


@main.route('/weather/lenghu')
def weather_lenghu():
    strings = lang_map[get_lang()]
    return render_template('weather/lenghu.html', strings=strings)


@main.route('/team')
def team():
    team_file = os.path.join(DATA_DIR, 'justp_team.json')
    if os.path.exists(team_file):
        with open(team_file, encoding='utf-8') as f:
            members = json.load(f)
    else:
        members = []
    return render_template('team/members.html', members=members, strings=lang_map[get_lang()], title='天语望远镜团队')


@main.route("/publications")
def publications():
    lang = get_lang()
    strings = lang_map[lang]  # 确保先定义

    bib_path = os.path.join(DATA_DIR, 'publications.bib')
    meta_path = os.path.join(DATA_DIR, 'pub_meta.json')

    # 解析 BibTeX 文件
    bib_data = parse_file(bib_path)

    # 加载元信息（PDF、状态等）
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

    # 按年份倒序排序（最新在前）
    entries.sort(key=lambda e: e.get("year", ""), reverse=True)

    return render_template("publications.html", entries=entries, strings=strings, get_lang=get_lang)