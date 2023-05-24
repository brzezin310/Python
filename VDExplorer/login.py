# login.py

import streamlit as st

def login():
    st.title("Logowanie")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Hasło", type="password", key="login_password")
    if st.button("Zaloguj"):
        # Tutaj dodaj logikę uwierzytelniania użytkownika
        # Sprawdź poprawność danych logowania
        if email == "admin@example.com" and password == "password":
            st.success("Zalogowano pomyślnie!")
            return True
        else:
            st.error("Błąd logowania. Sprawdź poprawność danych.")
    return False

is_logged_in = login()

if is_logged_in:
    # Uruchom naszą aplikację główną
    import app8  # Nazwa twojego pliku z aplikacją główną
    app8.run_app()  # Wywołaj funkcję uruchamiającą aplikację główną
