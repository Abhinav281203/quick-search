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
    input_query = st.sidebar.text_area("**Search here:**", height=100)
    max_token_limit = st.sidebar.number_input(
        "**Adjust length (Maximum words)**",
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
        article_links = fetch.fetch_urls(input_query, start=0, stop=2)
        print("Searched", article_links)

        article_content = ""
        for link in article_links:
            try:
                article_content += fetch.extract_content(link)["content"]
            except Exception as e:
                print("Error@37-app:", e)

        # Generate summary based on the input query
        summary = summary_.generate_summary(article_content, max_token_limit, language)

        st.write(summary)

        st.header("Things You Might Like")
        # Display suggested articles based on keywords
        suggested_content = suggested_keywords.get_suggested(input_query, summary)
        # print(suggested_content)

        for link in suggested_content:
            obj = fetch.extract_content(link)
            if not obj["status"]:
                continue
            title = obj["title"]

            st.subheader(title)
            st.write(link)


if __name__ == "__main__":
    main()
