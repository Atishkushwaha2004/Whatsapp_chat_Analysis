📱 WhatsApp Chat Analysis

A Python-based WhatsApp Chat Analysis project that analyzes exported WhatsApp conversations and provides useful insights such as message statistics, user activity, timelines, word usage, and communication patterns.

🚀 Features
📊 Total messages analysis
👥 User-wise message statistics
📅 Date-wise and monthly activity analysis
⏰ Most active hours
📈 Daily/Monthly message trends
🔤 Most frequently used words
😂 Emoji analysis
🔗 URL/link analysis
🗣️ User activity comparison
📊 Interactive data visualizations
📱 Simple web interface using Streamlit
🛠️ Technologies Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Streamlit
URLExtract
Regular Expressions
📂 Project Structure
Whatsapp_Chat_Analysis/
│
├── app.py
├── helper.py
├── preprocessor.py
├── requirements.txt
├── README.md
│
├── __pycache__/
│
└── whatsapp_chat_data.pkl


__pycache__/ is ignored using .gitignore and should not be uploaded to GitHub.

📋 Dataset

The project works with a WhatsApp exported chat file.

To export a WhatsApp chat:

Open WhatsApp.
Open the required chat/group.
Click on the three dots.
Select More → Export chat.
Choose Without Media.
Save the exported .txt file.
Upload/use the file in the application.
⚙️ Installation

Clone the repository:

git clone https://github.com/Atishkushwaha2004/Whatsapp_Chat_Analysis.git


Go to the project directory:

cd Whatsapp_Chat_Analysis


Create a virtual environment:

python -m venv venv


Activate it on Windows:

venv\Scripts\activate


Install the required libraries:

pip install -r requirements.txt

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py


The application will open in your browser.

📊 Analysis Performed
1. Overall Statistics

The application calculates:

Total messages
Total words
Total media messages
Total links shared
2. User Analysis

For group chats, the project analyzes:

Messages sent by each user
Most active users
User contribution percentage
3. Timeline Analysis

The project provides:

Monthly timeline
Daily timeline
Activity trends
Most active dates
4. Activity Analysis

It identifies:

Most active days
Most active months
Most active hours
Weekly activity patterns
5. Word Analysis

The project analyzes frequently used words and helps identify common communication patterns.

6. Emoji Analysis

The application extracts emojis and displays:

Most frequently used emojis
Emoji frequency
User-wise emoji usage
📸 Project Preview

Add screenshots of your application here:

![WhatsApp Chat Analysis](screenshots/dashboard.png)<img width="1906" height="1025" alt="Screenshot 2026-08-20 212058" src="https://github.com/user-attachments/assets/301c286f-5ff5-4441-86bc-6d8cc3630729" />


🎯 Future Improvements
Sentiment analysis
Word cloud generation
Advanced NLP analysis
Chat comparison between users
AI-powered conversation insights
Deployment using Streamlit Cloud
Improved interactive visualizations
👨‍💻 Author

Atish Kushwaha

B.Tech – Electronics & Communication Engineering

Connect With Me
GitHub: [Atishkushwaha2004   ](https://github.com/Atishkushwaha2004)                                                                             
LinkedIn: linkedin.com/in/atish-kushwaha-25a907268
⭐ Show Your Support

If you found this project useful, consider giving it a ⭐ on GitHub.
