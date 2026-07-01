def menstrual_cycle_tracker(last_period, cycle_length, period_duration):

    from datetime import datetime, timedelta

    last_period_date = datetime.strptime(
        last_period,
        "%Y-%m-%d"
    )

    next_period = last_period_date + timedelta(days=int(cycle_length))

    today = datetime.today()

    cycle_day = (today - last_period_date).days + 1


    if cycle_day <= int(period_duration):
        phase = "Menstrual Phase"

    elif cycle_day <= 14:
        phase = "Follicular Phase"

    elif cycle_day <= 16:
        phase = "Ovulation Phase"

    else:
        phase = "Luteal Phase"


    if 21 <= int(cycle_length) <= 35:
        cycle_status = "Normal cycle length"
    else:
        cycle_status = "Cycle may be irregular"


    if int(period_duration) <= 7:
        period_status = "Normal period duration"
    else:
        period_status = "Long period duration"


    return f"""
Menstrual Cycle Analysis

Last Period:
{last_period}

Expected Next Period:
{next_period.date()}

Current Cycle Day:
{cycle_day}

Current Phase:
{phase}


Health Insights:

✓ {cycle_status}

✓ {period_status}


Note:
This tracker provides educational information only.
"""