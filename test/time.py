from datetime import datetime
text = "12:00-20:00"

if ':' and '-' in text:
    try:
        start_time, end_time = text.split('-')
        s_h, s_m= start_time.split(':')
        e_h, e_m= end_time.split(':')
        start_time = datetime.fromisoformat('2000-01-01 {}:{}'.format(s_h,s_m))
        if s_h > e_h:
            end_time = datetime.fromisoformat('2000-01-02 {}:{}'.format(e_h,e_m))
        else:
            end_time = datetime.fromisoformat('2000-01-01 {}:{}'.format(e_h,e_m))
        result = end_time - start_time
        h, m = result.__str__()[:-3].split(":")
        result = "相差{}小時{}分鐘".format(h,m)
        print(result)
    except ValueError:
        print("It seems not a correct format.")
else:        
    print("It seems not a correct format.")