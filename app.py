if st.button("Get Answer"):
    if query.strip():
        answer = search_with_openai(query)
        if "No relevant information" in answer:
            answer = search_answer_in_file(query)
        st.success(f"Answer: {answer}")
    else:
        st.error("Please enter a query.")
