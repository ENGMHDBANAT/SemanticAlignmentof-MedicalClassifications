import streamlit as st
import pandas as pd
import requests, certifi, os, time

from streamlit_jupyter import StreamlitPatcher
StreamlitPatcher().jupyter()   # Run Streamlit inside Jupyter

# --------------------- API Settings ---------------------
CLIENT_ID = "aa84524e-2648-4f35-8107-1d67e5325f29_b7ae6ba1-6572-4f00-b719-2b61007ee5e8"
CLIENT_SECRET = "n1xGam0CyawIt2IvoFy656wrZF6YMJV/lQS1qsT4W2E="
TOKEN_URL = "https://icdaccessmanagement.who.int/connect/token"
SEARCH_URL = "https://id.who.int/icd/entity/search"

OUTPUT_FILE = "search_results.csv"

# --------------------- API Functions ---------------------
def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "icdapi_access",
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(TOKEN_URL, data=data, headers=headers, verify=certifi.where())
    r.raise_for_status()
    json_data = r.json()
    if "access_token" not in json_data:
        raise Exception(f"Token not returned: {json_data}")
    return json_data["access_token"]

def search_icd11(term, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Accept-Language": "en",
        "API-Version": "v2"
    }
    params = {"q": term, "useFlexSearch": "true"}
    r = requests.get(SEARCH_URL, headers=headers, params=params, verify=certifi.where())
    r.raise_for_status()
    data = r.json()
    return data.get("destinationEntities", [])

def fetch_entity_details(uri, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Accept-Language": "en",
        "API-Version": "v2"
    }
    r = requests.get(uri, headers=headers, verify=certifi.where())
    r.raise_for_status()
    data = r.json()

    title = data.get("title", {}).get("@value") if isinstance(data.get("title"), dict) else None
    definition = data.get("definition", {}).get("@value") if isinstance(data.get("definition"), dict) else None
    synonyms = [s["label"]["@value"] for s in data.get("synonym", []) if isinstance(s.get("label"), dict)]

    # Children URIs
    children = []
    for k in ["child", "children"]:
        for v in data.get(k, []):
            if isinstance(v, dict):
                ch_uri = v.get("@id") or v.get("id") or v.get("uri")
                if ch_uri:
                    children.append(ch_uri)

    # Parent URI
    parent = data.get("parent")
    if isinstance(parent, dict):
        parent_uri = parent.get("@id")
    elif isinstance(parent, list) and len(parent) > 0 and isinstance(parent[0], dict):
        parent_uri = parent[0].get("@id")
    else:
        parent_uri = None

    return {
        "URI": uri,
        "Title": title,
        "Definition": definition,
        "Synonyms": "; ".join(synonyms),
        "Parent_URI": parent_uri,
        "Children": children
    }

# --------------------- Streamlit Interface ---------------------
def run_app():
    st.title("🔍 ICD-11 Foundation Multiline Search Tool")
    st.write("Enter a list of terms, one per line:")

    text_input = st.text_area("Terms:", height=200)

    if st.button("Start Fetching"):
        terms = [t.strip() for t in text_input.split("\n") if t.strip()]
        if not terms:
            st.error("Please enter some terms")
            return

        st.success(f"📌 Number of terms: {len(terms)}")
        token = get_access_token()

        progress = st.progress(0)
        table_placeholder = st.empty()

        # Load existing CSV if available
        if os.path.exists(OUTPUT_FILE):
            df = pd.read_csv(OUTPUT_FILE)
        else:
            df = pd.DataFrame(columns=["Query", "URI", "Title", "Definition", "Synonyms", "Parent_URI", "Children"])

        total = len(terms)
        for i, term in enumerate(terms, start=1):
            search_results = search_icd11(term, token)
            term_entities = []

            for res in search_results:
                uri = res.get("theCode") or res.get("id") or res.get("@id")
                if uri:
                    details = fetch_entity_details(uri, token)
                    details["Query"] = term
                    term_entities.append(details)

            if term_entities:
                df = pd.concat([df, pd.DataFrame(term_entities)], ignore_index=True)
                df.to_csv(OUTPUT_FILE, index=False)

            progress.progress(i / total)
            table_placeholder.dataframe(df)

            time.sleep(0.2)

        st.success("🎉 Fetching completed successfully!")

# --------------------- Run the App ---------------------
run_app()
