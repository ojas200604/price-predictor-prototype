def evaluate_decision_support(current_price: float, predicted_price: float):
    pct_change = ((predicted_price - current_price) / current_price) * 100
    
    if pct_change >= 10.0:
        risk_level = "CRITICAL"
        action = "High price spike expected. Immediately release 10,000 MT from strategic buffer stock."
    elif pct_change >= 5.0:
        risk_level = "WARNING"
        action = "Moderate price increase projected. Prepare 5,000 MT buffer release."
    else:
        risk_level = "STABLE"
        action = "Prices within normal variance. Maintain standard monitoring."
        
    return round(pct_change, 2), risk_level, action