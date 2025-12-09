from flask import Blueprint, render_template, session, redirect, request
import json
import os

main = Blueprint('main', __name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# 中英文文案映射字典
lang_map = {
    'zh': {
        'title': '上海交通大学天语望远镜',
        'home': '首页',
        'project': '项目介绍',
        'team': '团队成员',
        'weather': '实时气象',
        'yuanqi': '源启天文台',
        'lenghu': '冷湖天文站',
        'welcome': '欢迎访问上海交通大学天语望远镜网站',
        'intro': '本网站展示天语望远镜项目，包含实时气象、团队介绍和科研动态。'
    },
    'en': {
        'title': 'SJTU Tianyu Telescope',
        'home': 'Home',
        'project': 'Projects',
        'team': 'Team',
        'weather': 'Weather',
        'yuanqi': 'Yuanqi Observatory',
        'lenghu': 'Lenghu Station',
        'welcome': 'Welcome to SJTU Tianyu Telescope',
        'intro': 'This site presents the Tianyu Telescope project, weather data, and team updates.'
    }
}

def get_lang():
    if 'lang' not in session:
        session['lang'] = 'zh'  # 默认语言设为中文
    return session['lang']

@main.route('/lang/<lang>', strict_slashes=False)
def set_lang(lang):
    session['lang'] = lang
    return redirect(request.referrer or '/')

@main.route('/', strict_slashes=False)
def index():
    strings = lang_map[get_lang()]
    return render_template('index.html', strings=strings)

@main.route('/project', strict_slashes=False)
def project():
    strings = lang_map[get_lang()]
    return render_template('project.html', strings=strings)

@main.route('/weather/yuanqi', strict_slashes=False)
def weather_yuanqi():
    strings = lang_map[get_lang()]
    return render_template('weather/yuanqi.html', strings=strings)

@main.route('/weather/lenghu', strict_slashes=False)
def weather_lenghu():
    strings = lang_map[get_lang()]
    return render_template('weather/lenghu.html', strings=strings)

@main.route('/team', strict_slashes=False)
def team():
    with open(os.path.join(DATA_DIR, 'justp_team.json'), encoding='utf-8') as f:
        members = json.load(f)
    return render_template('team/members.html', members=members, strings=lang_map[get_lang()], title='天语望远镜团队')

@main.route('/test', strict_slashes=False)
def test():
    return "测试页面正常工作！"

from flask import Blueprint, render_template, session, redirect, request
import json
import os

print("routes.py 文件已加载！")  # 添加这行调试信息

main = Blueprint('main', __name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')