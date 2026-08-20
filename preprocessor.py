import re
import pandas as pd


def preprocess(data):

    # =====================================================
    # WHATSAPP MESSAGE PATTERNS
    # =====================================================

    # Example:
    # 12/08/25, 10:30 pm - Shreyansh: Hello
    #
    # 12/08/2025, 10:30 - Shreyansh: Hello
    #
    # 12/08/25, 10:30 PM - Shreyansh: Hello

    pattern = re.compile(
        r"^(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
        r",?\s+"
        r"(\d{1,2}:\d{2}(?::\d{2})?"
        r"(?:\s?[AaPp][Mm])?)"
        r"\s*[-–]\s*"
        r"(.*)$"
    )

    dates = []
    times = []
    messages = []

    current_date = None
    current_time = None
    current_message = None

    # =====================================================
    # READ CHAT LINE BY LINE
    # =====================================================

    for line in data.splitlines():

        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)

        # -------------------------------------------------
        # NEW MESSAGE
        # -------------------------------------------------

        if match:

            # Save previous message
            if current_message is not None:

                dates.append(current_date)
                times.append(current_time)
                messages.append(current_message)

            current_date = match.group(1)
            current_time = match.group(2)
            current_message = match.group(3)

        # -------------------------------------------------
        # MULTI-LINE MESSAGE
        # -------------------------------------------------

        else:

            if current_message is not None:

                current_message += " " + line

    # =====================================================
    # SAVE LAST MESSAGE
    # =====================================================

    if current_message is not None:

        dates.append(current_date)
        times.append(current_time)
        messages.append(current_message)

    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    df = pd.DataFrame({

        "date": dates,

        "time": times,

        "message": messages

    })

    if df.empty:

        return df

    # =====================================================
    # EXTRACT USER NAME
    # =====================================================

    users = []
    actual_messages = []

    for message in df["message"]:

        message = str(message)

        # -------------------------------------------------
        # NORMAL USER MESSAGE
        # -------------------------------------------------
        #
        # Example:
        # Shreyansh: Hello
        #
        # Shreyansh: Hello bro
        #
        # We allow zero or more spaces after :
        # -------------------------------------------------

        user_match = re.match(
            r"^([^:]+):\s*(.*)$",
            message
        )

        if user_match:

            user = user_match.group(1).strip()

            msg = user_match.group(2).strip()

            # Clean some common prefixes
            user = user.replace(
                "\u200e",
                ""
            ).strip()

            users.append(user)

            actual_messages.append(msg)

        else:

            # -------------------------------------------------
            # GROUP / SYSTEM NOTIFICATION
            # -------------------------------------------------

            users.append(
                "group_notification"
            )

            actual_messages.append(
                message
            )

    # =====================================================
    # ADD USER COLUMN
    # =====================================================

    df["user"] = users

    df["message"] = actual_messages

    # =====================================================
    # DATE CONVERSION
    # =====================================================

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    # =====================================================
    # DATETIME
    # =====================================================

    df["datetime"] = pd.to_datetime(
        df["date"].dt.strftime(
            "%d/%m/%Y"
        )
        + " "
        + df["time"].astype(str),
        dayfirst=True,
        errors="coerce"
    )

    # =====================================================
    # REMOVE INVALID ROWS
    # =====================================================

    df = df.dropna(
        subset=["datetime"]
    )

    if df.empty:

        return df

    # =====================================================
    # DATE FEATURES
    # =====================================================

    df["year"] = df["datetime"].dt.year

    df["month_num"] = df["datetime"].dt.month

    df["month"] = (
        df["datetime"]
        .dt.month_name()
    )

    df["day"] = (
        df["datetime"]
        .dt.day
    )

    df["day_name"] = (
        df["datetime"]
        .dt.day_name()
    )

    df["hour"] = (
        df["datetime"]
        .dt.hour
    )

    df["minute"] = (
        df["datetime"]
        .dt.minute
    )

    # =====================================================
    # ONLY DATE
    # =====================================================

    df["only_date"] = (
        df["datetime"]
        .dt.date
    )

    # =====================================================
    # TIME PERIOD
    # =====================================================

    def period(hour):

        if hour == 23:

            return "23-00"

        return f"{hour:02d}-{hour + 1:02d}"

    df["period"] = (
        df["hour"]
        .apply(period)
    )

    # =====================================================
    # RESET INDEX
    # =====================================================

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df