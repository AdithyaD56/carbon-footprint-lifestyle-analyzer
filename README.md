# 🌍 AI Carbon Footprint Studio

> Predict. Visualize. Improve.  
> An intelligent sustainability dashboard that helps users understand and reduce their carbon footprint through machine learning, interactive analytics, and AI-powered guidance.

AI Carbon Footprint Studio is an interactive Streamlit application that predicts a user's personal carbon emissions based on their lifestyle habits, visualizes the environmental impact across multiple time scales, allows users to simulate reduction strategies, and provides personalized sustainability recommendations using Groq AI.

The application combines data science, sustainability analytics, and generative AI to make environmental awareness more accessible, practical, and engaging.

---

# 🎯 Chosen Vertical

**Environmental Sustainability**

This project focuses on helping users understand the environmental impact of their everyday activities and encouraging more sustainable choices through predictive analytics and AI-generated guidance.

### Problems Addressed
- Most people do not know how much carbon they generate each month.
- Carbon footprint calculators are often difficult to understand and visually unappealing.
- Users rarely receive personalized suggestions tailored to their lifestyle.
- It is difficult to estimate how small changes in travel, shopping, or digital usage affect emissions.

### Solution

AI Carbon Footprint Studio solves these challenges by:
- Predicting monthly carbon emissions using a trained machine learning model
- Visualizing emissions across different categories and time scales
- Simulating reduction strategies through an interactive lab
- Generating personalized sustainability advice using Groq AI

---

# 🚀 Approach and Logic

The application follows a complete prediction-to-action workflow:

1. Collect user lifestyle inputs
2. Convert those inputs into the format expected by the trained ML pipeline
3. Predict the user's monthly carbon emissions
4. Visualize the emissions using multiple charts and comparisons
5. Allow the user to test reduction scenarios
6. Use Groq AI to generate practical sustainability guidance

### Machine Learning Logic
A trained machine learning pipeline (`pipeline.pkl` or `carbon_pipeline.pkl`) is used to estimate monthly carbon emissions based on the user's:

- Transportation habits
- Energy usage
- Screen time
- Shopping frequency
- Food preferences
- Waste generation

The model predicts the user's estimated monthly carbon footprint in kilograms of CO₂.

### AI Guidance Logic
After the prediction is generated, the app passes the emission values and lifestyle summary into Groq AI. The assistant then creates:

- A short diagnosis of the user's carbon habits
- The top recommendations for improvement
- A concise motivational conclusion

The recommendations are inspired by trusted public sustainability sources such as the EPA and IEA.

---

# ⚙️ How the Solution Works

### Step 1 — Lifestyle Input
The user enters personal details and lifestyle habits from the sidebar.

Input categories include:
- Transportation and travel distance
- Electricity and household energy usage
- Digital / screen time
- Shopping and clothing frequency
- Waste and recycling habits
- Food consumption

---

### Step 2 — Carbon Prediction
The application sends the processed inputs into the trained ML model and predicts the user's monthly carbon footprint.

The dashboard then calculates:
- Estimated Monthly CO₂
- Estimated Yearly CO₂
- Lifestyle Status
- Tree Offset Requirement

---

### Step 3 — Visual Analytics
The prediction results are displayed through multiple interactive charts:

#### Monthly Emission Mix
A donut chart showing the percentage contribution of:
- Transport
- Food
- Digital / Home
- Shopping
- Waste

#### Time-Scale Projection
A line graph showing emissions across:
- 1 Day
- 1 Week
- 1 Month
- 1 Year

#### Category-Wise Emission Trend
A line chart comparing the carbon contribution of different lifestyle categories.

#### Dataset Comparison
A histogram comparing the user's carbon footprint against the values in the training dataset.

---

### Step 4 — Reduction Lab
Users can experiment with sustainable changes to see how their carbon footprint would change.

They can reduce:
- Travel distance
- Digital / screen time
- Shopping frequency

The app then estimates:
- New Monthly CO₂
- New Yearly CO₂
- Total Carbon Reduction

