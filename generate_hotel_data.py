import pandas as pd
import numpy as np
import random
import json
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# ── helpers ──────────────────────────────────────────────────────────────────

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

# ── CONFIG ───────────────────────────────────────────────────────────────────

N_GUESTS       = 600
START_DATE     = datetime(2023, 1, 1)
END_DATE       = datetime(2024, 12, 31)
HOTEL_NAME     = "The Magnolia Hotel"

FIRST_NAMES = [
    "James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda",
    "William","Barbara","David","Susan","Richard","Jessica","Joseph","Sarah",
    "Thomas","Karen","Charles","Lisa","Christopher","Nancy","Daniel","Betty",
    "Matthew","Margaret","Anthony","Sandra","Mark","Ashley","Donald","Dorothy",
    "Steven","Kimberly","Paul","Emily","Andrew","Donna","Joshua","Michelle",
    "Kenneth","Carol","Kevin","Amanda","Brian","Melissa","George","Deborah",
    "Timothy","Stephanie","Ronald","Rebecca","Edward","Sharon","Jason","Laura",
    "Jeffrey","Cynthia","Ryan","Kathleen","Jacob","Amy","Gary","Angela",
    "Nicholas","Shirley","Eric","Anna","Jonathan","Brenda","Stephen","Pamela",
    "Larry","Emma","Justin","Nicole","Scott","Helen","Brandon","Samantha",
    "Benjamin","Katherine","Samuel","Christine","Raymond","Debra","Gregory","Rachel",
    "Frank","Carolyn","Alexander","Janet","Patrick","Maria","Jack","Heather",
    "Dennis","Diane","Jerry","Julie"
]

LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson",
    "Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson",
    "White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker",
    "Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell",
    "Carter","Roberts"
]

CITIES = [
    ("New York","NY","Northeast"),("Los Angeles","CA","West"),
    ("Chicago","IL","Midwest"),("Houston","TX","South"),
    ("Phoenix","AZ","West"),("Philadelphia","PA","Northeast"),
    ("San Antonio","TX","South"),("San Diego","CA","West"),
    ("Dallas","TX","South"),("San Jose","CA","West"),
    ("Atlanta","GA","South"),("Austin","TX","South"),
    ("Nashville","TN","South"),("Charlotte","NC","South"),
    ("Denver","CO","West"),("Seattle","WA","West"),
    ("Boston","MA","Northeast"),("Miami","FL","South"),
    ("Minneapolis","MN","Midwest"),("Portland","OR","West"),
    ("London","UK","International"),("Toronto","ON","International"),
    ("Mexico City","MX","International"),("Sydney","AU","International"),
]

DIETARY_FLAGS = ["None","Vegetarian","Vegan","Gluten-Free","Halal","Kosher","Dairy-Free","Nut Allergy"]

ROOM_CATEGORIES = ["Standard","Deluxe","Junior Suite","Suite","Presidential Suite"]
ROOM_BASE_RATES = {"Standard":149,"Deluxe":199,"Junior Suite":279,"Suite":399,"Presidential Suite":699}

OUTLETS = ["Bar","Restaurant","Spa","Room Service","Minibar","Retail"]

