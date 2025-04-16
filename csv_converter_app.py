import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Format Converter for Jimdo", layout="centered")
st.title("🧾 CSV Format Converter for Jimdo")

uploaded_file = st.file_uploader("Upload seller-report CSV (mit ; als Trennzeichen)", type="csv")
template_file = st.file_uploader("Upload Jimdo-Beispiel CSV", type="csv")

if uploaded_file and template_file:
    try:
        # German special character support (ä, ö, ü, ß)
        source = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
        target = pd.read_csv(template_file, encoding="latin1")

        converted = pd.DataFrame(columns=target.columns)

        # Mapping example fields
        converted["Artikel"] = source.get("listing title", "")
        converted["Bestell-Datum"] = source.get("order date", "") + " " + source.get("order time", "")
        converted["Preis Brutto"] = source.get("gmv", "")
        converted["Währung"] = source.get("order currency", "")
        converted["Rechn. Nachname"] = source.get("buyer address name", "")
        converted["Rechn. Straße"] = source.get("buyer address line1", "")
        converted["Rechn. Postleitzahl"] = source.get("buyer address postal code", "")
        converted["Rechn. Stadt"] = source.get("buyer address city", "")
        converted["Rechn. Land"] = source.get("buyer address country", "")

        st.success("✅ Umwandlung erfolgreich! Hier kannst du die Datei herunterladen:")
        st.download_button(
            label="📥 Download CSV-Datei",
            data=converted.to_csv(index=False, encoding="utf-8-sig"),  # UTF-8 mit BOM für Excel-Kompatibilität
            file_name="converted_for_jimdo.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Fehler beim Verarbeiten der Datei: {e}")
