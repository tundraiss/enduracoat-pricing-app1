# EnduraCoat Pricing App (Local Web App)

This is a simple “actual app” version of your Excel pricing calculator, built in **Streamlit**.

## What you get
- App-style inputs + results
- 3 calculation modes:
  - Option 1: Flat area (cm)
  - Option 2: Steel weight (kg)
  - Circular: radius (cm)

## Run it locally (Windows / Mac)
1) Install Python 3.10+  
2) Open a terminal in this folder  
3) Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4) Start the app:
   ```
   python -m streamlit run streamlit_app.py
   ```
Streamlit will open a browser tab with the app.

## Notes
The formulas match the ones found in your Excel sheet:
- Coverage = 1000 / (SG * microns)
- Area & powder grams calculations follow the same logic
