from .enums import *
from uuid import uuid4
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

def generate_uuid():
    return uuid4().hex


"""
return  the end date based on date_start and the number of days
"""
def determine_end_date_knowing_duration(start_date, number_of_days):
    end_date = start_date + timedelta(days=number_of_days)
    return end_date

"""
Providing the date_start and the date_end, this function convert
and return the remainning duration  in days, hours, minuites, secondes
"""
def determine_remaining_duration(start_date, end_date):
    remaining_duration = end_date - start_date
    days, remainder = divmod(remaining_duration.days * 86400 + remaining_duration.seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes, seconds
