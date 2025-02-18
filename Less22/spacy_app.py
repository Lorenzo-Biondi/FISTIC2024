import streamlit as st
import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_lg')

input_text = st.text_area("Text string to analyze:", "Jennifer drove to Seattle.")

doc = nlp(input_text)


# Add a section header:
st.header('Entity Visualizer')
# Take the text from the input field and render the entity html.
# Note that style="ent" indicates entities.
ent_html = displacy.render(doc, style='ent', jupyter=False)
# Display the entity visualization in the browser:
st.markdown(ent_html, unsafe_allow_html=True)