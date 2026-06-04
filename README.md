# 📱 WhatsApp Chat Advanced Analyzer

An end-to-end Data Science and Analytics web application built using Python and Streamlit to analyze WhatsApp chat exports. This app provides deep insights into chat behaviors, active timelines, vocabulary statistics, sentiment patterns, and emoji distributions for both overall group metrics and individual user dynamics.

🚀 **Live App Link:** [https://whatsapp-chat-analyzer-madebymauryaji.streamlit.app/]

---

## ✨ Features

### 1. 📊 Top Core Statistics
* **Total Message Counter:** Total number of messages processed in the chat timeline.
* **Total Word Extraction:** Comprehensive count of all parsed lexical tokens.
* **Media Tracking:** Tracks shared media counts (`<Media omitted>`).
* **Link Scraper:** Identifies and counts unique URLs and hyperlinks shared within conversations.

### 2. 🎭 Sentiment Analysis (Chat Mood)
* Implements natural language processing via NLTK's **VADER Sentiment Intensity Analyzer**.
* Breaks down chat patterns into precise **Positive**, **Negative**, and **Neutral** percentage metrics.
* Visualizes collective emotional profiles via clean interactive **Pie Charts**.

### 3. ⏳ Timelines & Trends
* **Monthly Activity:** Chronological historical graphs charting message frequency over months and years.
* **Daily Frequency Matrix:** Continuous linear line graphs monitoring daily message spikes.

### 4. 📅 Spatiotemporal Activity Maps
* Monitors structural variation across active weekdays and operational calendar months using structured bar graphs.
* Incorporates a comprehensive **Hourly Heatmap** (using Seaborn) to locate precise peak engagement windows during the 24-hour cycle.

### 5. 🏆 Top Active Users (Group Exclusive)
* Segregates communication logs to establish relative active tier lists for group participants.
* Features integrated dataframes displaying message distributions along with percentage contribution values.

### 6. ☁️ Vocabulary Exploration
* Generates an dynamic **Word Cloud** filtering out common stop words to display frequently used terms.
* Identifies and displays the **Top 20 Most Common Words** using a horizontal frequency visualization layout.

### 7. 😂 Emoji Metrics
* Parses text strings using the specialized `emoji` catalog library to find used items.
* Maps emoji occurrences inside clean distribution tables along with descriptive tracking pie diagrams.

---

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3.x
* **Framework:** Streamlit (UI & Cloud Web Deployment Engine)
* **Data Engineering:** Pandas & NumPy
* **Data Visualization:** Matplotlib & Seaborn
* **Natural Language Processing:** NLTK (VADER Lexicon Package)
* **Text Analytics Tools:** WordCloud & Regular Expressions (`re`)
* **Core Tokenizer:** Emoji Framework

---

## 💻 Local Installation & Setup

If you want to run this project on your local workstation machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/jaymaurua456-lang/whatsapp-chat-analyzer.git](https://github.com/jaymaurua456-lang/whatsapp-chat-analyzer.git)
cd whatsapp-chat-analyzer
