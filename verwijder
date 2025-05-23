import pandas as pd

# Laad de bestaande verlofdata
bestand = "verlofregistratie_2025.csv"
verlof_data = pd.read_csv(bestand)

# Geef hier de naam en datum van de boeking die je wil verwijderen
naam = "Melissa"
datum = "3/07/2025"  # Opgelet: formaat moet exact zo zijn als in de CSV

# Filter de rij eruit (verwijder als naam én datum overeenkomen)
verlof_data = verlof_data[~((verlof_data["Naam"] == naam) & (verlof_data["Datum"] == datum))]

# Sla de aangepaste gegevens terug op
verlof_data.to_csv(bestand, index=False)

print(f"✅ Boekingen van {naam} op {datum} verwijderd.")
