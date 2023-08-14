import lvgl as lv
import json
import urequests
import utime

scr = lv.scr_act()
the_question_btn = lv.btn(scr)
the_question_btn.set_size(200,50)
the_question_label = lv.label(the_question_btn)
the_question_label.set_text("click me!")
the_question_label.center()


chart = lv.chart(lv.scr_act())
chart.set_size(180,150)
chart.set_style_bg_color(lv.color_hex(0x000000),0)
chart.set_style_line_color(lv.color_hex(0x1aec1a),0)
chart.set_style_border_color(lv.color_hex(0x1aec1a),0)

chart.align_to(the_question_btn, lv.ALIGN.OUT_BOTTOM_RIGHT,40,10)
chart.set_type(lv.chart.TYPE.LINE)
chart.set_update_mode(lv.chart.UPDATE_MODE.SHIFT)
chart.set_point_count(30)
chart.set_div_line_count(0,0)

ser1 = chart.add_series(lv.color_hex(0x00eeff), lv.chart.AXIS.PRIMARY_Y)
chart.set_range(lv.chart.AXIS.PRIMARY_Y, 0, 1000)
chart.set_axis_tick( lv.chart.AXIS.PRIMARY_Y, 15, 5, 8, 2, True, 60)

def update_chart(chart,series):
    ymax = 500
    url = 'http://192.168.1.120/co2/query.php'
    data = urequests.get(url)
    data_j = json.loads(data.text)
    print(data_j)
    for i in data_j:
        if(type(i['mean']) != None.__class__):
            temp = int(i['mean'])
            print(temp)
            chart.set_next_value(series, temp)
            if temp > ymax:
                ymax = ((temp // 500) * 500) + 500
                chart.set_range(lv.chart.AXIS.PRIMARY_Y, 0, ymax)
                print("Updated yrange to ", ymax)

while True:
    update_chart(chart,ser1)
    utime.sleep(10)