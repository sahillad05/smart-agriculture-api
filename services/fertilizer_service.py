def recommend_fertilizer(data):

    n = data.nitrogen
    p = data.phosphorus
    k = data.potassium

    # Simple rule-based recommendation logic

    if n < 50:
        return "Urea"

    elif p < 40:
        return "DAP"

    elif k < 40:
        return "MOP (Muriate of Potash)"

    elif n > 100:
        return "Compost or Organic Fertilizer"

    else:
        return "NPK Balanced Fertilizer"