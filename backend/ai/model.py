import spacy
import re


# NLP modelini yükleyelim
nlp = spacy.load("en_core_web_sm")

# Anahtar kelimeler ve cilt bakım sorunlarına yönelik kurallar
SKINCARE_KEYWORDS = {
    "sensitive": ["sensitive", "irritated", "reactive", "allergic", "itchy"],
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
        "rule": "For sensitive skin, prioritize gentle, barrier-repairing ingredients. Use mild cleansers like micellar water or cream-based formulas. Look for soothing agents such as aloe vera, centella asiatica, chamomile, and oat extract. Hydration is key, so incorporate ceramides, glycerin, and hyaluronic acid.",
        "ingredients": [
            "ceramides", "glycerin", "hyaluronic acid", "aloe vera", 
            "centella asiatica", "chamomile", "oat extract", 
            "micellar water", "cream cleanser"
        ],
        "avoid": [
            "alcohol", "fragrance", "harsh exfoliants", "sulfates", "essential oils"
        ]
    },
    "acne_prone": {
        "rule": "For acne-prone skin, use antibacterial and oil-regulating ingredients. Salicylic acid (BHA) helps unclog pores, while benzoyl peroxide fights acne-causing bacteria. Retinoids (retinol, adapalene) accelerate cell turnover to prevent breakouts. Niacinamide reduces inflammation and controls sebum. Stick to non-comedogenic, lightweight formulas.",
        "ingredients": [
            "salicylic acid", "benzoyl peroxide", "retinol", "adapalene", 
            "niacinamide", "tea tree oil", "witch hazel", "zinc"
        ],
        "avoid": [
            "heavy oils", "coconut oil", "shea butter", "alcohol", "fragrance", "occlusive ingredients"
        ]
    },
    "dry": {
        "rule": "For dry skin, focus on deep hydration and moisture retention. Use rich moisturizers with ceramides, hyaluronic acid, and glycerin. Oils like jojoba, argan, and rosehip provide nourishment. Avoid harsh cleansers and opt for hydrating serums. Occlusives like petrolatum and shea butter help lock in moisture.",
        "ingredients": [
            "ceramides", "hyaluronic acid", "glycerin", "squalane", 
            "jojoba oil", "argan oil", "rosehip oil", 
            "petrolatum", "shea butter", "hydrating serums"
        ],
        "avoid": [
            "foaming cleansers", "alcohol-based toners", "strong exfoliants", "clay masks"
        ]
    },
    "oily": {
        "rule": "For oily skin, choose lightweight, oil-controlling products. Water-based moisturizers and gel cleansers are ideal. Niacinamide regulates oil production, while salicylic acid keeps pores clear. Tea tree oil and witch hazel help reduce excess shine. Avoid heavy creams and comedogenic oils.",
        "ingredients": [
            "niacinamide", "salicylic acid", "tea tree oil", 
            "witch hazel", "zinc", "water-based moisturizers", 
            "gel-based cleansers"
        ],
        "avoid": [
            "heavy oils", "coconut oil", "thick creams", "alcohol", "sulfates"
        ]
    },
    "combination": {
        "rule": "For combination skin, balance hydration and oil control. Use lightweight moisturizers and hydrating serums. Niacinamide and lactic acid help regulate oil in the T-zone while maintaining moisture for dry areas. Multi-masking can target different skin concerns simultaneously.",
        "ingredients": [
            "hyaluronic acid", "niacinamide", "lactic acid", 
            "gentle exfoliants", "lightweight moisturizers"
        ],
        "avoid": [
            "harsh cleansers", "alcohol", "heavy occlusives", "strong acids"
        ]
    },
    "hyperpigmentation": {
        "rule": "For hyperpigmentation, focus on brightening and exfoliating ingredients. Vitamin C and niacinamide help even out skin tone, while alpha arbutin and tranexamic acid reduce dark spots. AHAs like glycolic acid and lactic acid promote cell turnover. Daily SPF is essential to prevent further discoloration.",
        "ingredients": [
            "vitamin C", "ascorbic acid", "niacinamide", 
            "alpha arbutin", "tranexamic acid", "licorice root extract", 
            "glycolic acid", "lactic acid", "sunscreen"
        ],
        "avoid": [
            "harsh physical scrubs", "alcohol", "fragrance", "lemon juice", "essential oils"
        ]
    },
    "aging": {
        "rule": "For aging skin, use collagen-boosting and antioxidant-rich ingredients. Retinoids (retinol, tretinoin) are key for reducing fine lines. Peptides, vitamin C, and vitamin E improve skin texture and firmness. Hydrating agents like hyaluronic acid and ceramides help maintain skin elasticity.",
        "ingredients": [
            "retinol", "tretinoin", "peptides", "vitamin C", 
            "vitamin E", "niacinamide", "hyaluronic acid", "ceramides"
        ],
        "avoid": [
            "harsh exfoliants", "alcohol", "fragrance", "over-exfoliation"
        ]
    },
    "rosacea": {
        "rule": "For rosacea-prone skin, opt for soothing, anti-inflammatory ingredients. Azelaic acid reduces redness, while niacinamide, green tea extract, and colloidal oatmeal calm irritation. Avoid harsh exfoliants, alcohol, and fragrance, which can trigger flare-ups.",
        "ingredients": [
            "azelaic acid", "niacinamide", "green tea extract", "colloidal oatmeal"
        ],
        "avoid": [
            "alcohol", "fragrance", "menthol", "eucalyptus oil", "harsh exfoliants"
        ]
    },
    "eczema": {
        "rule": "For eczema, focus on barrier-strengthening and soothing ingredients. Ceramides and fatty acids help repair the skin. Use fragrance-free, hypoallergenic products. Rich occlusive moisturizers like petrolatum and shea butter prevent water loss and soothe irritation.",
        "ingredients": [
            "ceramides", "fatty acids", "colloidal oatmeal", 
            "fragrance-free products", "petrolatum", "shea butter"
        ],
        "avoid": [
            "fragrance", "essential oils", "alcohol", "harsh cleansers", "sulfates"
        ]
    },
    "sun_damage": {
        "rule": "For sun-damaged skin, prioritize antioxidants and repair agents. Vitamin C, E, and niacinamide help reverse damage, while ceramides and peptides strengthen the skin barrier. Daily sunscreen with SPF 30 or higher is crucial to prevent further harm.",
        "ingredients": [
            "vitamin C", "vitamin E", "niacinamide", 
            "ceramides", "peptides", "sunscreen"
        ],
        "avoid": [
            "alcohol", "fragrance", "harsh exfoliants", "unprotected sun exposure"
        ]
    }
}


