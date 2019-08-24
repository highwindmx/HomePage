
from datetime import (datetime,timedelta)
import webbrowser
#
from flask import (Flask, render_template, request, redirect, url_for, jsonify)

from data import (data_city_table, data_count, bar_base, map_base, mon_l)

#2 建立和配置Flask
flaskserver = Flask(__name__)
flaskserver.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5) # 不然由于浏览器存储了静态文件，则即使改了也很久（若干小时之后）才会更新

####################################

@flaskserver.route("/", methods=["POST", "GET"])
def home():
    refreshtime = datetime.now().strftime("%Y{0}%m{1}%d{2} %H:%M:%S").format(*'年月日') #得用format格式化不然会出现unicode错误
    return render_template("index.html", issearch=False, rftime = refreshtime) # issearch是传递判断是否需要在navbar添加搜索框的

@flaskserver.route("/notebook/", methods=["POST", "GET"])
def homeNoteBook():
    # data_city_table_html = data_city_table.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    # 使用 pandas 的 to_html展示表格
    return render_template("homenotebook.html", issearch=False)

@flaskserver.route("/search/", methods=["POST", "GET"])
def homeSearch():
    home_search_keywords = ""
    home_search_engine = "bing"
    home_search_in_engine_list = ["bing","baidu","sogou","dogedoge","blank"]
    home_search_out_engine_list = ["zhihu","wechat","github","movie","subtitle","cloudpan","torrent","navigator"] 
    # 各引擎排列顺序，这就就得采用列表的数据结构了
    if request.method == "POST":
        got_json = request.get_json() #print(jsonify(home_search_engine))
        if got_json:
            home_search_keywords = got_json['keywordVal'] # 接收ajax传递来的json
            home_search_keywords = "+".join(home_search_keywords.split(" "))
            home_search_engine = got_json['engineVal']
        else:
            if request.form.get("formi-keywords"): 
                home_search_keywords = request.form.get("formi-keywords") # 接收form传递来input里面的value
                home_search_keywords = "+".join(home_search_keywords.split(" "))
        print(f"将在 {home_search_engine} 中检索 {home_search_keywords}")
        if home_search_engine == "zhihu":
            webbrowser.open_new_tab("https://www.zhihu.com/search?type=content&q=" + home_search_keywords) # 知乎
            # 有些网站限制了用embed或iframe获取界面，只能用自带的webbrowser模块新开一个标签页
        if home_search_engine == "github":
            webbrowser.open_new_tab("https://github.com/search?q=" + home_search_keywords) # github
        if home_search_engine == "wechat":
            webbrowser.open_new_tab("https://weixin.sogou.com/weixin?type=2&query=" + home_search_keywords) # 搜狗微信
        
            
    home_search_in_engine_dict = {"bing":{"title":"必应搜索", "type":"门户", "url":"https://cn.bing.com/search?q=" + home_search_keywords}
                                 ,"baidu":{"title":"百度搜索", "type":"门户", "url":"https://www.baidu.com/baidu?wd=" + home_search_keywords}
                                 ,"sogou":{"title":"搜狗搜索", "type":"门户", "url":"https://www.sogou.com/web?query=" + home_search_keywords}
                                 ,"dogedoge":{"title":"搜狗搜索", "type":"门户", "url":"https://www.dogedoge.com/results?q=" + home_search_keywords}
                                 ,"blank":{"title":"搜索反馈", "type":"反馈", "url":url_for('static', filename='/selfmade/home_search_404.html')}
                                 }
    home_search_out_engine_dict = {"zhihu":{"title":"知乎搜索", "type":"知识", "url":""}
                                  ,"wechat":{"title":"搜狗微信搜索", "type":"知识", "url":""}
                                  ,"github":{"title":"GitHub", "type":"知识", "url":""}
                                  ,"movie":{"title":"电影", "type":"批量", "url":""}
                                  ,"subtitle":{"title":"字幕", "type":"批量", "url":""}
                                  ,"cloudpan":{"title":"云盘", "type":"批量", "url":""} 
                                  ,"torrent":{"title":"种子磁链", "type":"批量", "url":""} 
                                  ,"navigator":{"title":"导航站", "type":"批量", "url":""} 
                                  }
    #print(home_search_in_engine_dict["blank"]["url"])
    return render_template("homesearch.html", issearch=True, kwvalue=home_search_keywords, egUl = home_search_in_engine_list, egRl = home_search_out_engine_list
                          ,egUd = home_search_in_engine_dict, egRd = home_search_out_engine_dict)

@flaskserver.route("/analysis/", methods=["POST", "GET"])
def homeAnalysis():
    data_city_table_html = data_city_table.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    # 使用 pandas 的 to_html展示表格
    return render_template("homeanalysis.html", issearch=False, dtcnt=data_count, dtctl = data_city_table_html)

############################ 以下是使用pyecharts模块的内容 #####################
@flaskserver.route("/pyecharts_saleclothes/")
def pyechartsdemo1():
    return render_template("pyecharts_demo1.html", issearch=False)

@flaskserver.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes() # 逻辑类似于用主函数引入一个另外准备好的网址显示内容

@flaskserver.route("/pyecharts_salemap/")
def pyechartsdemo2():
    return render_template("pyecharts_demo2.html", issearch=False, maps=mon_l)

@flaskserver.route("/map/<mon>")
def get_map_chart(mon):
    #print(mon)
    c = map_base()[mon]
    return c.dump_options_with_quotes()
#5 运行
if __name__ == "__main__": 
    flaskserver.run(debug=True, port="6789")