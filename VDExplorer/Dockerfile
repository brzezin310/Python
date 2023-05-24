# Użyj obrazu bazowego Python
FROM python:3.9-slim

# Ustaw katalog roboczy wewnątrz kontenera
WORKDIR /app

# Skopiuj plik requirements.txt do katalogu /app
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj pozostałą zawartość aplikacji do katalogu /app wewnątrz kontenera
COPY . .

# Zdefiniuj zmienne środowiskowe, jeśli są wymagane przez Twoją aplikację
ENV VARIABLE_NAME value

# Uruchom aplikację wewnątrz kontenera
CMD ["python", "app.py"]
