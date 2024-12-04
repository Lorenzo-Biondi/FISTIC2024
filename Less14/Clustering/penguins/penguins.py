import streamlit as st
import joblib
import pandas as pd

def load_model():
    """Load the trained penguin species prediction model."""
    try:
        return joblib.load("Penguins.pkl")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def setup_page():

    
    st.title("🐧 Palmer Penguins Species Predictor")
    st.markdown("""
    This app predicts the species of Palmer Archipelago penguins based on their physical characteristics.
    The model is trained on the famous Palmer Penguins dataset, which includes measurements from three penguin species:
    - Adelie
    - Gentoo
    - Chinstrap
    """)

def get_user_input():
    """Collect and validate user input for penguin measurements."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Physical Measurements")
        bill_length = st.number_input(
            "Bill Length (mm)",
            min_value=30.0,
            max_value=60.0,
            value=45.0,
            help="The length of the penguin's bill in millimeters"
        )
        
        bill_depth = st.number_input(
            "Bill Depth (mm)",
            min_value=13.0,
            max_value=22.0,
            value=17.0,
            help="The depth of the penguin's bill in millimeters"
        )
        
        flipper_length = st.slider(
            "Flipper Length (mm)",
            min_value=170,
            max_value=240,
            value=200,
            help="The length of the penguin's flipper in millimeters"
        )
    
    with col2:
        st.subheader("Additional Information")
        body_mass = st.slider(
            "Body Mass (g)",
            min_value=2700,
            max_value=6300,
            value=4000,
            step=100,
            help="The penguin's body mass in grams"
        )
        
        sex = st.radio(
            "Sex",
            options=["Male", "Female"],
            horizontal=True
        )
        
        island = st.selectbox(
            "Island",
            options=["Torgersen", "Biscoe", "Dream"],
            help="The island where the penguin was observed"
        )
    
    return {
        "bill_length_mm": bill_length,
        "bill_depth_mm": bill_depth,
        "flipper_length_mm": flipper_length,
        "body_mass_g": body_mass,
        "sex": sex.lower(),
        "island": island
    }

def make_prediction(model, input_data):
    """Make a prediction using the loaded model."""
    try:
        df = pd.DataFrame([input_data])
        prediction = model.predict(df)
        return prediction[0]
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None

def display_results(prediction):
    """Display the prediction results with styling."""
    st.markdown("---")
    st.subheader("Prediction Results")
    
    if prediction:
        st.success(f"🎯 This penguin is predicted to be a **{prediction}** penguin!")
        
        # Add some educational content based on the prediction
        species_info = {
            "Adelie": {
                "description": "Adelie penguins are the smallest of the Palmer penguins, known for their distinctive white ring around their eyes.",
                "fun_fact": "They can swim up to 45 miles per hour!"
            },
            "Gentoo": {
                "description": "Gentoo penguins are the largest of the Palmer penguins, recognized by their bright orange-red bill and white stripe across the top of their head.",
                "fun_fact": "They're the fastest underwater swimming penguins, reaching speeds of 22 mph!"
            },
            "Chinstrap": {
                "description": "Chinstrap penguins are named for the narrow black band under their heads, making them appear to wear a tiny black helmet.",
                "fun_fact": "They make nests out of small stones and can be quite aggressive in defending them!"
            }
        }
        
        if prediction in species_info:
            st.info(f"**About {prediction} Penguins:**\n\n" + 
                   species_info[prediction]["description"])
            st.markdown(f"**Fun Fact:** {species_info[prediction]['fun_fact']}")

def main():
    """Main function to run the Streamlit app."""
    setup_page()
    
    model = load_model()
    if not model:
        return
    
    with st.expander("How to Use This App", expanded=False):
        st.markdown("""
        1. Enter the penguin's physical measurements
        2. Select the sex and island location
        3. The app will predict the penguin species
        4. Learn interesting facts about the predicted species!
        
        All measurements should be as accurate as possible for the best prediction results.
        """)
    
    input_data = get_user_input()
    
    if st.button("🔍 Predict Species", type="primary"):
        prediction = make_prediction(model, input_data)
        display_results(prediction)
    
    st.sidebar.markdown("""
    ### About
    This app uses machine learning to predict Palmer Archipelago penguin species based on their physical characteristics.
    
    Data source: [Palmer Penguins Dataset](https://allisonhorst.github.io/palmerpenguins/)
    """)

if __name__ == "__main__":
    main()