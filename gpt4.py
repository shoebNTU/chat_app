import requests
import streamlit as st

st.subheader("Siemens ChatGPT-like clone (GPT-4 model from SMO-IT). Not ACP compliant.")

password = st.text_input(label='Please enter password to access this application', type='password')

if password == st.secrets['password']:

    api_key = st.secrets['api_key']

    API_URL = "https://mobilityapi-dev.siemens.com/mobilityai/v2/deployments/MobilityAIGPT4/chat/completions?api-version=2023-05-15"

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": f"{api_key}",  # os.environ['API_KEY'] # REPLACE THIS WITH YOUR API KEY
    }

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            response = requests.post(
                API_URL,
                headers=headers,
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                },
            )
            ans = response.json()
            print(ans)
            full_response = ans["choices"][0]["message"]["content"]
            message_placeholder.markdown(full_response)
            # possibly summarize your reponse before saving it in content?
        st.session_state.messages.append({"role": "assistant", "content": full_response})
