import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import emoji


# =========================================================
# FILTER DATA
# =========================================================

def filter_data(selected_user, df):

    if selected_user == "Overall":

        return df.copy()

    return df[
        df["user"] == selected_user
    ].copy()


# =========================================================
# FETCH STATISTICS
# =========================================================

def fetch_stats(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )

    # -----------------------------------------------------
    # TOTAL MESSAGES
    # -----------------------------------------------------

    num_messages = len(
        temp_df
    )


    # -----------------------------------------------------
    # TOTAL WORDS
    # -----------------------------------------------------

    words = 0

    for message in temp_df["message"]:

        words += len(
            str(message).split()
        )


    # -----------------------------------------------------
    # MEDIA MESSAGES
    # -----------------------------------------------------

    media_patterns = [
        "<media omitted>",
        "<media omitted>",
        "image omitted",
        "video omitted",
        "audio omitted",
        "sticker omitted",
        "gif omitted"
    ]


    num_media_messages = 0


    for message in temp_df["message"]:

        message_lower = str(
            message
        ).lower()

        for pattern in media_patterns:

            if pattern in message_lower:

                num_media_messages += 1

                break


    # -----------------------------------------------------
    # LINKS
    # -----------------------------------------------------

    num_links = 0


    for message in temp_df["message"]:

        links = re.findall(
            r"https?://\S+|www\.\S+",
            str(message)
        )

        num_links += len(
            links
        )


    return (
        num_messages,
        words,
        num_media_messages,
        num_links
    )


# =========================================================
# MONTHLY TIMELINE
# =========================================================

