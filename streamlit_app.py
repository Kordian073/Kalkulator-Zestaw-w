import itertools
import streamlit as st

# Funkcja sprawdzająca, czy zestaw można stworzyć
def can_create_set(set_parts, available):
    for part, amount in set_parts.items():
        if part in available and available[part] < amount:
            return False
    return True

# Funkcja do odjęcia części zużytych do zestawu
def use_parts(set_parts, available):
    for part, amount in set_parts.items():
        if part in available:
            available[part] -= amount

# Funkcja do znajdowania optymalnego ułożenia zestawów
def find_optimal_order(available_parts, boss_sets):
    max_sets = 0
    best_order = None
    best_remaining = None
    used_sets = []

    for order in itertools.permutations(boss_sets):
        temp_available = available_parts.copy()
        temp_constructed = 0
        temp_used_sets = []

        for set_parts in order:
            set_parts_without_esek = {k: v for k, v in set_parts.items() if k != "esek"}
            while can_create_set(set_parts_without_esek, temp_available):
                temp_constructed += 1
                temp_used_sets.append(set_parts)
                use_parts(set_parts_without_esek, temp_available)

        if temp_constructed > max_sets:
            max_sets = temp_constructed
            best_order = order
            best_remaining = temp_available.copy()
            used_sets = temp_used_sets

    return max_sets, best_order, best_remaining, used_sets

# Interfejs Streamlit
st.title("🧮 Kalkulator Zestawów")
st.write("Podaj ilość części, a kalkulator znajdzie optymalne ułożenie zestawów dla bossa.")

eov = st.number_input("Ilość Eov", min_value=0)
nov = st.number_input("Ilość Nov", min_value=0)
voe = st.number_input("Ilość Voe", min_value=0)
vii = st.number_input("Ilość Vii", min_value=0)

if st.button("Oblicz"):
    available_parts = {
        "eov": eov,
        "nov": nov,
        "voe": voe,
        "vii": vii
    }

    boss_sets = [
        {"vii": 2, "voe": 2, "eov": 10},
        {"nov": 2, "eov": 2, "esek": 10},
        {"vii": 1, "voe": 2, "eov": 1, "esek": 10},
        {"vii": 1, "nov": 2, "eov": 1, "esek": 10},
        {"vii": 2, "nov": 1, "voe": 1, "esek": 10},
        {"nov": 1, "eov": 2, "voe": 1, "esek": 10}
    ]

    max_sets, best_order, best_remaining, used_sets = find_optimal_order(available_parts, boss_sets)

    st.success(f"🔢 Maksymalna liczba zestawów: {max_sets}")
    st.write("📦 Pozostałości części:")
    for part, amount in best_remaining.items():
        st.write(f"- {part}: {amount}")

    st.write("🛠️ Zestawy do wrzucenia do bossa:")
    for i, used_set in enumerate(used_sets, 1):
        st.write(f"  Zestaw {i}: {used_set}")
