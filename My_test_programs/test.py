from collections import defaultdict

categories = ["aa_bb","aa_cc","aa_dd","bb_ee","bb_ff","bb_gg"]
subcategories = defaultdict(list)
for category in set(cat.split("_")[0] for cat in categories):
    subcategories[category].extend(
        [subcat for subcat in categories if subcat.startswith(category)]
    )