def monthly_timeline(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    if temp_df.empty:

        return pd.DataFrame(
            columns=[
                "time",
                "message"
            ]
        )


    timeline = (
        temp_df
        .groupby(
            [
                "year",
                "month_num",
                "month"
            ]
        )
        .size()
        .reset_index(
            name="message"
        )
    )


    timeline["time"] = (
        timeline["month"]
        + "-"
        + timeline["year"].astype(str)
    )


    timeline["sort_key"] = (
        timeline["year"] * 100
        + timeline["month_num"]
    )


    timeline = timeline.sort_values(
        "sort_key"
    )


    return timeline[
        [
            "time",
            "message"
        ]
    ]


# =========================================================
# DAILY TIMELINE
# =========================================================

def daily_timeline(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    if temp_df.empty:

        return pd.DataFrame(
            columns=[
                "only_date",
                "message"
            ]
        )


    daily = (
        temp_df
        .groupby(
            "only_date"
        )
        .size()
        .reset_index(
            name="message"
        )
    )


    return daily


# =========================================================
# WEEK ACTIVITY MAP
# =========================================================

def week_activity_map(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]


    if temp_df.empty:

        return pd.Series(
            0,
            index=days_order
        )


    result = (
        temp_df["day_name"]
        .value_counts()
    )


    result = result.reindex(
        days_order,
        fill_value=0
    )


    return result


# =========================================================
# MONTH ACTIVITY MAP
# =========================================================

def month_activity_map(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    months_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]


    if temp_df.empty:

        return pd.Series(
            0,
            index=months_order
        )


    result = (
        temp_df["month"]
        .value_counts()
    )


    result = result.reindex(
        months_order,
        fill_value=0
    )


    return result


# =========================================================
# ACTIVITY HEATMAP
# =========================================================

def activity_heatmap(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    if temp_df.empty:

        return pd.DataFrame()


    heatmap = (
        temp_df
        .pivot_table(
            index="day_name",
            columns="period",
            values="message",
            aggfunc="count",
            fill_value=0
        )
    )


    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]


    heatmap = heatmap.reindex(
        days_order,
        fill_value=0
    )


    # -----------------------------------------------------
    # Sort Time Periods
    # -----------------------------------------------------

    def sort_period(period):

        try:

            return int(
                str(period)
                .split("-")[0]
            )

        except:

            return 0


    heatmap = heatmap[
        sorted(
            heatmap.columns,
            key=sort_period
        )
    ]


    return heatmap


# =========================================================
# MOST BUSY USERS
# =========================================================

def most_busy_users(df):

    # -----------------------------------------------------
    # COPY DATA
    # -----------------------------------------------------

    temp_df = df.copy()


    # -----------------------------------------------------
    # REMOVE SYSTEM MESSAGES
    # -----------------------------------------------------

    temp_df = temp_df[
        temp_df["user"].notna()
    ]


    temp_df = temp_df[
        temp_df["user"]
        .astype(str)
        .str.strip()
        != ""
    ]


    temp_df = temp_df[
        temp_df["user"]
        .astype(str)
        .str.lower()
        != "group_notification"
    ]


    # -----------------------------------------------------
    # IF NO USERS
    # -----------------------------------------------------

    if temp_df.empty:

        return (

            pd.Series(
                dtype="int64"
            ),

            pd.DataFrame(
                columns=[
                    "User",
                    "Messages",
                    "Percentage"
                ]
            )

        )


    # -----------------------------------------------------
    # MESSAGE COUNT PER USER
    # -----------------------------------------------------

    x = (
        temp_df["user"]
        .value_counts()
        .head(10)
    )


    # -----------------------------------------------------
    # PERCENTAGE
    # -----------------------------------------------------

    percentage = (
        temp_df["user"]
        .value_counts(
            normalize=True
        )
        .mul(100)
        .round(2)
        .head(10)
    )


    # -----------------------------------------------------
    # CREATE TABLE
    # -----------------------------------------------------

    new_df = pd.DataFrame({

        "User": percentage.index,

        "Messages": [
            x.get(
                user,
                0
            )
            for user in percentage.index
        ],

        "Percentage": percentage.values

    })


    return x, new_df


# =========================================================
# WORD CLOUD
# =========================================================

def create_wordcloud(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    if temp_df.empty:

        return WordCloud(
            width=1000,
            height=500,
            background_color="white"
        ).generate(
            "No Data"
        )


    # -----------------------------------------------------
    # REMOVE MEDIA
    # -----------------------------------------------------

    temp_df = temp_df[
        ~temp_df["message"]
        .astype(str)
        .str.contains(
            "<media omitted>",
            case=False,
            na=False
        )
    ]


    # -----------------------------------------------------
    # CREATE TEXT
    # -----------------------------------------------------

    text = " ".join(
        temp_df["message"]
        .astype(str)
    )


    if not text.strip():

        text = "No Data"


    # -----------------------------------------------------
    # WORD CLOUD
    # -----------------------------------------------------

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        min_font_size=10
    ).generate(
        text
    )


    return wc


# =========================================================
# MOST COMMON WORDS
# =========================================================

def most_common_words(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    words = []


    # -----------------------------------------------------
    # EXTRACT WORDS
    # -----------------------------------------------------

    for message in temp_df["message"]:

        message = str(
            message
        ).lower()


        # Remove URLs
        message = re.sub(
            r"https?://\S+|www\.\S+",
            "",
            message
        )


        # Remove punctuation
        message = re.sub(
            r"[^\w\s]",
            " ",
            message
        )


        words.extend(
            message.split()
        )


    # =====================================================
    # STOP WORDS
    # =====================================================

    stop_words = {

        # English
        "the",
        "to",
        "and",
        "a",
        "i",
        "of",
        "in",
        "is",
        "for",
        "on",
        "that",
        "it",
        "this",
        "was",
        "are",
        "you",
        "me",
        "my",
        "we",
        "be",
        "with",
        "have",
        "has",
        "had",
        "he",
        "she",
        "they",
        "them",
        "but",
        "or",
        "so",
        "if",
        "at",
        "as",
        "from",
        "your",
        "our",
        "just",
        "can",
        "will",
        "not",
        "no",
        "yes",
        "ok",
        "okay",

        # Hindi / Hinglish
        "hai",
        "hain",
        "ka",
        "ke",
        "ki",
        "ko",
        "me",
        "mein",
        "se",
        "mai",
        "main",
        "mujhe",
        "kya",
        "ye",
        "ya",
        "aur",
        "bhi",
        "toh",
        "nahi",
        "na",
        "ho",
        "tha",
        "the",
        "thi"
    }


    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    filtered_words = [

        word

        for word in words

        if word not in stop_words

        and len(word) > 2
    ]


    # -----------------------------------------------------
    # TOP 20 WORDS
    # -----------------------------------------------------

    most_common = (
        Counter(
            filtered_words
        )
        .most_common(20)
    )


    # IMPORTANT:
    # Named columns prevent KeyError
    # -----------------------------------------------------

    return pd.DataFrame(
        most_common,
        columns=[
            "word",
            "count"
        ]
    )


# =========================================================
# EMOJI ANALYSIS
# =========================================================

def emoji_helper(selected_user, df):

    temp_df = filter_data(
        selected_user,
        df
    )


    emojis = []


    # -----------------------------------------------------
    # EXTRACT EMOJIS
    # -----------------------------------------------------

    for message in temp_df["message"]:

        for character in str(message):

            if character in emoji.EMOJI_DATA:

                emojis.append(
                    character
                )


    # -----------------------------------------------------
    # COUNT
    # -----------------------------------------------------

    emoji_counter = Counter(
        emojis
    )


    # -----------------------------------------------------
    # DATAFRAME
    # -----------------------------------------------------

    return pd.DataFrame(
        emoji_counter.most_common(),
        columns=[
            "emoji",
            "count"
        ]
    )