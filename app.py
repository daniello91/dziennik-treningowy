import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(page_title="🏃♂️ Dziennik Treningowy", layout="centered")

st.title("🏃♂️ Dziennik Treningowy – 8 tygodni")

# --- PLAN TRENINGOWY ---

plan = [
    # TYDZIEŃ 1-2
    {"day": "Pon", "desc": "Marszobieg 1 min biegu / 2 min marszu × 8", "time": "24 min", "hr": "≤135 bpm"},
    {"day": "Wto", "desc": "Odpoczynek / spacer", "time": "–", "hr": "–"},
    {"day": "Śro", "desc": "Marszobieg 1 min biegu / 1,5 min marszu × 10", "time": "25 min", "hr": "≤135 bpm"},
    {"day": "Czw", "desc": "Odpoczynek lub joga", "time": "–", "hr": "–"},
    {"day": "Pt", "desc": "Marszobieg 2 min biegu / 2 min marszu × 6", "time": "24 min", "hr": "≤135 bpm"},
    {"day": "Sob", "desc": "Spacer / rower rekreacyjny", "time": "30–45 min", "hr": "–"},
    {"day": "Nd", "desc": "Marsz + trucht (5 min marszu / 3 min truchtu × 5)", "time": "40 min", "hr": "≤135 bpm"},

    # TYDZIEŃ 3-4
    {"day": "Pon", "desc": "Marszobieg 3 min biegu / 1,5 min marszu × 6", "time": "27 min", "hr": "≤135 bpm"},
    {"day": "Wto", "desc": "Spacer szybki / aktywna regeneracja", "time": "30 min", "hr": "–"},
    {"day": "Śro", "desc": "Marszobieg 4 min biegu / 1 min marszu × 5", "time": "25 min", "hr": "≤135 bpm"},
    {"day": "Czw", "desc": "Odpoczynek", "time": "–", "hr": "–"},
    {"day": "Pt", "desc": "Marszobieg 5 min biegu / 1 min marszu × 4", "time": "24 min", "hr": "≤135 bpm"},
    {"day": "Sob", "desc": "Lekki spacer / rozciąganie", "time": "30–40 min", "hr": "–"},
    {"day": "Nd", "desc": "Bieg + marsz: 10 min truchtu + 2 min marszu + 10 min biegu", "time": "22 min", "hr": "≤140 bpm"},

    # TYDZIEŃ 5-6
    {"day": "Pon", "desc": "Bieg ciągły 15 min + 5 min marszu + 10 min biegu", "time": "30 min", "hr": "≤140 bpm"},
    {"day": "Wto", "desc": "Spacer szybki / rower", "time": "30–40 min", "hr": "–"},
    {"day": "Śro", "desc": "Marszobieg 6 min biegu / 1 min marszu × 4", "time": "28 min", "hr": "≤135 bpm"},
    {"day": "Czw", "desc": "Odpoczynek", "time": "–", "hr": "–"},
    {"day": "Pt", "desc": "Bieg ciągły 20–25 min bardzo wolno", "time": "–", "hr": "≤140 bpm"},
    {"day": "Sob", "desc": "Rozciąganie, mobilizacja", "time": "–", "hr": "–"},
    {"day": "Nd", "desc": "Długi marsz lub 30 min marsz + 15 min trucht", "time": "45–50 min", "hr": "≤135 bpm"},

    # TYDZIEŃ 7-8
    {"day": "Pon", "desc": "Bieg ciągły 30 min wolno", "time": "–", "hr": "≤140 bpm"},
    {"day": "Wto", "desc": "Spacer / rower / regeneracja", "time": "40 min", "hr": "–"},
    {"day": "Śro", "desc": "Marszobieg 8 min biegu / 1 min marszu × 3", "time": "27 min", "hr": "≤135 bpm"},
    {"day": "Czw", "desc": "Wolne", "time": "–", "hr": "–"},
    {"day": "Pt", "desc": "Bieg ciągły 25 min + 5 przebieżek (60 m)", "time": "~30 min", "hr": "Przebieżki: bez przekraczania 150 bpm"},
    {"day": "Sob", "desc": "Spacer, joga", "time": "45 min", "hr": "–"},
    {"day": "Nd", "desc": "Długi spokojny bieg lub trucht z marszem", "time": "45–60 min", "hr": "≤135 bpm"},
]

# Start planu - 14.07.2025 poniedziałek
start_date = datetime(2025, 7, 14).date()

# --- WYBÓR DATY ---
st.sidebar.header("📅 Wybierz dzień treningowy")
selected_date = st.sidebar.date_input("Data", datetime.today().date())

day_index = (selected_date - start_date).days

