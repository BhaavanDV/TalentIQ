# TalentIQ

🧠 TalentIQ: AI-Powered Resume Relevance System
An intelligent resume screening tool that automates the candidate shortlisting process by analyzing and ranking resumes based on their relevance to a specific job description. TalentIQ helps recruiters and HR professionals streamline their workflow, save valuable time, and make data-driven hiring decisions.

🌟 Features
📝 Job Description Input: Easily paste or type a job description to be used as the benchmark for relevance.

📄 Resume Upload: Upload single or multiple resumes in various formats (PDF, DOCX) for analysis.

📊 Relevance Scoring: Get a percentage-based relevance score for each resume, indicating how well it matches the job description.

📉 Ranked Results: View a list of candidates sorted by their relevance score in descending order.

💾 CSV Export: Download the results (including candidate name, score, and key skills) as a CSV file for easy record-keeping.

⚙️ Technology Stack: Built with Python, NLP techniques, and a user-friendly web interface using Streamlit.

💡 How It Works
TalentIQ uses a robust NLP pipeline to achieve its accuracy. The core process involves:

Text Extraction: The system uses libraries like PyPDF2 and python-docx to extract raw text from PDF and DOCX resume files.

Preprocessing: The text from both the resumes and the job description is cleaned and preprocessed (e.g., converted to lowercase, special characters removed).

Vectorization: The processed text is converted into numerical vectors using a technique like TF-IDF (Term Frequency-Inverse Document Frequency). This method assigns a numerical weight to each word, representing its importance in a document.

Similarity Calculation: The Cosine Similarity algorithm is used to calculate the similarity score between each resume's vector and the job description's vector. A higher cosine similarity score indicates a closer match.

Ranking: Finally, the resumes are ranked and displayed in a user-friendly interface based on their calculated scores.

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
You need to have Python installed on your system. It's recommended to use a virtual environment.

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate


Clone the repository:

git clone https://github.com/BhaavanDV/TalentIQ.git
cd TalentIQ

Install dependencies:
pip install -r requirements.txt
Note: The requirements.txt file must contain all the project's dependencies, such as streamlit, scikit-learn, PyPDF2, python-docx, etc.

Running the App
Once all dependencies are installed, you can launch the application from your terminal:

streamlit run app.py
This will start a local server and automatically open the application in your web browser.


📜 License
This project is licensed under the MIT License - see the LICENSE.md file for details.


