"""The lab's sample data: grocery items to store and search in Chroma."""

GROCERY_ITEMS = [
    "fresh red apples",
    "organic bananas",
    "ripe mangoes",
    "whole wheat bread",
    "farm-fresh eggs",
    "natural yogurt",
    "frozen vegetables",
    "grass-fed beef",
    "free-range chicken",
    "fresh salmon fillet",
    "aromatic coffee beans",
    "pure honey",
    "golden apple",
    "red fruit",
]

# One unique id per item: food_1, food_2, ...
GROCERY_IDS = [f"food_{number}" for number in range(1, len(GROCERY_ITEMS) + 1)]

# Every item shares the same metadata
GROCERY_METADATAS = [{"source": "grocery_store", "category": "food"} for _ in GROCERY_ITEMS]
