from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend.app.db_models.tracking import Tracking
from backend.app.db_models.chat import ChatMessage
from backend.app.db_models.insight import Insight
from backend.app.db_models.notification import Notification


# ============================================================
# 3-MONTH HISTORY
# ============================================================

def get_three_month_history(
    db: Session,
    user_id,
):
    """
    Collect all relevant user data from the last 90 days.

    This function only retrieves data.
    Pattern detection is handled separately by
    analyze_health_patterns().
    """

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=90)

    tracking_records = (
        db.query(Tracking)
        .filter(
            Tracking.user_id == user_id,
            Tracking.date >= start_date.date(),
        )
        .order_by(Tracking.date.asc())
        .all()
    )

    chat_messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == user_id,
            ChatMessage.created_at >= start_date,
        )
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    insights = (
        db.query(Insight)
        .filter(
            Insight.user_id == user_id,
            Insight.created_at >= start_date,
        )
        .order_by(Insight.created_at.asc())
        .all()
    )

    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.created_at >= start_date,
        )
        .order_by(Notification.created_at.asc())
        .all()
    )

    return {
        "period": {
            "from": start_date.date(),
            "to": now.date(),
        },
        "tracking": tracking_records,
        "chat_messages": chat_messages,
        "insights": insights,
        "notifications": notifications,
    }


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(value):
    """
    Safely normalize text for comparisons.
    """
    if not value:
        return ""

    return str(value).strip().lower()


def add_pattern(
    patterns,
    pattern_type,
    severity,
    title,
    message,
    evidence=None,
):
    """
    Add a detected pattern to the result.
    """

    patterns.append(
        {
            "type": pattern_type,
            "severity": severity,
            "title": title,
            "message": message,
            "evidence": evidence or [],
        }
    )


# ============================================================
# CYCLE PATTERN DETECTION
# ============================================================

def analyze_cycle_patterns(tracking_records, patterns):
    """
    Detect abnormal or changing menstrual cycle patterns.

    Based on cycle_day and period_started information
    available in Tracking records.
    """

    records = [
        record
        for record in tracking_records
        if record.cycle_day is not None
    ]

    if not records:
        return

    # --------------------------------------------------------
    # Detect unusually high cycle days
    # --------------------------------------------------------

    high_cycle_records = [
        record
        for record in records
        if record.cycle_day > 35
    ]

    if len(high_cycle_records) >= 2:

        add_pattern(
            patterns=patterns,
            pattern_type="irregular_cycle",
            severity="moderate",
            title="Recurring irregular cycle pattern",
            message=(
                "Your records show repeated cycle days above "
                "the typical 21–35 day range."
            ),
            evidence=[
                f"{len(high_cycle_records)} records with cycle day above 35"
            ],
        )

    # --------------------------------------------------------
    # Detect unusually long cycle progression
    # --------------------------------------------------------

    very_high_cycle_records = [
        record
        for record in records
        if record.cycle_day > 45
    ]

    if very_high_cycle_records:

        add_pattern(
            patterns=patterns,
            pattern_type="long_cycle",
            severity="concerning",
            title="Extended cycle pattern",
            message=(
                "An extended menstrual cycle pattern was observed "
                "in your recent records."
            ),
            evidence=[
                f"{len(very_high_cycle_records)} records above 45 cycle days"
            ],
        )


# ============================================================
# PERIOD DURATION DETECTION
# ============================================================

