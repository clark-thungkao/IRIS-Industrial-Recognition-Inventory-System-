import streamlit as st
import requests

# Replace this with the Test URL you copied from n8n
WEBHOOK_URL = "https://germancapybara.app.n8n.cloud/webhook-test/4bdb11b9-6f5c-449e-a90c-d5bc77b23635"

st.title("⚙️ AI Parts Inspector")
st.write("Upload a photo of a mechanical component to identify it and check stock.")

# Sensor Input: Capture the image
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the image back to the user
    st.image(uploaded_file, caption="Component Preview", width=300)
    
    # Actuator: Trigger the workflow
    if st.button("Identify Part"):
        with st.spinner("Transmitting to n8n controller..."):
            
            # Package the binary data correctly for transport
            files = {"data": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                # Send the POST request to n8n
                response = requests.post(WEBHOOK_URL, files=files)
                
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    
                    # Parse the JSON returned by the n8n "Last Node" (OpenAI)
                    ai_result = response.json()
                    
                    # Display the results on the dashboard
                    st.subheader("Inspection Results")
                    st.json(ai_result)
                    
                else:
                    st.error(f"Communication Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")