# Cilt bakım bileşenlerinin uyumsuzlukları
INCOMPATIBLE_INGREDIENTS = {
    "retinol": ["salicylic acid", "benzoyl peroxide", "vitamin C", "adapalene"],
    "salicylic acid": ["retinol", "benzoyl peroxide", "adapalene"],
    "benzoyl peroxide": ["retinol", "salicylic acid", "adapalene"],
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


def analyze_skin_problem(text):
    """Kullanıcının cilt problemi hakkında öneriler sunar."""
    doc = nlp(text.lower())  # Metni küçük harfe çevir ve NLP analizi yap
    recommendations = set()  # Set kullanarak tekrarı önleyeceğiz
    ingredients = set()  # Kullanıcıya hangi bileşenlerin önerildiğini takip edeceğiz
    avoid= set()

    # Tüm anahtar kelimeler üzerinde döngü
    for problem, data in SKINCARE_KEYWORDS.items():
        for keyword in data:
            if any(re.search(r"\b" + re.escape(keyword) + r"\b", text.lower()) for keyword in SKINCARE_KEYWORDS[problem]):
                recommendations.add(SKINCARE_RULES[problem]["rule"])
                # İlgili bileşenleri öneriler listesine ekleyelim
                ingredients.update(SKINCARE_RULES[problem]["ingredients"])
                avoid.update(SKINCARE_RULES[problem]["avoid"])

    # İçerik uyumluğunu kontrol et
    incompatible = check_compatibility(list(ingredients))

    warning_message = ""
   

    if incompatible:
    # Tekrar eden öğeleri silmek için set kullanıyoruz, önce her çiftin bileşenlerini sıralıyoruz
        unique_incompatible = set(
            tuple(sorted(item)) for item in incompatible
        )
        
        # HTML formatında uyumsuz bileşen çiftlerini listelemek
        incompatible_str = "<br>".join(
            [f"'{item[0]}' & '{item[1]}'" for item in unique_incompatible]
        )
        
        warning_message = (
            f"Uyarı: Aşağıdaki bileşenler birlikte kullanıldığında uyumsuz olabilir:<br><br>"
            f"{incompatible_str}<br><br>"
            "Bu bileşenleri farklı zamanlarda kullanmayı ya da birini kullanmamayı düşünebilirsiniz."
        )


    # İçeriği döndürelim
    return list(recommendations), list(ingredients), list(avoid), warning_message