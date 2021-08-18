from datetime import datetime
text = "11:00-13:00"

if ':' and '-' in text:
    try:
        start_time, end_time = text.split('-')
        s_h, s_m= start_time.split(':')
        e_h, e_m= end_time.split(':')
        start_time = datetime.strptime(start_time,'%H:%M')
        end_time = datetime.strptime(end_time,'%H:%M')
        result = end_time - start_time
        print(result)
    except ValueError:
        print("It seems not a correct format.")
else:        
    print("It seems not a correct format.")