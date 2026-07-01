# from datetime import datetime, timedelta
#
#
# def menstrual_cycle_tracker():
#
#     print("\n========== Menstrual Health Tracker ==========")
#
#     last_period = input("Enter your last period date (YYYY-MM-DD): ")
#     cycle_length = int(input("Enter your average cycle length (days): "))
#     period_duration = int(input("Enter your period duration (days): "))
#
#     # Convert date
#     last_period_date = datetime.strptime(last_period, "%Y-%m-%d")
#
#     # Calculate next period
#     next_period = last_period_date + timedelta(days=cycle_length)
#
#     # Calculate current cycle day
#     today = datetime.today()
#     cycle_day = (today - last_period_date).days + 1
#
#
#     # Determine phase
#     if cycle_day <= period_duration:
#         phase = "Menstrual Phase"
#     elif cycle_day <= 14:
#         phase = "Follicular Phase"
#     elif cycle_day <= 16:
#         phase = "Ovulation Phase"
#     else:
#         phase = "Luteal Phase"
#
#
#     # Health insights
#     print("\n========== Cycle Analysis ==========")
#
#     print(f"Last Period Date: {last_period_date.date()}")
#     print(f"Expected Next Period: {next_period.date()}")
#     print(f"Current Cycle Day: {cycle_day}")
#     print(f"Current Cycle Phase: {phase}")
#
#
#     print("\nHealth Insights:")
#
#     if 21 <= cycle_length <= 35:
#         print("✓ Your cycle length is within the normal range.")
#     else:
#         print("⚠ Your cycle length may be irregular. Consider tracking regularly.")
#
#     if period_duration <= 7:
#         print("✓ Period duration is within common range.")
#     else:
#         print("⚠ Longer periods may require medical consultation.")
#
#
#     print("\nNote: This tracker provides health information and is not a medical diagnosis.")

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