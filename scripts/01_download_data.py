import os
import sys
import urllib.request
from pathlib import Path
from tqdm import tqdm

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("C:/Users/Boutros/ucl-predictor")
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
OPENFOOTBALL_DIR = RAW_DIR / "openfootball"
OPENFOOTBALL_DIR.mkdir(parents=True, exist_ok=True)

# 1. Download EloRatings.csv
elo_file = RAW_DIR / "EloRatings.csv"
if not elo_file.exists():
    elo_url = "https://raw.githubusercontent.com/xgabora/Club-Football-Match-Data/main/data/EloRatings.csv"
    print(f"Downloading European Elo ratings from {elo_url}...")
    req = urllib.request.Request(elo_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp, open(elo_file, "wb") as f:
        total = int(resp.headers.get("content-length", 0))
        with tqdm(total=total, unit="B", unit_scale=True, desc="EloRatings.csv") as pbar:
            while chunk := resp.read(65536):
                f.write(chunk)
                pbar.update(len(chunk))
    print(f"Saved EloRatings.csv ({elo_file.stat().st_size / 1024 / 1024:.2f} MB)")
else:
    print("EloRatings.csv already exists.")

# 2. Download all UCL seasons from openfootball
seasons = [
    "2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18",
    "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"
]

for s in seasons:
    dest = OPENFOOTBALL_DIR / f"{s}.txt"
    url = f"https://raw.githubusercontent.com/openfootball/champions-league/master/{s}/cl.txt"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            dest.write_bytes(content)
        print(f"Season {s}: {len(content.splitlines())} lines saved.")
    except Exception as e:
        print(f"Failed to download {s}: {e}")

print("Phase 1 Data Download Complete!")
