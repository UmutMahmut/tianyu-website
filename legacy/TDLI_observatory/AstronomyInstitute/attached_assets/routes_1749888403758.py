from flask import Blueprint, render_template, session, redirect, request
import json
import os

main = Blueprint('main', __name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# 中英文文案映射字典
lang_map = {
    'zh': {
        'title': '李政道研究所天文台',
        'home': '首页',
        'project': '项目介绍',
        'team': '团队成员',
        'weather': '实时气象',
        'yuanqi': '源启天文台',
        'lenghu': '冷湖天文站',
        'welcome': '欢迎访问李政道研究所天文台网站',
        'intro': '本网站展示与维护多个天文观测项目，包含实时气象、团队介绍和科研动态。'
    },
    'en': {
        'title': 'TDLI Observatory',
        'home': 'Home',
        'project': 'Projects',
        'team': 'Team',
        'weather': 'Weather',
        'yuanqi': 'Yuanqi Observatory',
        'lenghu': 'Lenghu Station',
        'welcome': 'Welcome to TDLI Observatory',
        'intro': 'This site presents ongoing astronomical projects, weather data, and team updates.'
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

@main.route('/weather/yuanqi')
def weather_yuanqi():
    strings = lang_map[get_lang()]
    return render_template('weather/yuanqi.html', strings=strings)

@main.route('/weather/lenghu')
def weather_lenghu():
    strings = lang_map[get_lang()]
    return render_template('weather/lenghu.html', strings=strings)

@main.route('/team/just')
def team_just():
    with open(os.path.join(DATA_DIR, 'just_team.json'), encoding='utf-8') as f:
        members = json.load(f)
    return render_template('team/members.html', members=members, strings=lang_map[get_lang()], title='JUST')

@main.route('/team/justp')
def team_justp():
    with open(os.path.join(DATA_DIR, 'justp_team.json'), encoding='utf-8') as f:
        members = json.load(f)
    return render_template('team/members.html', members=members, strings=lang_map[get_lang()], title='天语（JUST-P）')
