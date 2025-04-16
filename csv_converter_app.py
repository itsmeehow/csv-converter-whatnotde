import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Format Converter for Jimdo", layout="centered")
st.title("🧾 CSV Format Converter for Jimdo")

uploaded_file = st.file_uploader("Upload seller-report CSV", type="csv")
template_file = st.file_uploader("Upload Jimdo template CSV", type="csv")

if uploaded_file and template_file:
    try:
        source = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
        target = pd.read_csv(template_file, encoding="latin1")

        converted = pd.DataFrame(columns=target.columns)

        # Map fields (add more if needed)
        converted["Artikel"] = source.get("listing title", "")
        converted["Bestell-Datum"] = source.get("order date", "") + " " + source.get("order time", "")
        converted["Preis Brutto"] = source.get("gmv", "")
        converted["Währung"] = source.get("order currency", "")
        converted["Rechn. Nachname"] = source.get("buyer address name", "")
        converted["Rechn. Straße"] = source.get("buyer address line1", "")
        converted["Rechn. Postleitzahl"] = source.get("buyer address postal code", "")
        converted["Rechn. Stadt"] = source.get("buyer address city", "")
        converted["Rechn. Land"] = source.get("buyer address country", "")

        st.success("✅ Converted successfully! Download below:")
        st.download_button(
            label="Download Converted CSV",
            data=converted.to_csv(index=False).encode("utf-8"),
            file_name="converted_for_jimdo.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
