import sys
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

sys.stdout.reconfigure(encoding='utf-8')

from src.predictor import UCLPredictor
from src.matchday import predict_ucl_matchday, format_matchday_predictions

def main():
    parser = argparse.ArgumentParser(description="Predict UEFA Champions League matchdays and single games.")
    parser.add_argument("--season", type=str, default="2026-27", help="UCL season (e.g. 2026-27)")
    parser.add_argument("--matchday", type=int, default=1, help="Matchday number (1 to 8, or knockout rounds)")
    parser.add_argument("--format", type=str, default="detailed", choices=["compact", "detailed", "portfolio", "multimarket"], help="Output format")
    parser.add_argument("--home", type=str, default=None, help="Custom single match home team")
    parser.add_argument("--away", type=str, default=None, help="Custom single match away team")
    parser.add_argument("--odds-h", type=float, default=None, help="Bookmaker Home odds (decimal)")
    parser.add_argument("--odds-d", type=float, default=None, help="Bookmaker Draw odds (decimal)")
    parser.add_argument("--odds-a", type=float, default=None, help="Bookmaker Away odds (decimal)")

    args = parser.parse_args()

    predictor = UCLPredictor()

    if args.home and args.away:
        market_odds = None
        if args.odds_h and args.odds_d and args.odds_a:
            market_odds = {"H": args.odds_h, "D": args.odds_d, "A": args.odds_a}

        print(f"\n==================================================================")
        print(f"⚽ UCL 2.0 ADVANCED MATCH INTELLIGENCE: {args.home} vs {args.away}")
        print(f"==================================================================")
        p = predictor.predict_match(args.home, args.away, market_odds=market_odds)

        print(f"\n📊 1. PROBABILIDADES 1X2 (CALIBRADAS CON STACKING META-LEARNER):")
        print(f"   🏠 Local ({p.home_team}):     {p.probs['H']*100:5.1f}%  (Exp Goals: {p.lambda_home:.2f})")
        print(f"   🤝 Empate (X):                {p.probs['D']*100:5.1f}%")
        print(f"   🚗 Visitante ({p.away_team}):  {p.probs['A']*100:5.1f}%  (Exp Goals: {p.lambda_away:.2f})")
        print(f"   🎯 Pick Recomendado:          {p.prediction}")
        print(f"   🛡️ Doble Oportunidad:         {p.double_chance} ({p.double_chance_prob*100:.1f}%)")
        print(f"   🚦 Safety Tier:               {p.safety_tier.value}")
        print(f"   🔍 Confianza:                 {p.confidence.value}")

        print(f"\n⚽ 2. MERCADOS DE GOLES (DERIVADOS ANALÍTICAMENTE):")
        ou = p.over_under
        print(f"   Over 1.5: {ou.get('over_1_5', 0)*100:.1f}% | Under 1.5: {ou.get('under_1_5', 0)*100:.1f}%")
        print(f"   Over 2.5: {ou.get('over_2_5', 0)*100:.1f}% | Under 2.5: {ou.get('under_2_5', 0)*100:.1f}%")
        print(f"   Over 3.5: {ou.get('over_3_5', 0)*100:.1f}% | Under 3.5: {ou.get('under_3_5', 0)*100:.1f}%")
        btts = p.btts
        print(f"   Ambos Anotan (BTTS): Sí: {btts.get('yes', 0)*100:.1f}% | No: {btts.get('no', 0)*100:.1f}%")

        print(f"\n🎯 3. TOP 5 MARCADORES EXACTOS MÁS PROBABLES:")
        for score, pct in list(p.top_exact_scores.items())[:5]:
            print(f"   {score:<5} -> {pct:.1f}%")

        print(f"\n🌍 4. FACTORES CONTEXTUALES & FATIGA:")
        print(f"   Distancia de Viaje: {p.travel_distance_km:.1f} km (Índice de fatiga: {p.travel_fatigue:.2f})")

        if p.edge:
            print(f"\n💰 5. INTELIGENCIA DE MERCADO & VALUE BETTING (+EV):")
            has_val = p.edge.get("has_value_bet", False)
            if has_val:
                print("   🔥 ¡OPORTUNIDAD DE VALOR DETECTADA (+EV)!")
            for out_key, mkt in p.edge.get("markets", {}).items():
                val_tag = "✅ VALOR" if mkt["is_value_bet"] else "❌ Sin valor"
                print(f"   [{out_key}] Momio: {mkt['market_odd']} | Prob Modelo: {mkt['model_prob']*100:.1f}% | Fair: {mkt['fair_market_prob']*100:.1f}% | EV: {mkt['expected_value_pct']:+.1f}% | Kelly: {mkt['kelly_stake_pct']:.2f}% | {val_tag}")

        print("==================================================================\n")
    else:
        preds = predict_ucl_matchday(season=args.season, matchday=args.matchday, predictor=predictor)
        formatted = format_matchday_predictions(preds, format_type=args.format)
        print("\n" + formatted + "\n")

if __name__ == "__main__":
    main()
