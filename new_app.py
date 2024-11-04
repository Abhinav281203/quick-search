import streamlit as st
import fetch
import summary_
import suggested_keywords
import nltk

# nltk.download('stopwords')
# nltk.download('punkt')


def main():
    st.title("Quick Search")
    st.sidebar.header("Search Parameters")

    with st.sidebar:
        input_query = st.text_area("**Search here:**", height=100)
        max_token_limit = st.number_input(
            "**Adjust length (Maximum words)**",
            min_value=50,
            max_value=500,
            value=200,
            step=10,
        )
        language = st.selectbox(
            "**Select Language**", ["English", "Kannada", "Hindi", "Telugu"]
        )
        if input_query:
            search_button = st.button("**Search**")
            if search_button:
                st.session_state.input_query = input_query
                st.session_state.show = True
                article_links = fetch.fetch_urls(input_query, start=0, stop=2)
                # print("Searched", len(article_links), "links")
                # print(article_links)

                article_content = ""
                for link in article_links:
                    try:
                        article_content += fetch.extract_content(link)["content"]
                    except Exception as e:
                        print("Error@35-app:", e)
                summary = summary_.generate_summary(
                    article_content, max_token_limit, language
                )
                if len(st.session_state.messages) == 0:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": summary}
                    )

    if st.session_state.show:
        tab1, tab2 = st.tabs(["Ask anything", "More like this"])
        with tab1:

            for message in st.session_state.messages:
                with st.chat_message(
                    message["role"],
                    avatar="🧑‍💻" if message["role"] == "user" else "🤖",
                ):
                    st.markdown(message["content"])

            # Chat input
            if prompt := st.chat_input("What would you like to ask?"):
                # User message
                # print("prompted"* 200)
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Lyra's response
                with st.spinner("Assistant is thinking..."):
                    lyra_response = summary_.generate_resp(
                        st.session_state.input_query, st.session_state.messages, prompt
                    )
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(lyra_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": lyra_response}
                )
                st.rerun()

        with tab2:
            if "suggested" not in st.session_state:
                st.session_state.suggested = suggested_keywords.get_suggested(
                    input_query, summary
                )
                # print("Got keywords")
                # print(st.session_state.suggested, "&"*100)
                st.rerun()

            if "suggested" in st.session_state:
                for link in st.session_state.suggested:
                    obj = fetch.extract_content(link)
                    # print(obj)
                    if not obj["status"]:
                        continue
                    title = obj["title"]

                    st.subheader(title)
                    st.write(link)


if __name__ == "__main__":
    # Initialize session state for authentication status
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show" not in st.session_state:
        st.session_state.show = False

    main()
