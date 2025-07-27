# Compound Wallet Risk Scoring

## Overview

This project analyzes wallet interactions with the Compound V2/V3 lending protocol to assign a **risk score between 0 and 1000** to each wallet. The score reflects the wallet's historical behavior and potential creditworthiness based on key features derived from on-chain activity.

---

## Objective

- Retrieve Compound protocol transactions for each wallet.
- Engineer meaningful features from the on-chain data.
- Normalize and analyze wallet behavior.
- Assign a final risk score per wallet using a rule-based scoring model.

---

## Data Collection

- **Source:** Compound V2 and V3 subgraphs or APIs
- **Target wallets:** As listed in `Wallet_id.csv`
- **Transaction types:** supply, borrow, repay, liquidate, withdraw

---

## Feature Engineering

| Feature                     | Description                                                  |
|----------------------------|--------------------------------------------------------------|
| total_supplied_usd         | Total USD value supplied                                     |
| total_borrowed_usd         | Total USD borrowed                                           |
| repayment_ratio            | Total repaid / borrowed ratio                                |
| num_liquidations_received  | Times wallet was liquidated                                  |
| avg_borrow_supply_ratio    | Borrowed / supplied average across sessions                  |
| tx_frequency               | Number of Compound txs per day                               |
| days_active                | Duration between first and last interaction                  |
| asset_diversity            | Number of unique tokens used                                 |

Features were normalized using **Min-Max Scaling**.

---

## Scoring Method

Each feature contributes to the risk score based on defined rules. The base score is 1000 (max risk), and deductions are applied for safer behavior.

### Key Logic:
- Wallets with **high borrow & low repay** are penalized.
- **Frequent liquidations** increase risk.
- **Consistent supply + long activity duration** lower risk.
- Wallets with **balanced ratios** and low volatility score lower.

> Final Score = 1000 - (Feature Risk Contribution)

---

## Visualization

- Risk score distribution
- Borrow/supply ratio trends
- Liquidation frequency vs. score

---

## Files

| File                        | Description                                      |
|-----------------------------|--------------------------------------------------|
| `compound_wallet_scoring.py`| Core script to extract, process, and score data |
| `Wallet_id.csv`             | Input wallet addresses                           |
| `wallet_scores.csv`         | Final risk scores for each wallet                |
| `Report.pdf`                | Analytical insights and graphs                   |
| `README.md`                 | You’re here                                      |

---

## Conclusion

This model provides a foundational approach to DeFi wallet risk scoring. It can be extended with machine learning, market volatility analysis, and real-time monitoring for production-grade systems.

