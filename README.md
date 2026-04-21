# AI Carbon Footprint Studio

An interactive Streamlit application for predicting personal carbon emissions, visualizing the result across time scales, exploring reduction scenarios, and generating AI-powered sustainability guidance using Groq.

## Highlights

- Predicts carbon footprint from lifestyle inputs using a trained machine learning pipeline
- Shows clear analytics with:
  - Monthly emission mix donut chart
  - Time-scale line graph for `1 Day`, `1 Week`, `1 Month`, and `1 Year`
  - Category-wise emission trend graph
  - Dataset comparison histogram
- Includes a reduction lab to simulate lower travel, screen time, and shopping
- Uses Groq for personalized sustainability coaching
- Keeps the API key out of the frontend by loading it from `.env.local`
- Uses web-grounded sustainability guidance inspired by trusted public sources

## Project Structure

```text
Minor Project/
├─ app.py
├─ requirements.txt
├─ .env.local
├─ .gitignore
├─ pipeline.pkl / carbon_pipeline.pkl
├─ Carbon Emission.csv
└─ README.md
```

## Setup

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Create or update `.env.local`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

3. Run the app:

```powershell
streamlit run app.py
```

## Required Files

Make sure these files are present in the project folder:

- `Carbon Emission.csv`
- `pipeline.pkl` or `carbon_pipeline.pkl`

## Features

### 1. Lifestyle Prediction
Users enter personal, transport, energy, shopping, and waste details from the sidebar. The app converts those values into the expected model input format and predicts monthly carbon emissions.

### 2. Visual Analytics
After prediction, the dashboard displays:

- `Estimated Monthly CO2`
- `Estimated Yearly CO2`
- `Lifestyle Status`
- `Tree Offset Need`

It also provides:

- A donut chart for estimated monthly emission share by category
- A line chart showing prediction scale across `1 Day`, `1 Week`, `1 Month`, and `1 Year`
- A category-wise line graph for transport, food, digital/home, shopping, and waste
- A histogram comparing the user with the dataset

### 3. Reduction Lab
Users can test the effect of reducing:

- Travel distance
- Digital/screen time
- Shopping/clothing frequency

The app then estimates projected monthly and yearly reductions.

### 4. AI Sustainability Coach
The Groq-powered assistant generates:

- A short lifestyle diagnosis
- Top action recommendations
- A concise motivational closing line

## Web-Grounded Sustainability References

The suggestion system is informed by public guidance from:

- [IEA: Saving Energy](https://www.iea.org/topics/saving-energy)
- [EPA: Household Carbon Footprint Calculator](https://www.epa.gov/ghgemissions/household-carbon-footprint-calculator)
- [EPA: Preventing Wasted Food At Home](https://www.epa.gov/recycle/reducing-wasted-food-home)
- [EPA: Pollution Prevention Tips for Energy Efficiency](https://www.epa.gov/p2/pollution-prevention-tips-energy-efficiency)

## Security Note

Do not hardcode API keys into the frontend or commit them to version control.

Recommended:

- Keep secrets in `.env.local`
- Keep `.env.local` listed in `.gitignore`
- Rotate the Groq API key if it was ever shared publicly

## Tech Stack

- Streamlit
- Pandas
- NumPy
- Plotly
- scikit-learn
- Joblib
- Groq API
- python-dotenv

## Future Improvements

- Add downloadable PDF or CSV carbon reports
- Add user authentication and history tracking
- Add live carbon benchmarks by region
- Add richer AI conversation memory for follow-up sustainability questions

## Authoring Note

This version is optimized for student project demos: simple to run locally, visually polished, and easier to explain during presentations.
