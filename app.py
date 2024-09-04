from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    team1_matches = data.get('team1_matches', [])
    team2_matches = data.get('team2_matches', [])

    # Calculare goluri, cornere și cartonașe pentru fiecare echipă
    team1_goals = sum([match['goals_scored'] for match in team1_matches])
    team2_goals = sum([match['goals_scored'] for match in team2_matches])

    total_goals = team1_goals + team2_goals
    total_corners = sum([match['corners'] for match in team1_matches]) + sum([match['corners'] for match in team2_matches])
    total_cards = sum([match['cards'] for match in team1_matches]) + sum([match['cards'] for match in team2_matches])

    # Calculare șanse de câștig pe baza golurilor
    if total_goals == 0:
        team1_win_chance = 50
        team2_win_chance = 50
    else:
        team1_win_chance = (team1_goals / total_goals) * 100
        team2_win_chance = (team2_goals / total_goals) * 100

    # Generare simulări
    simulations = []
    for _ in range(5):
        simulations.append({
            "team1_score": random.randint(0, 4),
            "team2_score": random.randint(0, 4),
            "team1_corners": random.randint(3, 12),
            "team2_corners": random.randint(3, 12),
            "team1_cards": random.randint(0, 3),
            "team2_cards": random.randint(0, 3),
        })

    # Sugestii de pariuri
    over_under_goals = "over 2.5" if total_goals > 2 else "under 2.5"
    over_under_3_goals = "over 3.0" if total_goals > 3 else "under 3.0"
    both_teams_score = "yes" if team1_goals > 0 and team2_goals > 0 else "no"

    combined_corners = total_corners
    over_under_corners = "over 7.5" if combined_corners > 7 else "under 7.5"

    combined_cards = total_cards
    over_under_cards = "over 2.5" if combined_cards > 2 else "under 2.5"

    # Funcție pentru calcularea riscului pariurilor
    def calculate_risk(probability):
        if probability > 70:
            return "low risk"
        elif probability > 40:
            return "medium risk"
        else:
            return "high risk"

    # Rezultatele și sugestiile de pariuri
    result = {
        "team1_win_chance": round(team1_win_chance, 2),
        "team2_win_chance": round(team2_win_chance, 2),
        "simulations": simulations,
        "betting_suggestions": {
            "team1_win_risk": calculate_risk(team1_win_chance),
            "team2_win_risk": calculate_risk(team2_win_chance),
            "over_under_goals": over_under_goals,
            "combined_corners": combined_corners,
            "combined_cards": combined_cards,
            "both_teams_score": both_teams_score,
            "under_over_3_goals": over_under_3_goals,
            "total_corners": over_under_corners,
            "total_cards": over_under_cards
        }
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
