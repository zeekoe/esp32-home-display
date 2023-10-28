import lvgl as lv
import json
import urequests
import utime
import machine


scr = lv.scr_act()
scr.set_style_bg_color( lv.color_hex( 0x000000 ), lv.PART.MAIN | lv.STATE.DEFAULT )
# the_question_btn = lv.btn(scr)
# the_question_btn.set_size(200,50)
# the_question_label = lv.label(the_question_btn)
# the_question_label.set_text("click me!")
# the_question_label.center()

chart = lv.chart(scr)
chart.set_size(180,150)
chart.set_style_bg_color(lv.color_hex(0x000000),0)
chart.set_style_line_color(lv.color_hex(0x1aec1a),0)
chart.set_style_border_color(lv.color_hex(0x1aec1a),0)
chart.set_style_border_color( lv.color_hex( 0x000000 ), lv.PART.MAIN | lv.STATE.DEFAULT )
chart.set_style_text_color( lv.color_hex( 0x008817 ), lv.PART.TICKS | lv.STATE.DEFAULT )

chart.align_to(scr, lv.ALIGN.TOP_RIGHT,0,10)
chart.set_type(lv.chart.TYPE.LINE)
chart.set_update_mode(lv.chart.UPDATE_MODE.SHIFT)
chart.set_point_count(60)
chart.set_div_line_count(0,0)

ser1 = chart.add_series(lv.color_hex(0x008817), lv.chart.AXIS.PRIMARY_Y)
chart.set_range(lv.chart.AXIS.PRIMARY_Y, 0, 1000)
chart.set_axis_tick(lv.chart.AXIS.PRIMARY_Y, 10, 5, 5, 2, True, 50)
chart.set_style_size(0, 0, lv.PART.INDICATOR)

ymax = 1000
url = 'http://192.168.1.120/co2/query.php'
data = urequests.get(url)
data_j = json.loads(data.text)
print(data_j)

ta = lv.textarea(scr)
ta.align_to(chart,lv.ALIGN.TOP_RIGHT,30,150)

valuebuf = []
for i in data_j:
    if(type(i['mean']) != None.__class__):
        temp = int(i['mean'])
        valuebuf.append(temp)
        chart.set_next_value(ser1, temp)
        if temp > ymax:
            ymax = ((temp // 500) * 500) + 500
            chart.set_range(lv.chart.AXIS.PRIMARY_Y, 0, ymax)
            print("Updated yrange to ", ymax)

def update_chart(chart,series):
    ymax = 1000
    url = 'http://192.168.1.120/co2/query.php?window=1'
    data = urequests.get(url)
    data_j = json.loads(data.text)
    print(data_j)
    for i in data_j:
        if(type(i['mean']) != None.__class__):
            temp = int(i['mean'])
            valuebuf.append(temp)
            valuebuf.reverse()
            valuebuf.pop()
            valuebuf.reverse()
            chart.set_next_value(series, temp)
            ymax = ((max(valuebuf) // 500) * 500) + 500
            chart.set_range(lv.chart.AXIS.PRIMARY_Y, 0, ymax)
            print("Updated yrange to ", ymax)

def update_text(ta):
    url2 = 'http://192.168.1.120/co2/blackbird.php'
    data2 = urequests.get(url2)
    data_j2 = json.loads(data2.text)
    ta.set_text("Tijd: ")
    ta.add_text(data_j2['time'])
    ta.add_text("\nVerm. in: ")
    ta.add_text(data_j2['Pin'])
    ta.add_text("\nVerm. uit: ")
    ta.add_text(data_j2['Pout'])
    ta.add_text("\nLucht in: ")
    ta.add_text(data_j2['t_air_in'])
    ta.add_text("\nLucht uit: ")
    ta.add_text(data_j2['t_air_out'])
    ta.add_text("\nWater CV: ")
    ta.add_text(data_j2['t_water_house_in'])
    ta.add_text("\nCOP, RPM: ")
    ta.add_text(data_j2['hCOP'])
    ta.add_text(", ")
    ta.add_text(data_j2['rpm'])


while True:
    update_chart(chart,ser1)
    update_text(ta)
    utime.sleep(30)