def analyze_period_patterns(tracking_records, patterns):
    """
    Analyze period_started entries.

    The current Tracking model stores period_started as a string,
    so this detector focuses on repeated period-related records
    rather than assuming missing data means a medical abnormality.
    """

    period_records = [
        record
        for record in tracking_records
        if record.period_started
    ]

    if not period_records:
        return

    # Count recorded period dates
    period_dates = []

    for record in period_records: # cv

        try:
            date_value = str(record.period_started).strip().lower()

            if date_value == "yes":
                period_dates.append(record.date)
                continue

            if date_value == "no":
                continue

            parsed_date = datetime.strptime(
                date_value,
                "%Y-%m-%d",
            ).date()

            period_dates.append(parsed_date)

        except (ValueError, TypeError):
            # Ignore values that are not valid dates.
            continue

    if len(period_dates) < 2:
        return

    period_dates.sort()

    # Calculate gaps between recorded period starts.
    gaps = []

    for i in range(1, len(period_dates)):
        gap = (period_dates[i] - period_dates[i - 1]).days

        if gap > 0:
            gaps.append(gap)

    if not gaps:
        return

    irregular_gaps = [
        gap
        for gap in gaps
        if gap < 21 or gap > 35
    ]

    if len(irregular_gaps) >= 2:

        add_pattern(
            patterns=patterns,
            pattern_type="irregular_period_interval",
            severity="moderate",
            title="Irregular period interval pattern",
            message=(
                "Multiple period intervals in your records fall "
                "outside the typical 21–35 day range."
            ),
            evidence=[
                f"{len(irregular_gaps)} irregular intervals detected"
            ],
        )


# ============================================================
# SYMPTOM PATTERN DETECTION
# ============================================================

def analyze_symptom_patterns(tracking_records, patterns):
    """
    Detect recurring symptoms from Tracking.symptoms.

    This does NOT diagnose conditions.
    It only identifies repeated symptom mentions.
    """

    symptom_counter = Counter()

    for record in tracking_records:

        if not record.symptoms:
            continue

        raw_symptoms = str(record.symptoms).lower()

        # Allow common separators.
        normalized = (
            raw_symptoms
            .replace(";", ",")
            .replace("|", ",")
        )

        symptoms = [
            item.strip()
            for item in normalized.split(",")
            if item.strip()
        ]

        for symptom in symptoms:
            symptom_counter[symptom] += 1

    recurring = [
        (symptom, count)
        for symptom, count in symptom_counter.items()
        if count >= 2
    ]

    recurring.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    for symptom, count in recurring[:5]:

        add_pattern(
            patterns=patterns,
            pattern_type="recurring_symptom",
            severity="moderate",
            title="Recurring symptom detected",
            message=(
                f"The symptom '{symptom}' was recorded repeatedly "
                f"during the last three months."
            ),
            evidence=[
                f"Recorded {count} times"
            ],
        )


# ============================================================
# WEIGHT PATTERN DETECTION
# ============================================================

def analyze_weight_patterns(tracking_records, patterns):
    """
    Detect meaningful weight changes between available records.
    """

    weight_records = [
        record
        for record in tracking_records
        if record.weight is not None
    ]

    if len(weight_records) < 2:
        return

    weight_records.sort(
        key=lambda record: record.date
    )

    first_weight = weight_records[0].weight
    last_weight = weight_records[-1].weight

    if first_weight is None or last_weight is None:
        return

    change = last_weight - first_weight

    percentage_change = (
        abs(change) / first_weight * 100
        if first_weight != 0
        else 0
    )

    # Use a meaningful but conservative threshold.
    if percentage_change >= 5:

        direction = (
            "increase"
            if change > 0
            else "decrease"
        )

        add_pattern(
            patterns=patterns,
            pattern_type="weight_change",
            severity="moderate",
            title="Noticeable weight change",
            message=(
                f"A noticeable weight {direction} was recorded "
                "over the available three-month tracking period."
            ),
            evidence=[
                f"Initial weight: {first_weight}",
                f"Latest weight: {last_weight}",
                f"Change: {round(change, 2)}",
                f"Percentage change: {round(percentage_change, 1)}%",
            ],
        )


# ============================================================
# SLEEP PATTERN DETECTION
# ============================================================

