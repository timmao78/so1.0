#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import time
import re

# --------------------------------------------------------------------
#                          Main Function
# --------------------------------------------------------------------


def scrape_web(url):
    try:
        source = requests.get(url, timeout=20).text
    except Exception as e:
        print(e)
        return None

    soup = BeautifulSoup(source, 'lxml')

    paragraph = soup.find('p').text

    print(paragraph)
    print()
    return paragraph


if __name__ == "__main__":

    week_day_dict = {
    0 : 'Monday',
    1 : 'Tuesday',
    2 : 'Wednesday',
    3 : 'Thursday',
    4 : 'Friday',
    5 : 'Saturday',
    6 : 'Sunday'
  }

    #url_510300_jan = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510300_01?callback=jQuery112402078220234177265_1577088059316&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1577088059323"

    #url_510300_feb = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510300_02?callback=jQuery112402078220234177265_1577088059316&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1577088059351"

    url_510300_mar = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510300_03?callback=jQuery112402078220234177265_1577088059318&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1577088059356"

    url_510300_apr = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510300_04?callback=jQuery112409417454011549969_1582766597079&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1582766597086"

    url_510300_jun = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510300_06?callback=jQuery112402078220234177265_1577088059336&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1577088059360"

    url_510300_sep = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510300_09?callback=jQuery11240028350739831281335_1579742947846&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1579742947854"


    url_510300 = "http://yunhq.sse.com.cn:32041//v1/sh1/line/510300?callback=jQuery1124083017185515941_1577089469213&begin=0&end=-1&select=time%2Cprice%2Cvolume&_=1577089469215"

    #url_510050_jan = "http://yunhq.sse.com.cn:32041/v1/sho/list/tstyle/510050_01?callback=jQuery112408090383939976182_1574904018122&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&_=1574904018127"

    #url_510050_feb = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510050_02?callback=jQuery112407089919710187241_1577321533000&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1577321533005"

    url_510050_mar = "http://yunhq.sse.com.cn:32041/v1/sho/list/tstyle/510050_03?callback=jQuery111206287606767948288_1564018683263&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&_=1564018683268"

    url_510050_apr = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510050_04?callback=jQuery112409417454011549969_1582766597079&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1582766597082"

    url_510050_jun = "http://yunhq.sse.com.cn:32041/v1/sho/list/tstyle/510050_06?callback=jQuery111209494863322515489_1571879875297&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&_=1571879875304"

    url_510050_sep = "http://yunhq.sse.com.cn:32041//v1/sho/list/tstyle/510050_09?callback=jQuery11240028350739831281335_1579742947844&select=contractid%2Clast%2Cchg_rate%2Cpresetpx%2Cexepx&order=contractid%2Cexepx%2Case&_=1579742947849"

    url_510050 = "http://yunhq.sse.com.cn:32041/v1/sh1/line/510050?callback=jQuery111208396578891098054_1563195335181&begin=0&end=-1&select=time%2Cprice%2Cvolume & _ =1563195335188"

    url_list = [url_510300, url_510300_mar, url_510300_apr, url_510300_jun, url_510300_sep, url_510050, url_510050_mar, url_510050_apr, url_510050_jun, url_510050_sep]

    while True:

        now_shanghai = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        file_name = f"./txt/{now_shanghai.strftime('%Y-%m-%d')}.txt"
        print(file_name)

        for url in url_list:
            paragraph = scrape_web(url)

            if paragraph!=None:

                pattern_date = re.compile('"date":(\d+),')
                match_date = re.search(pattern_date, paragraph)
                webdate = int(match_date.group(1))
                realdate = int(now_shanghai.strftime('%Y%m%d'))
                # print("web date is: {}".format(webdate))
                # print("real date is: {}".format(realdate))

                pattern_time = re.compile('"time":(\d+),')
                match_time = re.search(pattern_time, paragraph)
                webtime = int(match_time.group(1))
                realTimeString = now_shanghai.strftime('%H%M%S')
                realTime = int(realTimeString)
                # print("web time is: {}".format(webtime))
                # print("real time is: {}".format(realTime))

                weekday = now_shanghai.weekday() 
                workday = weekday != 5 and weekday != 6 and webdate==realdate

                time_start = 93000
                time_break = 113000 
                time_restart = 130000
                time_stop = 150000
                time_near = 91500
                
                market_open = workday and ((webtime >=  time_start and realTime <  time_break) or (webtime >=  time_restart and realTime <=  time_stop))
                nearly_open = workday and ((time_break <= realTime and webtime <  time_restart) or (time_near < webtime < time_start))

                if market_open:
                    with open(file_name, 'a') as f:
                        try:
                            f.write(paragraph)
                            f.write('\n')
                            print('writing to file...')
                        except Exception as e:
                            print(e)

        if market_open:    
            print('{} {}{}:{}{}:{}{} markets open'.format(week_day_dict[weekday], realTimeString[0],realTimeString[1],
                                                                                realTimeString[2],realTimeString[3],
                                                                                realTimeString[4],realTimeString[5]))
            #print('waiting for 5 seconds')
            #time.sleep(5)
        elif nearly_open:
            print('{} {}{}:{}{}:{}{} markets opening soon'.format(week_day_dict[weekday], realTimeString[0],realTimeString[1],
                                                                                realTimeString[2],realTimeString[3],
                                                                                realTimeString[4],realTimeString[5]))
            print('waiting for 10 seconds')
            time.sleep(10)
        else:
            print('{} {}{}:{}{}:{}{} markets closed'.format(week_day_dict[weekday], realTimeString[0],realTimeString[1],
                                                                                    realTimeString[2],realTimeString[3],
                                                                                    realTimeString[4],realTimeString[5]))
            print('waiting for 10 minutes')
            time.sleep(600)
