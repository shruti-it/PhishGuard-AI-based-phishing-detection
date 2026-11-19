import pandas as pd
import random, numpy as np
random.seed(42)
np.random.seed(42)

rows = []
for i in range(10000):
    is_phish = 1 if i >= 5000 else 0
    # Add noise so models are NOT perfect - like real life
    noise = np.random.normal(0, 0.15)
    
    def val(prob_phish, prob_safe):
        p = prob_phish if is_phish else prob_safe
        # 8% random flip to make it realistic
        if random.random() < 0.08:
            return random.randint(0,1)
        return 1 if random.random() < p else 0

    rows.append({
        "having_IP": val(0.75, 0.10),
        "URL_Length": val(0.65, 0.20),
        "Shortining_Service": val(0.70, 0.15),
        "having_At_Symbol": val(0.80, 0.05),
        "double_slash": val(0.60, 0.25),
        "Prefix_Suffix": val(0.70, 0.18),
        "having_Sub_Domain": val(0.62, 0.22),
        "HTTPS": 0 if is_phish and random.random()>0.25 else 1 if random.random()>0.15 else 0,
        "Domain_registeration": val(0.20, 0.80),
        "Favicon": val(0.60, 0.30),
        "port": val(0.55, 0.30),
        "HTTPS_token": val(0.70, 0.12),
        "Result": 1 if is_phish else 0
    })

df = pd.DataFrame(rows)
df.to_csv("dataset.csv", index=False)
print("Done! Rows:", len(df))