This makes the impact of lifestyle changes easier to understand.

---

### Step 5 — AI Sustainability Coach
The Groq-powered assistant analyzes the user's lifestyle and prediction results to provide personalized advice.

The AI generates:
- A quick sustainability summary
- The top actions the user should take
- A short encouraging message

Example recommendations:
- Use public transport more frequently
- Reduce unnecessary shopping
- Cut down on wasted electricity
- Spend less time on energy-intensive devices

---

# 🧠 Key Features

## 1. Lifestyle Prediction
- Predicts monthly carbon footprint from user lifestyle inputs
- Uses a trained machine learning pipeline
- Converts raw lifestyle data into model-ready input automatically

## 2. Interactive Analytics Dashboard
Includes:
- Monthly CO₂ estimate
- Yearly CO₂ estimate
- Lifestyle status
- Tree offset requirement

With visualizations such as:
- Donut chart
- Line graph
- Trend analysis
- Comparison histogram

## 3. Reduction Lab
- Simulate lower travel, screen time, and shopping
- Compare before vs after emissions
- Understand how small changes create long-term environmental impact

## 4. AI Sustainability Coach
Powered by Groq AI:
- Personalized sustainability diagnosis
- Actionable recommendations
- Friendly motivational closing

---

# 📁 Project Structure

```text
Minor Project/
├── app.py
├── requirements.txt
├── .env.local
├── .gitignore
├── pipeline.pkl
├── carbon_pipeline.pkl
├── Carbon Emission.csv
└── README.md
```
## 📄 File Descriptions

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Required dependencies |
| `.env.local` | Stores the Groq API key securely |
| `pipeline.pkl` / `carbon_pipeline.pkl` | Trained machine learning model |
| `Carbon Emission.csv` | Dataset used for analysis and comparison |

---

## 🛠️ Setup & Running

### 1. Install Dependencies

```powershell id="8hl66l"
pip install -r requirements.txt

```markdown
## 2. Configure Environment Variables

Create or update a `.env.local` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 3. Run the Application

```powershell
streamlit run app.py
```

The app will open locally in your browser.

---

# 🔑 Required Files

Ensure the following files exist in the project directory:

- `Carbon Emission.csv`
- `pipeline.pkl` or `carbon_pipeline.pkl`

Without these files, the prediction model will not work.

---

# 🔒 Security Note

This project follows safe API key practices.

## Recommended Security Measures

- Keep the Groq API key inside `.env.local`
- Never hardcode the key in the frontend or source code
- Add `.env.local` to `.gitignore`
- Rotate the API key if it has ever been shared publicly

---

# 📚 Sustainability References

The sustainability suggestions and reduction advice are inspired by trusted public sources:

- IEA — Saving Energy
- EPA — Household Carbon Footprint Calculator
- EPA — Reducing Wasted Food at Home
- EPA — Energy Efficiency Tips

---

# 🏗️ Assumptions Made

- The machine learning pipeline has already been trained and exported as `pipeline.pkl` or `carbon_pipeline.pkl`.
- The dataset in `Carbon Emission.csv` contains representative carbon emission values.
- Groq API responses are used only for recommendation generation and not for prediction.
- Internet access is required only for Groq AI suggestions.
- All emission predictions are approximate and intended for awareness rather than scientific certification.

---

# 💻 Tech Stack

- Streamlit
- Pandas
- NumPy
- Plotly
- scikit-learn
- Joblib
- Groq API
- python-dotenv

---

# 🚀 Future Improvements

Potential future enhancements:

- Downloadable PDF or CSV sustainability reports
- User authentication and saved history
- Regional carbon benchmarks
- Multi-user dashboard
- Richer conversational AI with memory
- More advanced sustainability simulations

---

# 🌐 Live Demo

[🚀 Carbon Lifestyle Analyzer Studio ](https://carbon-footprint-lifestyle-analyzer-v1.streamlit.app/)

---

# 👨‍💻 Author

**Dhavala V D M Adithya Naidu**
```
