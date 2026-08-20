import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 650;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💬 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Choose a WhatsApp chat file",
    type=["txt"]
)


# =========================================================
# IF FILE IS UPLOADED
# =========================================================

if uploaded_file is not None:

    try:

        # =================================================
        # READ FILE
        # =================================================

        bytes_data = uploaded_file.getvalue()

        try:

            data = bytes_data.decode("utf-8")

        except UnicodeDecodeError:

            data = bytes_data.decode(
                "utf-8",
                errors="ignore"
            )


        # =================================================
        # PREPROCESS DATA
        # =================================================

        df = preprocessor.preprocess(data)


        # =================================================
        # CHECK DATA
        # =================================================

        if df.empty:

            st.error(
                "❌ No WhatsApp messages found."
            )

            st.info(
                "Please upload a valid WhatsApp exported .txt file."
            )

            st.stop()


        # =================================================
        # GET USERS
        # =================================================

        user_list = []

        for user in df["user"].dropna().unique():

            user = str(user).strip()

            # Skip empty users
            if user == "":
                continue

            # Skip system notifications
            if user.lower() == "group_notification":
                continue

            user_list.append(user)


        # Remove duplicate names
        user_list = list(
            dict.fromkeys(user_list)
        )


        # Sort users alphabetically
        user_list.sort(
            key=lambda x: x.lower()
        )


        # Add Overall at first
        user_list.insert(
            0,
            "Overall"
        )


        # =================================================
        # SIDEBAR USER SELECTION
        # =================================================

        st.sidebar.markdown(
            "---"
        )

        selected_user = st.sidebar.selectbox(
            "👤 Show analysis for",
            user_list
        )


        # =================================================
        # DEBUG INFORMATION
        # =================================================

        with st.sidebar.expander(
            "🔍 User Information"
        ):

            st.write(
                "Total participants:",
                len(user_list) - 1
            )

            st.write(
                "Participants:"
            )

            st.write(
                user_list[1:]
            )


        # =================================================
        # SHOW ANALYSIS BUTTON
        # =================================================

        show_analysis = st.sidebar.button(
            "📊 Show Analysis",
            use_container_width=True
        )


        # =================================================
        # ANALYSIS
        # =================================================

        if show_analysis:

            # =================================================
            # TOP STATISTICS
            # =================================================

            (
                num_messages,
                words,
                num_media_messages,
                num_links
            ) = helper.fetch_stats(
                selected_user,
                df
            )


            st.markdown(
                '<div class="main-title">📊 Top Statistics</div>',
                unsafe_allow_html=True
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "💬 Total Messages",
                    num_messages
                )


            with col2:

                st.metric(
                    "📝 Total Words",
                    words
                )


            with col3:

                st.metric(
                    "📷 Media Shared",
                    num_media_messages
                )


            with col4:

                st.metric(
                    "🔗 Links Shared",
                    num_links
                )


            # =================================================
            # MONTHLY TIMELINE
            # =================================================

            st.markdown(
                '<div class="section-title">📅 Monthly Timeline</div>',
                unsafe_allow_html=True
            )


            timeline = helper.monthly_timeline(
                selected_user,
                df
            )


            if not timeline.empty:

                fig, ax = plt.subplots(
                    figsize=(12, 5)
                )

                ax.plot(
                    timeline["time"],
                    timeline["message"],
                    marker="o"
                )

                ax.set_xlabel(
                    "Month"
                )

                ax.set_ylabel(
                    "Messages"
                )

                plt.xticks(
                    rotation=45,
                    ha="right"
                )

                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)

            else:

                st.info(
                    "No monthly timeline data available."
                )


            # =================================================
            # DAILY TIMELINE
            # =================================================

            st.markdown(
                '<div class="section-title">📆 Daily Timeline</div>',
                unsafe_allow_html=True
            )


            daily_timeline = helper.daily_timeline(
                selected_user,
                df
            )


            if not daily_timeline.empty:

                fig, ax = plt.subplots(
                    figsize=(12, 5)
                )

                ax.plot(
                    daily_timeline["only_date"],
                    daily_timeline["message"]
                )

                ax.set_xlabel(
                    "Date"
                )

                ax.set_ylabel(
                    "Messages"
                )

                plt.xticks(
                    rotation=45,
                    ha="right"
                )

                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)

            else:

                st.info(
                    "No daily timeline data available."
                )


            # =================================================
            # ACTIVITY MAP
            # =================================================

            st.markdown(
                '<div class="section-title">🔥 Activity Map</div>',
                unsafe_allow_html=True
            )


            col1, col2 = st.columns(2)


            # -------------------------------------------------
            # BUSIEST DAY
            # -------------------------------------------------

            with col1:

                st.subheader(
                    "📅 Most Busy Day"
                )


                busy_day = helper.week_activity_map(
                    selected_user,
                    df
                )


                fig, ax = plt.subplots(
                    figsize=(8, 5)
                )


                ax.bar(
                    busy_day.index,
                    busy_day.values
                )


                ax.set_xlabel(
                    "Day"
                )

                ax.set_ylabel(
                    "Messages"
                )


                plt.xticks(
                    rotation=45,
                    ha="right"
                )

                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)


            # -------------------------------------------------
            # BUSIEST MONTH
            # -------------------------------------------------

            with col2:

                st.subheader(
                    "📆 Most Busy Month"
                )


                busy_month = helper.month_activity_map(
                    selected_user,
                    df
                )


                fig, ax = plt.subplots(
                    figsize=(8, 5)
                )


                ax.bar(
                    busy_month.index,
                    busy_month.values
                )


                ax.set_xlabel(
                    "Month"
                )

                ax.set_ylabel(
                    "Messages"
                )


                plt.xticks(
                    rotation=45,
                    ha="right"
                )

                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)


            # =================================================
            # WEEKLY ACTIVITY MAP
            # =================================================

            st.markdown(
                '<div class="section-title">🗓️ Weekly Activity Map</div>',
                unsafe_allow_html=True
            )


            user_heatmap = helper.activity_heatmap(
                selected_user,
                df
            )


            if not user_heatmap.empty:

                fig, ax = plt.subplots(
                    figsize=(15, 6)
                )


                sns.heatmap(
                    user_heatmap,
                    annot=True,
                    fmt="g",
                    ax=ax
                )


                ax.set_xlabel(
                    "Time Period"
                )

                ax.set_ylabel(
                    "Day"
                )


                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)

            else:

                st.info(
                    "No weekly activity data available."
                )


            # =================================================
            # MOST BUSY USERS
            # =================================================

            if selected_user == "Overall":

                st.markdown(
                    '<div class="section-title">👥 Most Busy Users</div>',
                    unsafe_allow_html=True
                )


                x, new_df = helper.most_busy_users(
                    df
                )


                col1, col2 = st.columns(2)


                # -------------------------------------------------
                # CHART
                # -------------------------------------------------

                with col1:

                    if not x.empty:

                        fig, ax = plt.subplots(
                            figsize=(9, 6)
                        )


                        ax.bar(
                            x.index,
                            x.values
                        )


                        ax.set_xlabel(
                            "Users"
                        )

                        ax.set_ylabel(
                            "Messages"
                        )


                        plt.xticks(
                            rotation=45,
                            ha="right"
                        )


                        plt.tight_layout()

                        st.pyplot(fig)

                        plt.close(fig)

                    else:

                        st.warning(
                            "No user data available."
                        )


                # -------------------------------------------------
                # TABLE
                # -------------------------------------------------

                with col2:

                    if not new_df.empty:

                        st.dataframe(
                            new_df,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.warning(
                            "No user percentage data available."
                        )


            # =================================================
            # WORD CLOUD
            # =================================================

            st.markdown(
                '<div class="section-title">☁️ Word Cloud</div>',
                unsafe_allow_html=True
            )


            df_wc = helper.create_wordcloud(
                selected_user,
                df
            )


            fig, ax = plt.subplots(
                figsize=(14, 7)
            )


            ax.imshow(
                df_wc,
                interpolation="bilinear"
            )


            ax.axis("off")


            st.pyplot(fig)

            plt.close(fig)


            # =================================================
            # MOST COMMON WORDS
            # =================================================

            st.markdown(
                '<div class="section-title">📝 Most Common Words</div>',
                unsafe_allow_html=True
            )


            most_common_df = helper.most_common_words(
                selected_user,
                df
            )


            if not most_common_df.empty:

                fig, ax = plt.subplots(
                    figsize=(11, 7)
                )


                ax.barh(
                    most_common_df["word"],
                    most_common_df["count"]
                )


                ax.set_xlabel(
                    "Frequency"
                )

                ax.set_ylabel(
                    "Words"
                )


                ax.invert_yaxis()


                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)


            else:

                st.info(
                    "No common words available."
                )


            # =================================================
            # EMOJI ANALYSIS
            # =================================================

            st.markdown(
                '<div class="section-title">😀 Emoji Analysis</div>',
                unsafe_allow_html=True
            )


            emoji_df = helper.emoji_helper(
                selected_user,
                df
            )


            col1, col2 = st.columns(2)


            # -------------------------------------------------
            # EMOJI TABLE
            # -------------------------------------------------

            with col1:

                if not emoji_df.empty:

                    st.dataframe(
                        emoji_df,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No emojis found."
                    )


            # -------------------------------------------------
            # EMOJI PIE CHART
            # -------------------------------------------------

            with col2:

                if not emoji_df.empty:

                    top_emojis = emoji_df.head(
                        10
                    )


                    fig, ax = plt.subplots(
                        figsize=(7, 7)
                    )


                    ax.pie(
                        top_emojis["count"],
                        labels=top_emojis["emoji"],
                        autopct="%0.1f%%"
                    )


                    st.pyplot(fig)

                    plt.close(fig)

                else:

                    st.info(
                        "No emoji data available."
                    )


    except Exception as e:

        st.error(
            "❌ Something went wrong while analyzing the chat."
        )

        st.exception(e)


# =========================================================
# NO FILE UPLOADED
# =========================================================

else:

    st.markdown(
        '<div class="main-title">💬 WhatsApp Chat Analyzer</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload your WhatsApp exported chat file "
        "from the sidebar to start analysis."
    )

    st.info(
        "📌 Export your WhatsApp chat as a `.txt` file "
        "and upload it here."
    )