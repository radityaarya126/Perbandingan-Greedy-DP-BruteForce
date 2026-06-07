from itertools import combinations
import time

# ==================================================
# DATASET (15 TEMPAT)
# ==================================================

places = [
    {"id":"T1","name":"Tempat 1","cost":15000,"distance":1,"duration":1,"satisfaction":20},
    {"id":"T2","name":"Tempat 2","cost":25000,"distance":2,"duration":2,"satisfaction":35},
    {"id":"T3","name":"Tempat 3","cost":35000,"distance":4,"duration":2,"satisfaction":50},
    {"id":"T4","name":"Tempat 4","cost":20000,"distance":2,"duration":1,"satisfaction":30},
    {"id":"T5","name":"Tempat 5","cost":45000,"distance":5,"duration":3,"satisfaction":60},
    {"id":"T6","name":"Tempat 6","cost":30000,"distance":3,"duration":2,"satisfaction":45},
    {"id":"T7","name":"Tempat 7","cost":18000,"distance":1,"duration":1,"satisfaction":25},
    {"id":"T8","name":"Tempat 8","cost":50000,"distance":6,"duration":3,"satisfaction":70},
    {"id":"T9","name":"Tempat 9","cost":22000,"distance":2,"duration":1,"satisfaction":32},
    {"id":"T10","name":"Tempat 10","cost":40000,"distance":4,"duration":2,"satisfaction":55},
    {"id":"T11","name":"Tempat 11","cost":28000,"distance":3,"duration":2,"satisfaction":42},
    {"id":"T12","name":"Tempat 12","cost":35000,"distance":5,"duration":2,"satisfaction":48},
    {"id":"T13","name":"Tempat 13","cost":17000,"distance":1,"duration":1,"satisfaction":24},
    {"id":"T14","name":"Tempat 14","cost":55000,"distance":7,"duration":3,"satisfaction":75},
    {"id":"T15","name":"Tempat 15","cost":26000,"distance":2,"duration":2,"satisfaction":38}
]

# ==================================================
# NILAI TEMPAT
# Mempertimbangkan kepuasan dan jarak
# ==================================================

def get_value(place):
    return place["satisfaction"] - place["distance"]

# ==================================================
# GREEDY
# ==================================================

def greedy(places, max_budget, max_time):

    sorted_places = sorted(
        places,
        key=lambda x: get_value(x) / x["cost"],
        reverse=True
    )

    selected = []
    total_cost = 0
    total_time = 0
    total_value = 0

    for place in sorted_places:

        if (total_cost + place["cost"] <= max_budget and
            total_time + place["duration"] <= max_time):

            selected.append(place)

            total_cost += place["cost"]
            total_time += place["duration"]
            total_value += get_value(place)

    return selected, total_cost, total_time, total_value

# ==================================================
# BRUTE FORCE
# ==================================================

def brute_force(places, max_budget, max_time):

    best_solution = []
    best_value = 0
    best_cost = 0
    best_time = 0

    n = len(places)

    for r in range(n + 1):

        for subset in combinations(places, r):

            total_cost = sum(x["cost"] for x in subset)
            total_time = sum(x["duration"] for x in subset)
            total_value = sum(get_value(x) for x in subset)

            if total_cost <= max_budget and total_time <= max_time:

                if total_value > best_value:

                    best_solution = subset
                    best_value = total_value
                    best_cost = total_cost
                    best_time = total_time

    return best_solution, best_cost, best_time, best_value

# ==================================================
# DYNAMIC PROGRAMMING
# ==================================================

def dynamic_programming(places, max_budget, max_time):

    n = len(places)

    dp = [[[0 for _ in range(max_time + 1)]
           for _ in range(max_budget + 1)]
           for _ in range(n + 1)]

    for i in range(1, n + 1):

        cost = places[i - 1]["cost"]
        duration = places[i - 1]["duration"]
        value = get_value(places[i - 1])

        for b in range(max_budget + 1):

            for t in range(max_time + 1):

                dp[i][b][t] = dp[i - 1][b][t]

                if b >= cost and t >= duration:

                    dp[i][b][t] = max(
                        dp[i][b][t],
                        dp[i - 1][b - cost][t - duration] + value
                    )

    selected = []
    b = max_budget
    t = max_time

    for i in range(n, 0, -1):

        if dp[i][b][t] != dp[i - 1][b][t]:

            selected.append(places[i - 1])

            b -= places[i - 1]["cost"]
            t -= places[i - 1]["duration"]

    selected.reverse()

    total_cost = sum(x["cost"] for x in selected)
    total_time = sum(x["duration"] for x in selected)
    total_value = sum(get_value(x) for x in selected)

    return selected, total_cost, total_time, total_value

# ==================================================
# TAMPILKAN HASIL
# ==================================================

def print_result(name, result, exec_time):

    selected, cost, duration, value = result

    print(f"\n{name}")
    print("-" * 50)

    print("Tempat Terpilih:")

    for item in selected:
        print(
            f"{item['id']} | "
            f"Biaya={item['cost']} | "
            f"Jarak={item['distance']} km | "
            f"Durasi={item['duration']} jam | "
            f"Kepuasan={item['satisfaction']}"
        )

    print(f"\nTotal Biaya    : Rp{cost:,}")
    print(f"Total Durasi   : {duration} jam")
    print(f"Total Nilai    : {value}")
    print(f"Waktu Eksekusi : {exec_time:.6f} ms")

# ==================================================
# SKENARIO PENGUJIAN
# SESUAI METODOLOGI
# ==================================================

scenarios = [

    {
        "name": "SKENARIO 1",
        "places": places[:5],
        "budget": 50000,
        "time": 3
    },

    {
        "name": "SKENARIO 2",
        "places": places[:10],
        "budget": 100000,
        "time": 5
    },

    {
        "name": "SKENARIO 3",
        "places": places[:15],
        "budget": 150000,
        "time": 8
    }
]

# ==================================================
# EKSEKUSI SEMUA SKENARIO
# ==================================================

for scenario in scenarios:

    print("\n")
    print("=" * 60)
    print(scenario["name"])
    print("=" * 60)

    data = scenario["places"]
    budget = scenario["budget"]
    max_time = scenario["time"]

    start = time.perf_counter()
    greedy_result = greedy(data, budget, max_time)
    greedy_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    dp_result = dynamic_programming(data, budget, max_time)
    dp_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    bf_result = brute_force(data, budget, max_time)
    bf_time = (time.perf_counter() - start) * 1000

    print_result("GREEDY", greedy_result, greedy_time)
    print_result("DYNAMIC PROGRAMMING", dp_result, dp_time)
    print_result("BRUTE FORCE", bf_result, bf_time)