def analyze_sleep_patterns(tracking_records, patterns):
    """
    Detect repeated low-sleep records.
    """

    sleep_records = [
        record
        for record in tracking_records
        if record.sleep_hours is not None
    ]

    if not sleep_records:
        return

    low_sleep = [
        record
        for record in sleep_records
        if record.sleep_hours < 6
    ]

    if len(low_sleep) >= 3:

        average_sleep = sum(
            record.sleep_hours
            for record in sleep_records
        ) / len(sleep_records)

        add_pattern(
            patterns=patterns,
            pattern_type="low_sleep",
            severity="moderate",
            title="Recurring low-sleep pattern",
            message=(
                "Repeated records show less than six hours "
                "of sleep."
            ),
            evidence=[
                f"{len(low_sleep)} low-sleep records",
                f"Average recorded sleep: {round(average_sleep, 1)} hours",
            ],
        )


# ============================================================
# MOOD PATTERN DETECTION
# ============================================================

def analyze_mood_patterns(tracking_records, patterns):
    """
    Detect repeated negative mood entries.

    This intentionally does not diagnose mental-health conditions.
    """

    mood_counter = Counter()

    negative_terms = {
        "bad",
        "sad",
        "low",
        "tired",
        "anxious",
        "anxiety",
        "stressed",
        "stress",
        "irritable",
        "irritated",
        "poor",
        "depressed",
        "unhappy",
        "exhausted",
    }

    for record in tracking_records:

        mood = normalize_text(record.mood)

        if not mood:
            continue

        for term in negative_terms:

            if term in mood:
                mood_counter[term] += 1

    recurring_moods = [
        (term, count)
        for term, count in mood_counter.items()
        if count >= 2
    ]

    recurring_moods.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    if recurring_moods:

        evidence = [
            f"{term}: {count} records"
            for term, count in recurring_moods[:5]
        ]

        add_pattern(
            patterns=patterns,
            pattern_type="recurring_mood_concern",
            severity="moderate",
            title="Recurring mood-related pattern",
            message=(
                "Repeated mood-related concerns were recorded "
                "during the last three months."
            ),
            evidence=evidence,
        )


# ============================================================
# CHAT PATTERN DETECTION
# ============================================================

def analyze_chat_patterns(chat_messages, patterns):
    """
    Identify recurring health concerns mentioned in conversations.

    This is intentionally simple and conservative.
    The LLM will later be used to summarize structured findings,
    rather than being responsible for detecting medical conditions.
    """

    if not chat_messages:
        return

    health_keywords = {
        "fatigue": [
            "tired",
            "fatigue",
            "exhausted",
            "low energy",
        ],
        "pain": [
            "pain",
            "cramp",
            "cramps",
            "ache",
        ],
        "bleeding": [
            "bleeding",
            "heavy bleeding",
            "spotting",
        ],
        "sleep": [
            "can't sleep",
            "cannot sleep",
            "insomnia",
            "poor sleep",
            "not sleeping",
        ],
        "cycle": [
            "irregular period",
            "irregular cycle",
            "late period",
            "missed period",
            "period late",
        ],
        "mood": [
            "anxious",
            "anxiety",
            "stressed",
            "stress",
            "sad",
            "low mood",
        ],
    }

    category_counter = Counter()

    for message in chat_messages:

        if normalize_text(message.role) != "user":
            continue

        content = normalize_text(message.content)

        if not content:
            continue

        for category, keywords in health_keywords.items():

            if any(keyword in content for keyword in keywords):
                category_counter[category] += 1

    recurring = [
        (category, count)
        for category, count in category_counter.items()
        if count >= 2
    ]

    recurring.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    for category, count in recurring:

        add_pattern(
            patterns=patterns,
            pattern_type="recurring_chat_concern",
            severity="moderate",
            title=f"Recurring {category} concern",
            message=(
                f"You mentioned {category}-related concerns "
                "multiple times in your conversations."
            ),
            evidence=[
                f"{count} user messages matched this concern"
            ],
        )


# ============================================================
# COMBINED PATTERN DETECTION
# ============================================================