FOOD_ITEMS = {
    "Bar": [
        ("Margarita",14),("Old Fashioned",16),("House Wine",13),("Craft Beer",10),
        ("Espresso Martini",17),("Mocktail",9),("Whiskey Neat",15),("Gin & Tonic",14),
        ("Aperol Spritz",15),("Negroni",16),("Bar Snack Platter",22),("Cheese Board",28),
    ],
    "Restaurant": [
        ("Breakfast Buffet",28),("Continental Breakfast",18),("Eggs Benedict",24),
        ("Club Sandwich",22),("Caesar Salad",19),("Ribeye Steak",58),
        ("Salmon Fillet",42),("Pasta Primavera",28),("Burger & Fries",26),
        ("Kids Meal",14),("Dessert",12),("Non-Alcoholic Beverage",6),("House Wine by Glass",15),
    ],
    "Spa": [
        ("60-Min Swedish Massage",120),("90-Min Deep Tissue",165),
        ("Couples Massage",240),("Facial Treatment",110),
        ("Manicure",55),("Pedicure",65),("Full Body Scrub",130),
        ("Day Pass",85),
    ],
    "Room Service": [
        ("Breakfast Plate",34),("Late Night Burger",38),("Club Sandwich",30),
        ("Cheese & Charcuterie",45),("Kids Breakfast",22),("Bottle of Wine",65),
        ("Beer (4-pack)",28),("Fruit Platter",24),("Caesar Salad",26),
        ("Fish & Chips",36),
    ],
    "Minibar": [
        ("Soft Drink",6),("Beer",9),("Miniature Spirits",14),
        ("Chocolate Bar",7),("Mixed Nuts",8),("Sparkling Water",5),
    ],
    "Retail": [
        ("Hotel Branded Robe",95),("Candle",45),("Sunscreen",18),
        ("Toothbrush Kit",12),("Branded Tote Bag",35),("Local Artisan Jam",22),
        ("Postcard Set",8),("Coffee Beans",28),
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# TABLE 1 — GUESTS
# ═══════════════════════════════════════════════════════════════════════════

def build_guests(n):
    rows = []
    for i in range(1, n + 1):
        generation = weighted_choice(
            ["Boomer","Gen X","Millennial","Gen Z"],
            [0.25, 0.25, 0.35, 0.15]
        )
        age = {
            "Boomer":   random.randint(60, 78),
            "Gen X":    random.randint(44, 59),
            "Millennial": random.randint(28, 43),
            "Gen Z":    random.randint(22, 27),
        }[generation]

        # booking channel skews by generation
        channel_weights = {
            "Boomer":     [0.45, 0.20, 0.25, 0.10],   # direct, OTA, corporate, travel agent
            "Gen X":      [0.35, 0.30, 0.28, 0.07],
            "Millennial": [0.30, 0.48, 0.18, 0.04],
            "Gen Z":      [0.22, 0.65, 0.10, 0.03],
        }[generation]
        booking_channel = weighted_choice(
            ["Direct","OTA","Corporate","Travel Agent"], channel_weights
        )

        # loyalty tier correlated with booking channel and repeat behaviour
        if booking_channel == "Direct":
            tier = weighted_choice(["None","Silver","Gold","Platinum"], [0.20, 0.30, 0.30, 0.20])
        elif booking_channel == "Corporate":
            tier = weighted_choice(["None","Silver","Gold","Platinum"], [0.15, 0.25, 0.35, 0.25])
        elif booking_channel == "OTA":
            tier = weighted_choice(["None","Silver","Gold","Platinum"], [0.60, 0.25, 0.10, 0.05])
        else:
            tier = weighted_choice(["None","Silver","Gold","Platinum"], [0.35, 0.30, 0.25, 0.10])

        total_visits = {
            "None": random.randint(1, 2),
            "Silver": random.randint(2, 5),
            "Gold": random.randint(4, 10),
            "Platinum": random.randint(8, 25),
        }[tier]

        repeat_guest = total_visits > 1

        # party composition skewed by generation and purpose
        if generation in ["Millennial","Gen X"] and random.random() < 0.45:
            party = "Family"
        elif generation == "Boomer" and random.random() < 0.30:
            party = "Family"
        else:
            party = weighted_choice(["Solo","Couple","Group"], [0.35, 0.45, 0.20])

        num_children = 0
        if party == "Family":
            num_children = random.randint(1, 3)

        city, state, market_region = random.choice(CITIES)
        market_type = "International" if market_region == "International" else \
                      weighted_choice(["Local","Regional","National"], [0.15, 0.35, 0.50])

        dietary = weighted_choice(DIETARY_FLAGS, [0.55,0.10,0.07,0.08,0.05,0.03,0.07,0.05])

        first = random.choice(FIRST_NAMES)
        last  = random.choice(LAST_NAMES)
        email = f"{first.lower()}.{last.lower()}{random.randint(1,999)}@example.com"

        rows.append({
            "guest_id":        f"G{i:04d}",
            "first_name":      first,
            "last_name":       last,
            "email":           email,
            "age":             age,
            "generation":      generation,
            "home_city":       city,
            "home_state":      state,
            "market_type":     market_type,
            "booking_channel": booking_channel,
            "loyalty_tier":    tier,
            "total_visits":    total_visits,
            "repeat_guest":    repeat_guest,
            "party_composition": party,
            "num_children":    num_children,
            "dietary_flag":    dietary,
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════
# TABLE 2 — RESERVATIONS
# ═══════════════════════════════════════════════════════════════════════════

def build_reservations(guests):
    rows = []
    res_id = 1
    for _, g in guests.iterrows():
        n_stays = g["total_visits"]
        for stay_num in range(1, n_stays + 1):
            checkin = rand_date(START_DATE, END_DATE)

            # purpose of travel
            if g["booking_channel"] == "Corporate":
                purpose = weighted_choice(["Business","Bleisure","Leisure"], [0.65, 0.25, 0.10])
            elif g["party_composition"] == "Family":
                purpose = weighted_choice(["Business","Bleisure","Leisure"], [0.05, 0.10, 0.85])
            else:
                purpose = weighted_choice(["Business","Bleisure","Leisure"], [0.25, 0.20, 0.55])

            # check-in day: business skews weekday, leisure skews weekend
            if purpose == "Business":
                checkin_day = weighted_choice(
                    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                    [0.22, 0.22, 0.22, 0.18, 0.10, 0.03, 0.03]
                )
            else:
                checkin_day = weighted_choice(
                    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                    [0.08, 0.07, 0.07, 0.10, 0.22, 0.28, 0.18]
                )

            # length of stay
            if purpose == "Business":
                los = random.randint(1, 3)
            elif purpose == "Bleisure":
                los = random.randint(2, 5)
            else:
                los = random.randint(2, 7)
            if g["party_composition"] == "Family":
                los = max(los, random.randint(3, 7))

            # lead time: OTA books later, direct and travel agent book earlier
            lead_map = {
                "Direct": (14, 90), "OTA": (1, 30),
                "Corporate": (3, 21), "Travel Agent": (21, 120),
            }
            lo, hi = lead_map[g["booking_channel"]]
            lead_time = random.randint(lo, hi)

            # room category: correlated with tier and party
            if g["loyalty_tier"] == "Platinum":
                room_cat = weighted_choice(ROOM_CATEGORIES, [0.05, 0.15, 0.25, 0.40, 0.15])
            elif g["loyalty_tier"] == "Gold":
                room_cat = weighted_choice(ROOM_CATEGORIES, [0.15, 0.30, 0.30, 0.20, 0.05])
            elif g["party_composition"] == "Family":
                room_cat = weighted_choice(ROOM_CATEGORIES, [0.10, 0.35, 0.35, 0.18, 0.02])
            elif g["booking_channel"] == "OTA":
                room_cat = weighted_choice(ROOM_CATEGORIES, [0.45, 0.35, 0.15, 0.04, 0.01])
            else:
                room_cat = weighted_choice(ROOM_CATEGORIES, [0.30, 0.35, 0.20, 0.12, 0.03])

            base_rate = ROOM_BASE_RATES[room_cat]

            # rate type
            if g["booking_channel"] == "Corporate":
                rate_type = "Corporate Rate"
                rate = round(base_rate * random.uniform(0.80, 0.90), 2)
            elif g["booking_channel"] == "OTA":
                rate_type = "OTA Rate"
                rate = round(base_rate * random.uniform(0.92, 1.05), 2)
            elif g["loyalty_tier"] in ["Gold","Platinum"]:
                rate_type = weighted_choice(["Loyalty Rate","BAR","Package"], [0.50, 0.30, 0.20])
                rate = round(base_rate * random.uniform(0.85, 0.95), 2)
            else:
                rate_type = weighted_choice(["BAR","Package","Promotional"], [0.60, 0.25, 0.15])
                rate = round(base_rate * random.uniform(0.95, 1.10), 2)

            room_revenue = round(rate * los, 2)

            # satisfaction: OTA guests rate lower; higher tier guests rate higher
            base_sat = {"None":6.8,"Silver":7.2,"Gold":7.8,"Platinum":8.4}[g["loyalty_tier"]]
            if g["booking_channel"] == "OTA":
                base_sat -= 0.5
            if stay_num > 1:           # repeat guests trend higher
                base_sat += 0.3
            sat_score = round(min(10, max(1, np.random.normal(base_sat, 0.8))), 1)

            if sat_score >= 9:
                nps = "Promoter"
            elif sat_score >= 7:
                nps = "Passive"
            else:
                nps = "Detractor"

            # rebooked direct after a great stay?
            rebooked_direct = (sat_score >= 8.5) and (random.random() < 0.55)

            rows.append({
                "reservation_id":  f"R{res_id:05d}",
                "guest_id":        g["guest_id"],
                "stay_number":     stay_num,
                "checkin_date":    checkin.strftime("%Y-%m-%d"),
                "checkin_day":     checkin_day,
                "length_of_stay":  los,
                "lead_time_days":  lead_time,
                "purpose":         purpose,
                "room_category":   room_cat,
                "rate_type":       rate_type,
                "nightly_rate":    rate,
                "room_revenue":    room_revenue,
                "satisfaction_score": sat_score,
                "nps":             nps,
                "rebooked_direct": rebooked_direct,
            })
            res_id += 1

    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════
# TABLE 3 — TRANSACTIONS  (the outlet / POS data)
# ═══════════════════════════════════════════════════════════════════════════

def pick_items(outlet, n):
    pool = FOOD_ITEMS[outlet]
    chosen = random.choices(pool, k=n)
    return chosen   # list of (name, price) tuples

def build_transactions(reservations, guests):
    guest_lookup = guests.set_index("guest_id").to_dict("index")
    rows = []
    txn_id = 1

    for _, res in reservations.iterrows():
        g      = guest_lookup[res["guest_id"]]
        los    = res["length_of_stay"]
        party  = g["party_composition"]
        tier   = g["loyalty_tier"]
        kids   = g["num_children"]
        purpose = res["purpose"]
        room_cat = res["room_category"]

        # ── spend propensity multipliers ──────────────────────────────────
        tier_mult = {"None":0.85,"Silver":1.0,"Gold":1.15,"Platinum":1.35}[tier]
        room_mult = {"Standard":0.80,"Deluxe":1.0,"Junior Suite":1.15,
                     "Suite":1.30,"Presidential Suite":1.60}[room_cat]

        # BAR
        # Business travellers drink more at the bar; families less
        bar_nights = 0
        if purpose == "Business":
            bar_nights = random.randint(1, los)
        elif party == "Family":
            bar_nights = random.randint(0, max(1, los // 3))
        else:
            bar_nights = random.randint(0, los)

        for night in range(bar_nights):
            drinks_per_session = random.randint(2, 6)
            # skew bar spend to Friday/Saturday — simplified: late-week nights
            day_of_stay = random.randint(1, los)
            time_of_day = f"{random.randint(17,23):02d}:{random.choice(['00','15','30','45'])}"
            items = pick_items("Bar", drinks_per_session)
            for item_name, item_price in items:
                amount = round(item_price * random.uniform(0.95, 1.05) * tier_mult, 2)
                rows.append({
                    "transaction_id":   f"T{txn_id:06d}",
                    "reservation_id":   res["reservation_id"],
                    "guest_id":         res["guest_id"],
                    "outlet":           "Bar",
                    "item":             item_name,
                    "amount":           amount,
                    "day_of_stay":      day_of_stay,
                    "time_of_day":      time_of_day,
                    "charged_to_room":  random.random() < 0.75,
                })
                txn_id += 1

        # RESTAURANT
        # Families eat breakfast at restaurant; business skips; leisure varies
        restaurant_visits = 0
        if party == "Family":
            restaurant_visits = random.randint(los, los * 2)   # breakfast + some dinners
        elif purpose == "Business":
            restaurant_visits = random.randint(0, los // 2)
        else:
            restaurant_visits = random.randint(los // 2, los)

        for _ in range(restaurant_visits):
            n_items = random.randint(1, 4) + (1 if kids > 0 else 0)
            items = pick_items("Restaurant", n_items)
            day_of_stay = random.randint(1, los)
            # breakfast skews 7-10am, dinner 18-21
            meal = weighted_choice(["Breakfast","Dinner"], [0.55, 0.45])
            if meal == "Breakfast":
                time_of_day = f"{random.randint(7,10):02d}:{random.choice(['00','15','30','45'])}"
            else:
                time_of_day = f"{random.randint(18,21):02d}:{random.choice(['00','15','30','45'])}"

            for item_name, item_price in items:
                amount = round(item_price * random.uniform(0.95, 1.05) * tier_mult, 2)
                rows.append({
                    "transaction_id":   f"T{txn_id:06d}",
                    "reservation_id":   res["reservation_id"],
                    "guest_id":         res["guest_id"],
                    "outlet":           "Restaurant",
                    "item":             item_name,
                    "amount":           amount,
                    "day_of_stay":      day_of_stay,
                    "time_of_day":      time_of_day,
                    "charged_to_room":  random.random() < 0.70,
                })
                txn_id += 1

        # SPA
        # Leisure and higher tiers use spa more; families with kids use spa less
        spa_prob = 0.15
        if purpose == "Leisure":
            spa_prob += 0.25
        if tier in ["Gold","Platinum"]:
            spa_prob += 0.20
        if room_cat in ["Suite","Presidential Suite"]:
            spa_prob += 0.15
        if kids > 0:
            spa_prob -= 0.20
        spa_prob = max(0, min(1, spa_prob))

        spa_visits = np.random.binomial(los, spa_prob * 0.4)
        for _ in range(spa_visits):
            items = pick_items("Spa", 1)
            item_name, item_price = items[0]
            amount = round(item_price * room_mult * random.uniform(0.95, 1.05), 2)
            time_of_day = f"{random.randint(9,17):02d}:{random.choice(['00','30'])}"
            rows.append({
                "transaction_id":   f"T{txn_id:06d}",
                "reservation_id":   res["reservation_id"],
                "guest_id":         res["guest_id"],
                "outlet":           "Spa",
                "item":             item_name,
                "amount":           amount,
                "day_of_stay":      random.randint(1, los),
                "time_of_day":      time_of_day,
                "charged_to_room":  random.random() < 0.85,
            })
            txn_id += 1

        # ROOM SERVICE
        # Families order room service heavily (kids' breakfasts, late nights)
        # Business travellers order occasional late-night
        if party == "Family":
            rs_orders = random.randint(los, los * 2)
        elif purpose == "Business":
            rs_orders = random.randint(0, los)
        else:
            rs_orders = random.randint(0, los // 2)

        for _ in range(rs_orders):
            n_items = random.randint(1, 3) + (kids if kids > 0 else 0)
            n_items = min(n_items, 5)
            items = pick_items("Room Service", n_items)
            # room service skews early morning or late night
            slot = weighted_choice(["Morning","LateNight"], [0.55, 0.45])
            if slot == "Morning":
                time_of_day = f"{random.randint(6,9):02d}:{random.choice(['00','30'])}"
            else:
                time_of_day = f"{random.randint(21,23):02d}:{random.choice(['00','30'])}"

            for item_name, item_price in items:
                amount = round(item_price * random.uniform(0.95, 1.05) * tier_mult, 2)
                rows.append({
                    "transaction_id":   f"T{txn_id:06d}",
                    "reservation_id":   res["reservation_id"],
                    "guest_id":         res["guest_id"],
                    "outlet":           "Room Service",
                    "item":             item_name,
                    "amount":           amount,
                    "day_of_stay":      random.randint(1, los),
                    "time_of_day":      time_of_day,
                    "charged_to_room":  True,
                })
                txn_id += 1

        # MINIBAR
        minibar_hits = random.randint(0, los)
        for _ in range(minibar_hits):
            items = pick_items("Minibar", random.randint(1, 3))
            for item_name, item_price in items:
                amount = round(item_price * random.uniform(0.95, 1.05), 2)
                rows.append({
                    "transaction_id":   f"T{txn_id:06d}",
                    "reservation_id":   res["reservation_id"],
                    "guest_id":         res["guest_id"],
                    "outlet":           "Minibar",
                    "item":             item_name,
                    "amount":           amount,
                    "day_of_stay":      random.randint(1, los),
                    "time_of_day":      f"{random.randint(20,23):02d}:00",
                    "charged_to_room":  True,
                })
                txn_id += 1

        # RETAIL
        retail_prob = 0.10
        if party == "Family":
            retail_prob += 0.20
        if tier in ["Gold","Platinum"]:
            retail_prob += 0.10
        if purpose == "Leisure":
            retail_prob += 0.10

        if random.random() < retail_prob:
            items = pick_items("Retail", random.randint(1, 3))
            for item_name, item_price in items:
                amount = round(item_price * random.uniform(0.95, 1.05), 2)
                rows.append({
                    "transaction_id":   f"T{txn_id:06d}",
                    "reservation_id":   res["reservation_id"],
                    "guest_id":         res["guest_id"],
                    "outlet":           "Retail",
                    "item":             item_name,
                    "amount":           amount,
                    "day_of_stay":      random.randint(1, los),
                    "time_of_day":      f"{random.randint(10,18):02d}:00",
                    "charged_to_room":  random.random() < 0.50,
                })
                txn_id += 1

    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════
# BUILD + SAVE
# ═══════════════════════════════════════════════════════════════════════════

print("Building guests table...")
guests = build_guests(N_GUESTS)

print("Building reservations table...")
reservations = build_reservations(guests, )

print("Building transactions table...")
transactions = build_transactions(reservations, guests)

# save
guests.to_csv("/mnt/user-data/outputs/guests.csv", index=False)
reservations.to_csv("/mnt/user-data/outputs/reservations.csv", index=False)
transactions.to_csv("/mnt/user-data/outputs/transactions.csv", index=False)

# ── summary ──────────────────────────────────────────────────────────────────
print("\n── Dataset Summary ───────────────────────────────────────────────")
print(f"  Guests:        {len(guests):,}")
print(f"  Reservations:  {len(reservations):,}")
print(f"  Transactions:  {len(transactions):,}")

total_room_rev = reservations["room_revenue"].sum()
total_fb_rev   = transactions[transactions["outlet"].isin(["Bar","Restaurant","Room Service","Minibar"])]["amount"].sum()
total_spa_rev  = transactions[transactions["outlet"] == "Spa"]["amount"].sum()
total_retail   = transactions[transactions["outlet"] == "Retail"]["amount"].sum()
total_rev      = total_room_rev + total_fb_rev + total_spa_rev + total_retail

print(f"\n  Total room revenue:  ${total_room_rev:,.0f}")
print(f"  Total F&B revenue:   ${total_fb_rev:,.0f}")
print(f"  Total spa revenue:   ${total_spa_rev:,.0f}")
print(f"  Total retail:        ${total_retail:,.0f}")
print(f"  Total revenue:       ${total_rev:,.0f}")

print(f"\n  Avg nightly rate:    ${reservations['nightly_rate'].mean():.2f}")
print(f"  Avg length of stay:  {reservations['length_of_stay'].mean():.1f} nights")
print(f"  Avg satisfaction:    {reservations['satisfaction_score'].mean():.1f}/10")

print("\n  Loyalty tier breakdown:")
print(guests["loyalty_tier"].value_counts().to_string())

print("\n  Booking channel breakdown:")
print(guests["booking_channel"].value_counts().to_string())

print("\n  Party composition:")
print(guests["party_composition"].value_counts().to_string())

print("\n  Outlet revenue breakdown:")
print(transactions.groupby("outlet")["amount"].sum().sort_values(ascending=False).apply(lambda x: f"${x:,.0f}").to_string())
print("\n✓ All files saved to /mnt/user-data/outputs/")
