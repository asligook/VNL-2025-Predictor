import joblib
import xgboost as xgb
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load DataFrames
world_df = pd.read_csv('world_df.csv')
team_stats_df = pd.read_csv('team_stats.csv')

# Load models
logistic_model = joblib.load('logistic_model.pkl')
random_forest_model = joblib.load('random_forest_model.pkl')
neural_net_model = joblib.load('neural_net_model.pkl')

xgb_model = xgb.XGBClassifier()
xgb_model.load_model('xgboost_model.json')

# Combine into dictionary (same as before)
trained_models = {
    'Logistic Regression': logistic_model,
    'Random Forest': random_forest_model,
    'XGBoost': xgb_model,
    'Neural Net': neural_net_model
}

# --- Prepare input ---
def prepare_match_input(team_a_code, team_b_code):
    a_row = world_df.loc[world_df['Code'] == team_a_code].iloc[0]
    b_row = world_df.loc[world_df['Code'] == team_b_code].iloc[0]

    rank_diff = a_row['Rank'] - b_row['Rank']
    points_diff = a_row['Points'] - b_row['Points']

    a_team_stat = team_stats_df.loc[team_stats_df['Team'] == team_a_code].iloc[0]['Offense_Score']
    b_team_stat = team_stats_df.loc[team_stats_df['Team'] == team_b_code].iloc[0]['Offense_Score']
    offense_diff = a_team_stat - b_team_stat

    return pd.DataFrame([{
        'Rank_Diff': rank_diff,
        'Points_Diff': points_diff,
        'Offense_Diff': offense_diff
    }])

# --- Predict match ---
def predict_match(team_a, team_b):
    input_data = prepare_match_input(team_a, team_b)
    probs = []
    all_model_probs = {}

    for name, model in trained_models.items():
        prob = model.predict_proba(input_data)[0, 1]  # P(team A wins)
        probs.append(prob)
        all_model_probs[name] = prob

    avg_prob = sum(probs) / len(probs)
    winner = team_a if avg_prob >= 0.5 else team_b
    return winner, avg_prob, all_model_probs

# --- Simulate ---
def simulate_tournament():
    results = []

    # QFs
    quarter_finals = [
        ('ITA', 'USA'),
        ('POL', 'CHN'),
        ('JPN', 'TUR'),
        ('BRA', 'GER')
    ]
    semi_finalists = []
    for team_a, team_b in quarter_finals:
        winner, avg_prob, details = predict_match(team_a, team_b)
        results.append({
            "stage": "Quarter Final",
            "match": f"{team_a} vs {team_b}",
            "winner": winner,
            "avg_prob": avg_prob,
            "details": details
        })
        semi_finalists.append(winner)

    # SFs
    semi_finals = [
        (semi_finalists[0], semi_finalists[1]),
        (semi_finalists[2], semi_finalists[3])
    ]
    finalists = []
    for team_a, team_b in semi_finals:
        winner, avg_prob, details = predict_match(team_a, team_b)
        results.append({
            "stage": "Semi Final",
            "match": f"{team_a} vs {team_b}",
            "winner": winner,
            "avg_prob": avg_prob,
            "details": details
        })
        finalists.append(winner)

    # Final
    team_a, team_b = finalists[0], finalists[1]
    winner, avg_prob, details = predict_match(team_a, team_b)
    results.append({
        "stage": "Final",
        "match": f"{team_a} vs {team_b}",
        "winner": winner,
        "avg_prob": avg_prob,
        "details": details
    })

    return results


# --- Streamlit UI ---
st.header("🏆 VNL 2025 Full Tournament Simulator")
if st.button("Simulate Tournament"):
    results = simulate_tournament()

    for r in results:
        st.subheader(f"{r['stage']}: {r['match']}")
        st.write(f"**Predicted Winner:** {r['winner']}  \n"
                 f"**Average Probability:** {r['avg_prob']:.2%}")
        with st.expander("See individual model probabilities"):
            for name, p in r['details'].items():
                st.write(f"{name}: {p:.2%}")

    st.success(f"🏐 **Champion: {results[-1]['winner']}** 🏆")