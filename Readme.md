# 🚀 Introducing MailSensei
## Your Cutting-Edge Email Management Companion 📧✂️

<!-- <img  src="https://i.ibb.co/Bg6h8qp/your-image.png"  alt="MailSensei Image"> -->
<!-- ![Image](./PeerlistHackathon_CoverImg.png) -->


![Cover Image](https://raw.githubusercontent.com/Deven1902/Peerlist-Hackathon/main/coverImg.png)

Tired of sifting through endless emails, only to discover they're not worth your time? Ever missed important messages due to email overload? In today's digital age, our inboxes are overflowing with both vital and distracting content. You might spend precious time on lengthy, irrelevant emails. MailSensei is here to revolutionize your email experience by addressing these challenges. 🚀

### Need for a Solution 🤔

![Email Overload](https://media.giphy.com/media/OothRHNJSCaTS/giphy.gif)

CEOs and business professionals often receive hundreds of emails daily, making efficient email management essential. MailSensei offers a solution to navigate this email overload, ensuring that crucial messages are never missed and time is spent more productively. 🕒💼

### How to run the project 🌟
- Visit the following URL to locate the project:- **[https://replit.com/@DevenNandapurka/Peerlist-Hackathon](https://replit.com/@DevenNandapurka/Peerlist-Hackathon)**

- You will see the replit workspace. Click the `Run` button. 

- You need to setup an **App Password** before you can set credentails for MailSensei. 
Here we have attached an article to guide you through setting up an app password -> **[Generate your App Password](https://support.google.com/mail/answer/185833?hl=en)**

- Once the project is up and running, enter your credentials in the project and click the `Set Credentials` button. 

- Click the `Fetch Emails` button -> and all of your unread emails will be fetched and rendered in a short summary format. 

### Our Unique Approach 🌟

- **Gmail Credentials Setup:** Securely collect your "Gmail Address" and "App Password" via Streamlit to maintain the confidentiality of your email data. 🔒

- **IMAP Connection:** Establish a connection to your Gmail account using IMAP (Internet Message Access Protocol) for seamless email access. 🌐

- **Email Decoding:** Decode your emails to extract essential information, including "From," "Subject," and email content. 📤

- **Email Summarization:** Utilize Large Language Models (LLMs), specifically "distilbart-cnn-12-6," to generate concise summaries of your emails, saving you valuable time. 📝⏳

- **Tag Generation:** Intelligently categorize and organize emails using "t5-base-tag-generation." Tags are displayed alongside email details. 🏷️

- **Streamlined Presentation:** Display email information in an ordered format, including "From," "Subject," and associated tags for easy reference. 📊

- **Dropdown Summaries:** Provide a dropdown button for each email, allowing users to access the summary with a single click, enhancing readability. 📑

- **Original Email Link:** Include a convenient link at the end of each summary that directs users to the original email for further context and action. 🔗

### Technology Stack 🛠️

- **Programming Languages:** Python
- **Web Framework:** Streamlit
- **Machine Learning Framework:** PyTorch
- **Email Access:** IMAP (Internet Message Access Protocol)
- **Text Processing:** Transformers library (from Hugging Face)
- **Logging:** Python Logging Library

### Models Used 🧠

1. **Large Language Model (LLM) for Summarization:**
   - **Model:** `sshleifer/distilbart-cnn-12-6` (DistilBART)
   - **Purpose:** Summarizes email content to generate concise summaries.
   - **Utilized for:** Email summarization.

2. **Spam Detection Model(Currently commented out as results are not accurate) :**
   - **Model:** `1aurent/distilbert-base-multilingual-cased-finetuned-email-spam` (DistilBERT)
   - **Purpose:** Detects spam emails within the inbox.
   - **Utilized for:** Spam filtering.

3. **Tag Generation Model:**
   - **Model:** `fabiochiu/t5-base-tag-generation` (T5)
   - **Purpose:** Generates tags to categorize and organize emails.
   - **Utilized for:** Email tagging and categorization.


### Running locally:
Requirements:
- Python 3.7+
- cuda (optional for GPU support)
- Minimum 4GB RAM is required to run the app

clone the repository:
```bash
git clone https://github.com/Deven1902/Peerlist-Hackathon
```
optionally create a virtual environment:
```bash
python -m venv venv
```
activate the virtual environment:

for Linux
```bash
source venv/bin/activate
```

for Windows
```bash
venv\Scripts\activate
```

install requirements using pip:
```bash
pip install -r requirements.txt
```

run the app:
```bash
streamlit run app/streamlit_app.py
```

### Future Enhancements 🚀🔮

- **Improved Spam Filtering:** We'll enhance the accuracy of our spam detection algorithm for a cleaner inbox. 🚮

- **Tag Collections & Sharing:** Users can create and share tag collections, streamlining collaboration and productivity. 🚀📊

- **Custom Tag Generation:** Customize your own tag generation models for tailored email organization. 🏷️

- **User Preferences:** Fine-tune MailSensei with preferences like summarization length and tag rules for a personalized experience. ⚙️👤


*"Initially, we used OpenAI keys for all our app functions. However, we later changed our approach as some users may not have premium keys, and we wanted to ensure accessibility without additional costs. 😉😊"*