if 0 <= day_index < len(plan):
    day_plan = plan[day_index]

    st.subheader(f"Trening na {selected_date.strftime('%A, %d.%m.%Y')}")
    st.markdown(f"**Dzień tygodnia:** {day_plan['day']}")
    st.markdown(f"**Trening:** {day_plan['desc']}")
    st.markdown(f"**Czas:** {day_plan['time']}")
    st.markdown(f"**Tętno:** {day_plan['hr']}")

    # --- FORMULARZ ---
    st.markdown("---")
    st.write("Uzupełnij dane o wykonaniu i samopoczuciu:")

    with st.form("form"):
        wykonane = st.checkbox("✅ Wykonano trening?")
        samopoczucie = st.slider("Jak oceniasz swoje samopoczucie? (1-10)", 1, 10, 5)
        sen = st.slider("Ile godzin spałeś(-aś)?", 0.0, 12.0, 7.0, 0.5)

        # Jeśli poniedziałek – dodatkowe pola pomiarowe
        pomiary = {}
        if selected_date.weekday() == 0:  # 0 = poniedziałek
            st.markdown("### 📏 Pomiary ciała")
            pomiary_fields = {
                "Klatka (cm)": "klatka",
                "Brzuch nad pępkiem (cm)": "brzuch_nad",
                "Brzuch pod pępkiem (cm)": "brzuch_pod",
                "Biceps prawy (cm)": "biceps_p",
                "Biceps lewy (cm)": "biceps_l",
                "Udo prawe (cm)": "udo_p",
                "Udo lewe (cm)": "udo_l",
                "Łydka prawa (cm)": "lydka_p",
                "Łydka lewa (cm)": "lydka_l",
            }

            for label, key in pomiary_fields.items():
                pomiary[key] = st.number_input(label, min_value=0.0, max_value=300.0, step=0.1)

        notatki = st.text_area("Notatki / komentarze", height=80)
        submitted = st.form_submit_button("Zapisz dane")

    if submitted:
        try:
            df = pd.read_csv("dziennik.csv")
        except FileNotFoundError:
            df = pd.DataFrame()

        # Dane podstawowe
        new_row = {
            "Data": selected_date.strftime("%Y-%m-%d"),
            "Wykonano": wykonane,
            "Samopoczucie": samopoczucie,
            "Sen": sen,
            "Notatki": notatki,
        }

        # Jeśli poniedziałek – dodaj pomiary
        if selected_date.weekday() == 0:
            new_row.update(pomiary)

        # Usuń istniejący wpis tego dnia, jeśli istnieje
        df = df[df["Data"] != selected_date.strftime("%Y-%m-%d")]
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_csv("dziennik.csv", index=False)
        st.success("✅ Dane zapisane!")

# --- PODGLĄD DANYCH ---
st.markdown("---")
st.subheader("📋 Podgląd zapisanych danych:")

try:
    df = pd.read_csv("dziennik.csv")
    df_display = df.sort_values("Data", ascending=False).reset_index(drop=True)

    # Formatowanie – zamieniamy puste komórki na "–"
    df_display.fillna("–", inplace=True)

    # Wyświetl pełną tabelę z możliwością przewijania
    st.dataframe(df_display, use_container_width=True)

    # Opcjonalnie: filtr tylko poniedziałków z pomiarami
    if "klatka" in df_display.columns:
        df_pomiary = df_display[df_display["klatka"] != "–"]
        if not df_pomiary.empty:
            st.markdown("### 📏 Historia pomiarów (tylko poniedziałki)")
            st.dataframe(df_pomiary[[
                "Data", "klatka", "brzuch_nad", "brzuch_pod",
                "biceps_p", "biceps_l", "udo_p", "udo_l", "lydka_p", "lydka_l"
            ]], use_container_width=True)

try:
    df = pd.read_csv("dziennik.csv")
    df_display = df.sort_values("Data", ascending=False).reset_index(drop=True)
    df_display.fillna("–", inplace=True)
    st.dataframe(df_display, use_container_width=True)

    if "klatka" in df_display.columns:
        df_pomiary = df_display[df_display["klatka"] != "–"].copy()
        if not df_pomiary.empty:
            st.markdown("### 📏 Historia pomiarów (tylko poniedziałki)")
            st.dataframe(df_pomiary[[
                "Data", "klatka", "brzuch_nad", "brzuch_pod",
                "biceps_p", "biceps_l", "udo_p", "udo_l", "lydka_p", "lydka_l"
            ]], use_container_width=True)

            # --- WYKRESY POSTĘPÓW ---
            import matplotlib.pyplot as plt

            st.markdown("### 📈 Wykresy postępów (pomiarów ciała)")

            # Konwersja danych
            df_pomiary["Data"] = pd.to_datetime(df_pomiary["Data"])
            pomiary_kolumny = ["klatka", "brzuch_nad", "brzuch_pod", "biceps_p", "biceps_l", "udo_p", "udo_l", "lydka_p", "lydka_l"]

            for kol in pomiary_kolumny:
                df_pomiary[kol] = pd.to_numeric(df_pomiary[kol], errors="coerce")

            wybor_pomiaru = st.selectbox("📊 Wybierz pomiar do wyświetlenia na wykresie:", pomiary_kolumny)

            fig, ax = plt.subplots()
            ax.plot(df_pomiary["Data"], df_pomiary[wybor_pomiaru], marker="o", linestyle="-")
            ax.set_xlabel("Data")
            ax.set_ylabel("Wartość (cm)")
            ax.set_title(f"Zmiana pomiaru: {wybor_pomiaru}")
            ax.grid(True)
            st.pyplot(fig)

except FileNotFoundError:
    st.write("Brak zapisanych danych jeszcze.")


except FileNotFoundError:
    st.write("Brak zapisanych danych jeszcze.")

else:
    st.warning("🕒 Dziś nie ma zaplanowanego treningu w ramach planu (poza zakresem 8 tygodni).")
