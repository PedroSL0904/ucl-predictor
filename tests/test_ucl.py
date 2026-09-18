"""Comprehensive test suite for UCL Predictor 2.0."""
import pytest
import numpy as np
from src.models.statistical import UCLDixonColes, dc_tau
from src.models.calibration import TemperatureScaler
from src.models.stacking import StackingMetaLearner
from src.strategy.safety import compute_safety_tier, SafetyTier
from src.strategy.double_chance import compute_double_chance
from src.features.geo import EuropeanGeoManager, haversine_km
from src.market.devig import devig_shin, devig_multiplicative
from src.market.edge import ValueBettingEngine
from src.data.clubelo import ClubEloManager
from src.predictor import UCLPredictor

def test_dixon_coles_probabilities():
    dc = UCLDixonColes()
    probs, grid, (lh, la) = dc.predict_proba(1, 2, home_elo=1800, away_elo=1700)
    assert np.isclose(probs.sum(), 1.0, atol=1e-5)
    assert probs[0] > probs[2]
    assert lh > 0 and la > 0
    assert np.isclose(grid.sum(), 1.0, atol=1e-5)

def test_multi_market_derivations():
    dc = UCLDixonColes()
    _, grid, _ = dc.predict_proba(1, 2, home_elo=1850, away_elo=1650)
    markets = UCLDixonColes.derive_multi_markets(grid)

    ou = markets["over_under"]
    assert np.isclose(ou["over_2_5"] + ou["under_2_5"], 1.0, atol=1e-3)
    assert np.isclose(ou["over_1_5"] + ou["under_1_5"], 1.0, atol=1e-3)
    assert ou["over_1_5"] >= ou["over_2_5"] >= ou["over_3_5"]

    btts = markets["btts"]
    assert np.isclose(btts["yes"] + btts["no"], 1.0, atol=1e-3)

    top_scores = markets["top_exact_scores"]
    assert len(top_scores) == 5
    assert sum(top_scores.values()) > 20.0  # Top 5 should cover meaningful mass

def test_geo_travel_engine():
    geo = EuropeanGeoManager()
    d_mad_man = geo.calculate_distance_km("Real Madrid", "Man City")
    assert 1300 < d_mad_man < 1600
    fatigue = geo.calculate_travel_fatigue(d_mad_man)
    assert 0.0 <= fatigue <= 1.0

    p_rm = geo.get_club_pedigree("Real Madrid")
    assert p_rm > 100.0

def test_devig_and_value_betting():
    odds = {"H": 2.10, "D": 3.40, "A": 3.60}
    fair_probs = devig_shin(odds)
    assert np.isclose(sum(fair_probs.values()), 1.0, atol=1e-4)
    assert fair_probs["H"] > fair_probs["A"]

    # Model gives 60% to Home
    model_probs = {"H": 0.60, "D": 0.22, "A": 0.18}
    evals = ValueBettingEngine.evaluate_market(model_probs, odds, min_edge_threshold=0.03)
    assert evals["has_value_bet"] is True
    assert evals["markets"]["H"]["is_value_bet"] is True
    assert evals["markets"]["H"]["expected_value_pct"] > 0
    assert evals["markets"]["H"]["kelly_stake_pct"] > 0

def test_stacking_meta_learner():
    meta = StackingMetaLearner(C=0.5)
    # 4 models * 3 outcomes = 12 meta features
    dummy_X = np.random.dirichlet((1, 1, 1), size=(50, 4)).reshape(50, 12)
    dummy_y = np.random.choice([0, 1, 2], size=50)
    meta.fit(dummy_X, dummy_y)
    probs = meta.predict_proba(dummy_X[:5])
    assert probs.shape == (5, 3)
    assert np.allclose(np.sum(probs, axis=1), 1.0)

def test_temperature_scaler():
    scaler = TemperatureScaler(temperature=0.60)
    raw = np.array([[0.60, 0.25, 0.15]])
    scaled = scaler.transform(raw)
    assert np.isclose(scaled.sum(), 1.0, atol=1e-5)
    assert scaled[0, 0] > raw[0, 0]

def test_safety_tiers_and_double_chance():
    tier = compute_safety_tier({"H": 0.65, "D": 0.20, "A": 0.15})
    assert tier == SafetyTier.BANQUERO

    dc_tag, dc_prob = compute_double_chance({"H": 0.55, "D": 0.25, "A": 0.20})
    assert dc_tag == "1X"
    assert np.isclose(dc_prob, 0.80)

def test_master_predictor_full():
    predictor = UCLPredictor()
    pred = predictor.predict_match("Real Madrid", "Stuttgart", market_odds={"H": 1.35, "D": 5.50, "A": 9.00})
    assert pred.home_team == "Real Madrid"
    assert np.isclose(sum(pred.probs.values()), 1.0, atol=1e-4)
    assert pred.over_under["over_2_5"] > 0
    assert pred.btts["yes"] > 0
    assert len(pred.top_exact_scores) == 5
    assert pred.travel_distance_km > 0
    assert pred.edge is not None

def test_full_uefa_knockout_simulation():
    from src.simulation.bracket import KnockoutSimulator
    teams = [f"Team_{i:02d}" for i in range(1, 37)]
    elos = {t: 1800 - i * 15 for i, t in enumerate(teams)}
    rng = np.random.default_rng(42)

    bracket_res = KnockoutSimulator.simulate_knockout_bracket(
        ranked_teams=teams,
        elo_lookup=lambda t: elos[t],
        rng=rng
    )
    assert len(bracket_res["playoffs"]) == 16
    assert len(bracket_res["r16"]) == 16
    assert len(bracket_res["qf"]) == 8
    assert len(bracket_res["sf"]) == 4
    assert len(bracket_res["finalists"]) == 2
    assert bracket_res["champion"] in bracket_res["finalists"]

def test_dynamic_causal_features():
    predictor = UCLPredictor()
    dyn = predictor._compute_dynamic_features("Real Madrid", "Barcelona", "2024-05-01")
    assert "form_3_h" in dyn
    assert "form_5_h" in dyn
    assert "gd_5_h" in dyn
    assert "rest_h" in dyn
    assert "h2h_total" in dyn
    assert dyn["rest_h"] >= 1.0

def test_elo_time_series_resolution():
    mgr = ClubEloManager()
    # Historic vs recent lookup for Atletico
    elo_2024 = mgr.get_elo("Atletico", match_date="2024-01-01")
    elo_now = mgr.get_elo("Atletico")
    assert elo_2024 > 1750
    assert elo_now > 1750
