import pytz

def fromUTCtoLocal(time):

    now_utc = time
    local_tz = pytz.timezone("Asia/Vladivostok")
    local_time = now_utc.astimezone(local_tz)
    return local_time


def fromLocaltoUTC(time):
    now_local = time
    local_tz = pytz.timezone("Asia/Vladivostok")
    now_local = now_local.replace(tzinfo=local_tz)
    utc_tz= pytz.timezone("UTC")
    utc_time = now_local.astimezone(utc_tz)
    return utc_time