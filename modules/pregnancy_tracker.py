# pregnancy_tracker.py

from datetime import datetime, date
import json
import os


import json
from pathlib import Path


def load_pregnancy_data():

    json_path = Path(__file__).parent.parent / "data" / "pregnancy_data.json"

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_pregnancy_week(lmp_date):

    today = date.today()

    days_pregnant = (today - lmp_date).days

    weeks = days_pregnant // 7

    # Pregnancy normally 40 weeks hoti hai,
    # lekin tracker 42 weeks tak support karega
    if weeks < 1:
        weeks = 1

    if weeks > 42:
        weeks = 42

    return weeks, days_pregnant



def calculate_due_date(lmp_date):

    due_date = lmp_date.replace()

    # 280 days = 40 weeks
    from datetime import timedelta

    return lmp_date + timedelta(days=280)



def get_trimester(week):

    if week <= 12:
        return "First Trimester"

    elif week <= 27:
        return "Second Trimester"

    else:
        return "Third Trimester"



def pregnancy_analysis(lmp_date):

    data = load_pregnancy_data()

    week, days = calculate_pregnancy_week(lmp_date)

    trimester = get_trimester(week)

    due_date = calculate_due_date(lmp_date)

    print("\n========== Pregnancy Journey Tracker ==========\n")

    print(f"Current Week: {week}")
    print(f"Days Pregnant: {days}")
    print(f"Trimester: {trimester}")
    print(f"Expected Due Date: {due_date}")

    print("\n--------------------------------------")

    week_data = data["pregnancy_weeks"].get(str(week))

    if week_data:
        return f"""
               Pregnancy Journey Tracker

               Current Week:
               {week}

               Days Pregnant:
               {days}

               Trimester:
               {trimester}

               Expected Due Date:
               {due_date}

               Baby Size:
               {week_data["baby_size_comparison"]}

               Baby Development:
               {week_data["baby_development"]}

               Maternal Changes:
               {week_data["maternal_changes"]}


               Recommendations:

               {"\n".join(week_data["recommendations"])}


               Note:
               This is health information only, not a medical diagnosis.
               """
    else:

        return f"""
    Pregnancy Journey Tracker

    Current Week:
    {week}

    Days Pregnant:
    {days}

    Trimester:
    {trimester}

    Expected Due Date:
    {due_date}


    No detailed information available for this week.


    Note:
    This tracker provides health information only and is not a medical diagnosis.
    """