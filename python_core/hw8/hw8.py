from datetime import datetime
from datetime import timedelta

# format: "yyyy-mm-dd"
def string_to_datetime(date):
    return datetime.strptime(date, '%Y-%m-%d').date()

# format: datetime.date(y, m, d)
def datetime_to_string(date):
    return date.strftime('%A')

def representation(day, names):
    result = datetime_to_string(day) + ": "
    for n in names:
        result += n + ", "
    print(result[:-2])

def get_birthdays_per_week(users):

    current_day = datetime.today().date()

    # Monday == 0; ...; Sunday == 6
    this_saturday = current_day + timedelta(days=5-current_day.weekday())

    # dictionary of datetimes for selected week
    week = {}
    for d in range(0, 7):
        week[this_saturday + timedelta(days=d)] = []

    # appending names to dictionary week accordind to b-day
    for user in users:
        user_bday_datetime = string_to_datetime(user["birthday"])
        if user_bday_datetime in week:
            week[user_bday_datetime].append(user["name"])

    # printing result
    for day in week.keys():
        # if day of week is Saturday or Sunday
        if day.weekday() > 4:
            continue
        # if day of week is Monday
        elif day.weekday() == 0:
            # list of names of Saturday, Sunday and Monday
            names = week[this_saturday] + week[this_saturday + timedelta(days=1)] + week[day]
            if names: representation(day, names)
        else:
            if week[day]: representation(day, week[day])
