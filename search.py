from t5.IS005 import search
import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:144px !important;
    color:#E666E6;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Song Finder</p>', unsafe_allow_html=True)
query = st.text_input("Type in the lyrics:")

if query:
    st.subheader("Results:")
    try:
        results = search(query)
        col1, col2 = st.columns(2)
        if results:
            i = 0
            for result in results:
                i += 1
                if i % 2 == 1:
                    with col1:
                        st.markdown(
                            f"**Number:** {result['doc_id']} | **Song Link:** [{result['link']}]"
                            f"({result['link']}) | **Similarity:** {100 * result['cosine_sim']:.2f}%")
                else:
                    with col2:
                        st.markdown(
                            f"**Number:** {result['doc_id']} | **Song Link:** [{result['link']}]"
                            f"({result['link']}) | **Similarity:** {100 * result['cosine_sim']:.2f}%")

        else:
            st.write("No results found.")
    except (KeyError):
        pass
