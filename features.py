def get_features(url):
    features = []
    features.append(len(url)) # URL length
    features.append(1 if "@" in url else 0) # @ symbol
    features.append(1 if url.startswith("https") else 0) # HTTPS
    features.append(url.count(".")) # Dot count
    features.append(url.count("-")) # Hyphen count
    features.append(1 if "192." in url or "http://" in url and url.count(".")>3 else 0) # IP check
    return features