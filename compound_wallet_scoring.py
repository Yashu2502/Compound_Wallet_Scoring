import pandas as pd
import requests
from tqdm import tqdm
import time

# === SETTINGS ===
COVALENT_API_KEY = "cqt_rQwKyDGM7f4RBjFppXQHJvrJgJKg"   # 🔁 Replace with your API key
CHAIN_ID = 1  # Ethereum Mainnet
COMPOUND_CONTRACTS = [
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b",  # Compound Comptroller
    "0xc00e94cb662c3520282e6f5717214004a7f26888",  # COMP Token
    # Add more relevant contracts if needed
]

# === STEP 1: Load Wallets ===
wallets_df = pd.read_csv("Wallet_id.csv")
wallets = wallets_df["wallet_id"].tolist()

# === STEP 2: Helper Function to Fetch Transactions ===
def fetch_transactions(wallet):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/transactions_v2/"
    params = {"key": COVALENT_API_KEY, "page-size": 1000}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching wallet {wallet}: {response.status_code}")
        return []
    return response.json().get("data", {}).get("items", [])

# === STEP 3: Extract Features ===
def extract_features(wallet, transactions):
    total_txn = len(transactions)
    compound_txn = 0
    high_value_txn = 0
    value_threshold = 1 * 10**18  # ~1 ETH
    
    for tx in transactions:
        to_address = tx.get("to_address", "").lower()
        value = int(tx.get("value", 0))
        
        if to_address in COMPOUND_CONTRACTS:
            compound_txn += 1
        if value > value_threshold:
            high_value_txn += 1
    
    return {
        "wallet_id": wallet,
        "total_txn": total_txn,
        "compound_txn": compound_txn,
        "high_value_txn": high_value_txn,
    }

# === STEP 4: Process All Wallets ===
features_list = []

print("Fetching and analyzing wallets...")
for wallet in tqdm(wallets):
    try:
        txns = fetch_transactions(wallet)
        features = extract_features(wallet, txns)
        features_list.append(features)
        time.sleep(1)  # To avoid rate limiting
    except Exception as e:
        print(f"Error processing {wallet}: {e}")

features_df = pd.DataFrame(features_list)

# === STEP 5: Scoring Logic (Simple Rule-Based) ===
# Normalize & score (simple example)
def calculate_score(row):
    base_score = 500
    score = base_score
    score += row["compound_txn"] * 10
    score -= row["high_value_txn"] * 5
    score = max(0, min(1000, score))  # Bound between 0–1000
    return int(score)

features_df["score"] = features_df.apply(calculate_score, axis=1)
final_df = features_df[["wallet_id", "score"]]

# === STEP 6: Save to CSV ===
final_df.to_csv("wallet_scores.csv", index=False)
print("\n✅ Done! Output saved to 'wallet_scores.csv'")
