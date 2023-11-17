import os
import datetime
from dateutil.relativedelta import relativedelta, MO
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.getcwd())

@app.route('/')
def index():
    # 현재 날짜부터 1년 뒤의 12월 말까지의 날짜 범위를 설정
    start_date = datetime.date.today()
    end_date = datetime.date(start_date.year + 1, 12, 31)

    # 성수기 및 초성수기 날짜 목록을 정의
    peak_season = set()
    super_peak_season = set()

    # 성수기와 초성수기 날짜 범위를 현재 연도와 다음 연도 모두 포함하도록 설정
    for year in [start_date.year, end_date.year]:
        peak_season.update([
            datetime.date(year, 1, 1),  # 신정
            datetime.date(year, 2, 11), # 헌법 기념일
            datetime.date(year, 2, 23), # 천황 탄생일
            datetime.date(year, 4, 29), # 쇼와의 날
            datetime.date(year, 5, 3),  # 헌법 기념일
            datetime.date(year, 5, 4),  # 미도리의 날
            datetime.date(year, 5, 5),  # 어린이날
            datetime.date(year, 8, 11), # 산의 날
            datetime.date(year, 11, 3), # 문화의 날
            datetime.date(year, 11, 23) # 노동 감사의 날
        ])

        # 월별 두 번째 월요일 및 세 번째 월요일에 해당하는 공휴일 추가
        for month, day in [(1, MO(2)), (7, MO(3)), (9, MO(3)), (10, MO(2))]:
            peak_season.add(datetime.date(year, month, 1) + relativedelta(weekday=day))

        # 춘분과 추분의 가능한 날짜
        for day in range(19, 23):
            peak_season.add(datetime.date(year, 3, day))
        for day in range(21, 25):
            peak_season.add(datetime.date(year, 9, day))
            
        # 성수기 날짜 정의
        peak_season.update({datetime.date(year, 3, 21) + datetime.timedelta(days=i) for i in range(16)})
        peak_season.update({datetime.date(year, 4, 28) + datetime.timedelta(days=i) for i in range(9)})
        peak_season.update({datetime.date(year, 7, 21) + datetime.timedelta(days=i) for i in range(42)})
        peak_season.update({datetime.date(year, 12, 25) + datetime.timedelta(days=i) for i in range(17)})

        # 초성수기 날짜 정의
        super_peak_season.update({datetime.date(year, 12, 28) + datetime.timedelta(days=i) for i in range(10)})
        super_peak_season.update({datetime.date(year, 4, 28) + datetime.timedelta(days=i) for i in range(9)})
        super_peak_season.update({datetime.date(year, 8, 10) + datetime.timedelta(days=i) for i in range(10)})

    # 각 날짜별로 초성수기, 성수기 여부 확인
    result = {"초성수기": [], "성수기": [], "비수기": []}
    current_date = start_date
    while current_date <= end_date:
        if current_date in super_peak_season:
            result["초성수기"].append(current_date)
        elif current_date in peak_season:
            result["성수기"].append(current_date)
##        else:
##            result["비수기"].append(current_date)
        current_date += datetime.timedelta(days=1)

    # HTML 페이지에 결과를 전달
    return render_template('index.html', result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    debug = "DEBUG" in os.environ
    app.run(host='0.0.0.0', port=port, debug=debug)