def analyze_combined_patterns(
    tracking_records,
    chat_messages,
    patterns,
):
    """
    Detect patterns supported by more than one data source.

    These are stronger longitudinal signals because the same
    concern appears across different parts of the application.
    """

    # --------------------------------------------------------
    # Sleep + fatigue
    # --------------------------------------------------------

    low_sleep_count = sum(
        1
        for record in tracking_records
        if record.sleep_hours is not None
        and record.sleep_hours < 6
    )

    fatigue_mentions = 0

    for message in chat_messages:

        if normalize_text(message.role) != "user":
            continue

        content = normalize_text(message.content)

        if any(
            keyword in content
            for keyword in [
                "tired",
                "fatigue",
                "exhausted",
                "low energy",
            ]
        ):
            fatigue_mentions += 1

    if low_sleep_count >= 3 and fatigue_mentions >= 2:

        add_pattern(
            patterns=patterns,
            pattern_type="sleep_fatigue_pattern",
            severity="concerning",
            title="Recurring sleep and fatigue pattern",
            message=(
                "Your tracking records show repeated low sleep, "
                "and fatigue-related concerns were also mentioned "
                "repeatedly in your conversations."
            ),
            evidence=[
                f"{low_sleep_count} low-sleep tracking records",
                f"{fatigue_mentions} fatigue-related chat messages",
            ],
        )

    # --------------------------------------------------------
    # Cycle + recurring cramps
    # --------------------------------------------------------

    irregular_cycles = sum(
        1
        for record in tracking_records
        if record.cycle_day is not None
        and (
            record.cycle_day < 21
            or record.cycle_day > 35
        )
    )

    cramps = 0

    for record in tracking_records:

        symptoms = normalize_text(record.symptoms)

        if (
            "cramp" in symptoms
            or "pain" in symptoms
        ):
            cramps += 1

    if irregular_cycles >= 2 and cramps >= 2:

        add_pattern(
            patterns=patterns,
            pattern_type="cycle_symptom_pattern",
            severity="concerning",
            title="Recurring cycle and symptom pattern",
            message=(
                "Repeated cycle irregularities and recurring "
                "cramp or pain-related symptoms were observed "
                "in your tracking records."
            ),
            evidence=[
                f"{irregular_cycles} irregular cycle observations",
                f"{cramps} cramp/pain-related records",
            ],
        )


# ============================================================
# MAIN PATTERN ANALYZER
# ============================================================

def analyze_health_patterns(history):
    """
    Analyze the user's last three months of health data.

    Returns structured findings that can later be passed to
    an LLM for natural-language interpretation.
    """

    tracking_records = history.get(
        "tracking",
        [],
    )

    chat_messages = history.get(
        "chat_messages",
        [],
    )

    patterns = []

    # Run all detectors.
    analyze_cycle_patterns(
        tracking_records,
        patterns,
    )

    analyze_period_patterns(
        tracking_records,
        patterns,
    )

    analyze_symptom_patterns(
        tracking_records,
        patterns,
    )

    analyze_weight_patterns(
        tracking_records,
        patterns,
    )

    analyze_sleep_patterns(
        tracking_records,
        patterns,
    )

    analyze_mood_patterns(
        tracking_records,
        patterns,
    )

    analyze_chat_patterns(
        chat_messages,
        patterns,
    )

    analyze_combined_patterns(
        tracking_records,
        chat_messages,
        patterns,
    )

    # --------------------------------------------------------
    # Overall status
    # --------------------------------------------------------

    concerning_count = sum(
        1
        for pattern in patterns
        if pattern["severity"] == "concerning"
    )

    moderate_count = sum(
        1
        for pattern in patterns
        if pattern["severity"] == "moderate"
    )

    if concerning_count > 0:
        overall_status = "concerning_patterns_detected"

    elif moderate_count > 0:
        overall_status = "recurring_patterns_detected"

    else:
        overall_status = "no_significant_patterns_detected"

    return {
        "period": history.get("period"),
        "overall_status": overall_status,
        "pattern_count": len(patterns),
        "patterns_detected": patterns,
    }