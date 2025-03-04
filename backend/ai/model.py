import spacy
import re

# NLP modelini yükleyelim
nlp = spacy.load("en_core_web_sm")

# Anahtar kelimeler ve cilt bakım sorunlarına yönelik kurallar
SKINCARE_KEYWORDS = {
    "sensitive": ["sensitive", "irritated", "reactive", "allergic"],
    "acne_prone": ["acne", "pimples", "breakouts", "blemishes", "zits", "spots", "acne-prone"],
    "aging": ["aging", "wrinkles", "fine lines", "lines", "sagging", "age spots"],
    "dry": ["dry", "flaky", "rough", "parched"],
    "oily": ["oily", "greasy", "shiny", "sebaceous"],
    "combination": ["combination", "mixed", "both dry and oily"],
    "hyperpigmentation": ["hyperpigmentation", "dark spots", "sun spots", "uneven skin tone", "melasma"],
    "rosacea": ["rosacea", "redness", "flushing", "blushing"],
    "eczema": ["eczema", "atopic dermatitis", "itchy", "dry patches"],
    "sun_damage": ["sun damage", "sun spots", "UV damage", "sunburn"]
}

# Cilt bakım kuralları ve içerikleri
SKINCARE_RULES = {
    "sensitive": {
        "rule": "For sensitive skin, focus on barrier-repairing and soothing ingredients. Use gentle cleansers like micellar water or cream cleansers. Look for calming ingredients such as aloe vera, centella asiatica, chamomile, and oat extract. Avoid harsh exfoliants, alcohol, and artificial fragrances. Use products with ceramides, glycerin, and hyaluronic acid to maintain hydration without irritation.",
        "ingredients": [
            "ceramides", "glycerin", "hyaluronic acid", "aloe vera", "centella asiatica",
            "chamomile", "oat extract", "micellar water", "cream cleansers"
        ]
    },
    "acne_prone": {
        "rule": "For acne-prone skin, prioritize ingredients with antibacterial and anti-inflammatory properties. Salicylic acid (BHA) helps unclog pores and reduce breakouts. Benzoyl peroxide is effective against acne-causing bacteria. Retinoids (like adapalene or retinol) promote cell turnover to prevent clogged pores. Niacinamide can help reduce inflammation and regulate sebum production. Avoid comedogenic ingredients and focus on non-comedogenic, lightweight products.",
        "ingredients": [
            "salicylic acid", "benzoyl peroxide", "retinol", "adapalene", "niacinamide",
            "tea tree oil", "witch hazel", "zinc", "benzoyl peroxide"
        ]
    },
    "dry": {
        "rule": "For dry skin, focus on hydrating and nourishing ingredients. Use rich moisturizers containing ceramides, hyaluronic acid, glycerin, and squalane. Incorporate oils like jojoba, argan, or rosehip oil for extra moisture. Avoid harsh cleansers and exfoliants that can strip your skin's natural oils. Use hydrating serums and apply occlusives like petrolatum or shea butter to lock in moisture.",
        "ingredients": [
            "ceramides", "hyaluronic acid", "glycerin", "squalane", "jojoba oil", 
            "argan oil", "rosehip oil", "petrolatum", "shea butter", "hydrating serums"
        ]
    },
    "oily": {
        "rule": "For oily skin, look for lightweight, non-comedogenic products. Use water-based moisturizers with ingredients like niacinamide, which helps regulate oil production, and salicylic acid to keep pores clear. Gel-based cleansers and products containing tea tree oil, witch hazel, and zinc are also beneficial. Avoid heavy creams and oils that may clog pores.",
        "ingredients": [
            "niacinamide", "salicylic acid", "tea tree oil", "witch hazel", "zinc",
            "water-based moisturizers", "gel-based cleansers"
        ]
    },
    "combination": {
        "rule": "For combination skin, balance is key. Use lightweight, hydrating products for dry areas and oil-controlling ingredients for the T-zone. Hyaluronic acid, niacinamide, and gentle exfoliants like lactic acid are great choices. Multi-masking can also help address different skin needs simultaneously.",
        "ingredients": [
            "hyaluronic acid", "niacinamide", "lactic acid", "gentle exfoliants", "lightweight moisturizers"
        ]
    },
    "hyperpigmentation": {
        "rule": "For hyperpigmentation, focus on brightening and exfoliating ingredients. Vitamin C (ascorbic acid) helps reduce dark spots and evens skin tone. Niacinamide can reduce pigmentation and improve skin barrier function. Alpha arbutin, tranexamic acid, and licorice root extract are also effective. Chemical exfoliants like AHAs (glycolic acid, lactic acid) can promote cell turnover. Always use sunscreen to prevent further pigmentation.",
        "ingredients": [
            "vitamin C", "ascorbic acid", "niacinamide", "alpha arbutin", "tranexamic acid",
            "licorice root extract", "glycolic acid", "lactic acid", "sunscreen"
        ]
    },
    "aging": {
        "rule": "For aging skin, focus on ingredients that promote collagen production and improve skin texture. Retinoids (retinol, tretinoin) are the gold standard for anti-aging. Peptides, antioxidants (such as vitamin C and E), and niacinamide can help reduce fine lines and wrinkles. Hyaluronic acid and ceramides maintain hydration and plump the skin. Avoid excessive exfoliation, which can make skin appear thinner.",
        "ingredients": [
            "retinol", "tretinoin", "peptides", "vitamin C", "vitamin E", "niacinamide",
            "hyaluronic acid", "ceramides"
        ]
    },
    "rosacea": {
        "rule": "For rosacea-prone skin, choose soothing and anti-inflammatory ingredients. Azelaic acid can reduce redness and bumps. Niacinamide, green tea extract, and colloidal oatmeal are also calming. Avoid harsh exfoliants, alcohol, and fragrance, as these can trigger flare-ups.",
        "ingredients": [
            "azelaic acid", "niacinamide", "green tea extract", "colloidal oatmeal"
        ]
    },
    "eczema": {
        "rule": "For eczema, prioritize barrier-strengthening and soothing ingredients. Ceramides, fatty acids, and colloidal oatmeal help repair the skin barrier. Use fragrance-free and hypoallergenic products. Avoid harsh cleansers and use rich, occlusive moisturizers like petrolatum and shea butter to prevent water loss.",
        "ingredients": [
            "ceramides", "fatty acids", "colloidal oatmeal", "fragrance-free products",
            "petrolatum", "shea butter"
        ]
    },
    "sun_damage": {
        "rule": "For sun-damaged skin, prioritize repairing and protecting ingredients. Antioxidants like vitamin C, E, and niacinamide help repair damage. Use moisturizers with ceramides and peptides to support the skin barrier. Sunscreen with SPF 30 or higher is essential to prevent further damage.",
        "ingredients": [
            "vitamin C", "vitamin E", "niacinamide", "ceramides", "peptides", "sunscreen"
        ]
    }
}

