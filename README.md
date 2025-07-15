# VNL-2025-Predictor

A hobby-data science project that uses official open-source volleyball data and aims to predict the winner of Women's VNL'25.

The project repository contains:

- data folder : contains necessary files from the official website
- a main notebook named model.ipynb which handles data collection, pre-processing / feature extraction and model implementations
- my_app folder : Streamlit app that provides a user interface for the tournament simulation
- models folder : Saved, trained models that were implemented in the notebook to use in the Streamlit app

After cloning the repository and navigating into the **my_app**:

Install streamlit if it is not already installed :

```bash
   pip install streamlit
```

After the installation, run this command to view Stremlit app on your local machine:

```bash
   streamlit run app.py
```

Now you can simulate the tournament and see the predicted winner! 🏆

Ps. Do not forget to check the official match results after the quarter-finals next week to see what will actually happen!
