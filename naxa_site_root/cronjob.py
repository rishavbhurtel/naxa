import datetime
from naxa_app.models import Profile


def wish_birthday():
    ''' This cron job should run in 0 0 * * *
    so that it runs everyday at midnight.
    also make use this file is executable and
    the python interpreter path is properly given'''
    profile_list = Profile.objects.values_list("birth_date", flat=True)
    month_day = datetime.datetime.now().strftime('%m-%d')
    for profile in profile_list:
        if month_day == profile.strftime('%m-%d'):
            print("Happy Birthday!")
            # or send an email to the user