# Cilt bakım bileşenlerinin uyumsuzlukları
INCOMPATIBLE_INGREDIENTS = {
    "retinol": ["salicylic acid", "benzoyl peroxide", "vitamin C"],
    "salicylic acid": ["retinol", "benzoyl peroxide"],
    "benzoyl peroxide": ["retinol", "salicylic acid"],
    "vitamin C": ["retinol"]
}

# İçerik uyumsuzluğunu kontrol etme
def check_compatibility(ingredients):
    incompatible = []
    for ingredient in ingredients:
        if ingredient in INCOMPATIBLE_INGREDIENTS:
            for incompatible_ingredient in INCOMPATIBLE_INGREDIENTS[ingredient]:
                if incompatible_ingredient in ingredients:
                    incompatible.append((ingredient, incompatible_ingredient))
    return incompatible

# Semantik Benzerlik Hesaplama
# def analyze_skin_problem(text):
#     """Kullanıcının cilt problemi hakkında öneriler sunar."""
#     doc = nlp(text.lower())  # Metni küçük harfe çevir ve NLP analizi yap
#     recommendations = set()  # Set kullanarak tekrarı önleyeceğiz
#     ingredients = set()  # Kullanıcıya hangi bileşenlerin önerildiğini takip edeceğiz

#     for problem, data in SKINCARE_KEYWORDS.items():
#         for keyword in data:
#             if any(re.search(r"\b" + re.escape(keyword) + r"\b", text.lower()) for keyword in SKINCARE_KEYWORDS[problem]):
#                 recommendations.add(SKINCARE_RULES[problem]["rule"])
#                 # İlgili bileşenleri öneriler listesine ekleyelim
#                 ingredients.update(SKINCARE_RULES[problem]["ingredients"])

#     # İçerik uyumluğunu kontrol et
#     incompatible = check_compatibility(list(ingredients))
    
#     # Uyumlu olmayan bileşenler varsa, kullanıcıya bildirelim
#     # If there are incompatible ingredients, notify the user
#     if incompatible:
#         incompatible_str = " and ".join(
#             [f"'{item[0]}' with '{item[1]}'" for item in incompatible]
#         )
#         warning_message = (
#             f"Warning: The following ingredients may not work well together: {incompatible_str}. "
#             "You may consider using these ingredients at different times or avoid using one of them."
#         )
#         return list(recommendations) + [warning_message]

#     # Eğer öneri yoksa kullanıcıya daha fazla detay verin dedik
#     return list(recommendations) if recommendations else ["Lütfen daha fazla detay verin."]
def analyze_skin_problem(text):
    """Kullanıcının cilt problemi hakkında öneriler sunar."""
    doc = nlp(text.lower())  # Metni küçük harfe çevir ve NLP analizi yap
    recommendations = set()  # Set kullanarak tekrarı önleyeceğiz
    ingredients = set()  # Kullanıcıya hangi bileşenlerin önerildiğini takip edeceğiz

    # Tüm anahtar kelimeler üzerinde döngü
    for problem, data in SKINCARE_KEYWORDS.items():
        for keyword in data:
            if any(re.search(r"\b" + re.escape(keyword) + r"\b", text.lower()) for keyword in SKINCARE_KEYWORDS[problem]):
                recommendations.add(SKINCARE_RULES[problem]["rule"])
                # İlgili bileşenleri öneriler listesine ekleyelim
                ingredients.update(SKINCARE_RULES[problem]["ingredients"])

    # İçerik uyumluğunu kontrol et
    incompatible = check_compatibility(list(ingredients))

    warning_message = ""
    # Uyumlu olmayan bileşenler varsa, kullanıcıya bildirelim
    if incompatible:
        incompatible_str = " and ".join(
            [f"'{item[0]}' with '{item[1]}'" for item in incompatible]
        )
        warning_message = (
            f"Warning: The following ingredients may not work well together: {incompatible_str}. "
            "You may consider using these ingredients at different times or avoid using one of them."
        )

    # İçeriği döndürelim
    return list(recommendations), list(ingredients), warning_message