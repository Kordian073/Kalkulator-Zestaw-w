import itertools
import streamlit as st

# 🎨 Stylizacja nagłówka
st.markdown(
    """
    <div style="background-color:#6c4b2a; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: #f5f5dc; font-family: 'Trebuchet MS', sans-serif;">🍺 Browar Of Taern 🍺</h1>
        <p style="color: #f5f5dc; font-size: 18px;">Optymalny kalkulator zestawów dla najlepszej gildii!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔧 Funkcja sprawdzająca, czy zestaw można stworzyć
def can_create_set(set_parts, available):
    for part, amount in set_parts.items():
        if part in available and available[part] < amount:
            return False
    return True

# 🔧 Funkcja do odjęcia części zużytych do zestawu
def use_parts(set_parts, available):
    for part, amount in set_parts.items():
        if part in available:
            available[part] -= amount

# 🔧 Funkcja do znajdowania optymalnego ułożenia zestawów
def find_optimal_order(available_parts, boss_sets):
    max_sets = 0
    best_order = None
    best_remaining = None
    used_counts = {i + 1: 0 for i in range(len(boss_sets))}

    for order in itertools.permutations(enumerate(boss_sets, start=1)):
        temp_available = available_parts.copy()
        temp_constructed = 0
        temp_counts = {i + 1: 0 for i in range(len(boss_sets))}

        for sarkofag_id, set_parts in order:
            set_parts_without_esek = {k: v for k, v in set_parts.items() if k != "esek"}
            while can_create_set(set_parts_without_esek, temp_available):
                temp_constructed += 1
                temp_counts[sarkofag_id] += 1
                use_parts(set_parts_without_esek, temp_available)

        if temp_constructed > max_sets:
            max_sets = temp_constructed
            best_order = order
            best_remaining = temp_available.copy()
            used_counts = temp_counts.copy()

    return max_sets, best_order, best_remaining, used_counts

# 🧮 Interfejs użytkownika
st.title("🧮 Kalkulator Zestawów")
st.write("Podaj ilość części, a kalkulator znajdzie optymalne ułożenie zestawów dla bossów (sarkofagów).")

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

    # 💀 Definicje sarkofagów
    boss_sets = [
        {"vii": 2, "voe": 2, "esek": 10},           # 1 sarkofag
        {"eov": 2, "nov": 2, "esek": 10},           # 2 sarkofag
        {"eov": 1, "vii": 1, "voe": 2, "esek": 10}, # 3 sarkofag
        {"eov": 1, "nov": 2, "vii": 1, "esek": 10}, # 4 sarkofag
        {"nov": 1, "vii": 2, "voe": 1, "esek": 10}, # 5 sarkofag
        {"eov": 2, "nov": 1, "voe": 1, "esek": 10}  # 6 sarkofag
    ]

    max_sets, best_order, best_remaining, used_counts = find_optimal_order(available_parts, boss_sets)

    st.success(f"🔢 Maksymalna liczba wszystkich zestawów: {max_sets}")
    st.write("📦 Pozostałości części:")
    for part, amount in best_remaining.items():
        st.write(f"- {part}: {amount}")

    st.write("🪦 Liczba stworzonych sarkofagów:")
    for i, count in used_counts.items():
        st.write(f"➡️ Sarkofag {i}: **{count}x**")
