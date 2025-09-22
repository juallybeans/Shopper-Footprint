# Shopper's Footprint: A Carbon-Aware Shopping Logger
Shopper's Footprint is a single-page web application designed to help users visualize the environmental impact of their online shopping habits. By logging each purchase, users can see a tangible representation of their consumption, encouraging more mindful and sustainable purchasing decisions.

The core of the app is a "Package Pile" — a visual dashboard where each logged item appears as a box. The size of the box is directly proportional to the item's estimated carbon footprint, providing an immediate, intuitive understanding of its environmental cost.

# Key Features
- AI-Powered Logging: Upload a photo of a purchased item, and the app uses the Gemini API to automatically identify the object, estimate its carbon footprint, and pre-fill the logging form.

- Manual Logging: Users can also log purchases manually, entering the item description and its carbon footprint if known.

- Visual Impact Dashboard: The "Package Pile" grows with each purchase, with larger boxes representing items with a higher carbon footprint.

- Live Summary: A summary card at the top of the app displays a running total of the number of packages and the cumulative carbon footprint in kg CO2e.

- Interactive Details: Click on any package in the pile to view its details in a clean, modern modal window.

# Tech Stack
- Frontend: Vue.js, Javascript

- Backend: Flask (Python)

- Database: Supabase (PostgreSQL)

- AI Model: Google Gemini 1.5 Flash Latest

# How to Run the Application
Follow these steps to set up and run the project on your local machine.

## 1. Backend Setup (Flask)

1. Project Files: Place the backend files (app.py, requirements.txt, .env) in a dedicated folder.

2. Install Dependencies:
```bash
pip install -r requirements.txt
```
3. Set Up Environment Variables:
Ensure your .env file is in the backend folder and contains the necessary API keys for Supabase and Google Gemini.
```env
SUPABASE_URL="YOUR_SUPABASE_URL_HERE"
SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY_HERE"
GEMINI_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY_HERE"
```
4. Run the Server:
```bash
flask run
```
The backend will now be running at http://127.0.0.1:5000.

## 2. Frontend Setup
1. No Installation Needed: The frontend is a single index.html file with no build steps.

2. Open in Browser: Simply open the index.html file in any modern web browser.

The application should now be fully functional, connecting to your running Flask backend and Supabase database.