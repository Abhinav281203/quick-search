import streamlit as st
import fetch
import summary_
import suggested_keywords


def main():
    st.title("Quick Search")
    st.sidebar.header("Search Parameters")
    input_query = st.sidebar.text_area("**Search here:**", height=100)
    max_token_limit = st.sidebar.number_input(
        "**Adjust length[Maximum words]**",
        min_value=50,
        max_value=500,
        value=200,
        step=10,
    )
    language = st.sidebar.selectbox(
        "**Select Language**", ["English", "Kannada", "Hindi", "Telugu"]
    )

    if st.sidebar.button("**Search**"):
        st.empty()

        # Fetch URLs related to the input query
        article_links = fetch.fetch_urls(input_query, start=1, stop=3)

        article_content = ""
        for link in article_links:
            try:
                article_content += fetch.extract_content(link)["content"]
            except Exception as e:
                print("Error:", e)

        # Generate summary based on the input query
        summary = summary_.generate_summary(article_content, max_token_limit, language)

        st.header("Summary")
        st.write(summary)

        st.header("Articles You Might Like")
        # Display suggested articles based on keywords
        suggested_content = suggested_keywords.get_suggested(input_query, summary)
        print(suggested_content)

        for link in suggested_content.values():
            title = fetch.extract_content(link)["title"]

            if title == "":
                continue
            st.subheader(title)
            st.write(link)


if __name__ == "__main__":
    main()
