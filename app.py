import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer - Advanced Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📱 WhatsApp Chat Advanced Analyzer")

# Sidebar Configuration Layout
st.sidebar.title("📁 Upload & Configure")
uploaded_file = st.sidebar.file_uploader("Choose WhatsApp Chat File (.txt)", type=["txt"])

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocess.preprocess(data)
    
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall Group Stats")
    
    selected_user = st.sidebar.selectbox("Show Analysis For:", user_list)
    
    if st.sidebar.button("Show Analysis"):
        st.success(f"Displaying Insights for: {selected_user} ✅")
        
        # ==========================================
        # 1. CORE STATS METRICS
        # ==========================================
        st.markdown("### 📊 Top Statistics")
        num_messages, total_words, media_count, links_array = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", total_words)
        with col3:
            st.metric("Media Omitted", media_count)
        with col4:
            st.metric("Links Shared", len(links_array))
            
        # ==========================================
        # 2. CHAT MOOD (SENTIMENT ANALYSIS)
        # ==========================================
        st.markdown("---")
        st.markdown("### 🎭 Sentiment Analysis (Chat Mood)")
        pos, neg, neu = helper.analyze_sentiment(selected_user, df)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**Positive Sentiment:** `{pos}%`")
            st.write(f"**Negative Sentiment:** `{neg}%`")
            st.write(f"**Neutral Sentiment:** `{neu}%`")
        with col2:
            if pos or neg or neu:
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.pie([pos, neg, neu], labels=['Positive', 'Negative', 'Neutral'], colors=['#25D366', '#E57373', '#34B7F1'], autopct='%1.1f%%', startangle=90)
                st.pyplot(fig)
            else:
                st.info("No text records found to process sentiment profiles.")

        # ==========================================
        # 3. DYNAMIC TREND TIMELINES
        # ==========================================
        st.markdown("---")
        st.markdown("### ⏳ Timelines & Trends")
        
        st.markdown("##### Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.plot(timeline['time'], timeline['message'], color='#25D366', marker='o', linewidth=2)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.markdown("##### Daily Timeline")
        d_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.plot(d_timeline['only_date'], d_timeline['message'], color='#34B7F1', linewidth=1.5)
        st.pyplot(fig)
        
        # ==========================================
        # 4. TEMPORAL ACTIVITY DATA
        # ==========================================
        st.markdown("---")
        st.markdown("### 📅 Activity Maps")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Most Active Days")
            busy_day = helper.daily_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#8E44AD')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.markdown("##### Most Active Months")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#E67E22')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        st.markdown("##### Hourly Activity Heatmap")
        try:
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(14, 6))
            sns.heatmap(user_heatmap, cmap="viridis", ax=ax, cbar_kws={'label': 'Message Frequency'})
            st.pyplot(fig)
        except Exception as e:
            st.info("Not enough variations in log timestamps to draw active coordinate arrays.")

        # ==========================================
        # 5. USER METRIC TIERS (ONLY FOR OVERALL CHAT)
        # ==========================================
        if selected_user == 'Overall Group Stats':
            st.markdown("---")
            st.markdown("### 🏆 Top 10 Active Users")
            x = df[df['user'] != 'group_notification']['user'].value_counts().head(10)
            
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='#2ECC71')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                percent_df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'count':'Percentage', 'user':'Name'})
                st.dataframe(percent_df.head(10), use_container_width=True)

        # ==========================================
        # 6. WORD CLOUDS AND KEYWORD TOKENS
        # ==========================================
        st.markdown("---")
        st.markdown("### ☁️ Vocabulary Exploration")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Word Cloud")
            try:
                wc = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(wc)
                ax.axis("off")
                st.pyplot(fig)
            except:
                st.info("Not enough clean contextual terms parsed to generate structural wordcloud diagrams.")
                
        with col2:
            st.markdown("##### Top 20 Common Words")
            common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(common_df['Word'], common_df['Frequency'], color='#3498DB')
            plt.gca().invert_yaxis()
            st.pyplot(fig)

        # ==========================================
        # 7. EMOJI DATA METRICS
        # ==========================================
        st.markdown("---")
        st.markdown("### 😂 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(emoji_df, use_container_width=True)
        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots(figsize=(5,5))
                ax.pie(emoji_df['Count'].head(5), labels=emoji_df['Emoji'].head(5), autopct="%0.2f%%")
                st.pyplot(fig)
            else:
                st.info("No standard emojis detected in target subset strings.")

        # ==========================================
        # 8. WORKSPACE CONTEXT LOGGER PREVIEW
        # ==========================================
        st.markdown("---")
        st.markdown("### 📄 Chat Dataset Preview")
        st.dataframe(df, use_container_width=True)