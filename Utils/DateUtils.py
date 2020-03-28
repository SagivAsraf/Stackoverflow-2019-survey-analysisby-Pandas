from datetime import datetime


class DateUtils:

    @staticmethod
    def get_today_date():
        today = datetime.today()
        d1 = today.strftime("%m/%d/%Y")
        return d1

    @staticmethod
    def get_time():
        now = datetime.now()
        time = now.strftime("%d-%m-%Y_%H.%M.%S")
        return time

    @staticmethod
    def get_time_without_hour():
        now = datetime.now()
        time = now.strftime("%Y-%m-%d")
        return time