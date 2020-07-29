from datetime import datetime, time


def is_time_between(begin_time, end_time, check_time=None):

    begin_time = time(begin_time[0], begin_time[1])
    end_time = time(end_time[0], end_time[1])

    # If check time is not given, default to current time
    check_time = check_time or datetime.now().time()

    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:  # If crosses midnight
        return check_time >= begin_time or check_time <= end_time
