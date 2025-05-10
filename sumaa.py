import streamlit as st
from transformers import pipeline

def summar_txt(preloaded_from_pdf):
    # Initialize the summarization pipeline
    @st.cache_resource
    def load_summarizer():
        return pipeline("summarization")

    summarizer = load_summarizer()

    # Streamlit app setup
   
    st.title("Text Summarizer with Transformers 🤖")
    st.write("Generate concise summaries of long texts using the Hugging Face Transformers library.")
    st.markdown("(PDF extracted text is sent to summarizer textarea for speed testing)")
    # Sidebar
    st.sidebar.header("Summarization Configuration")
    max_length = st.sidebar.slider("Maximum summary length:", min_value=20, max_value=200, value=50, step=10)
    min_length = st.sidebar.slider("Minimum summary length:", min_value=10, max_value=100, value=25, step=5)
    do_sample = st.sidebar.checkbox("Enable sampling (randomness in output)?", value=False)
    show_model_info = st.sidebar.checkbox("Show model details", value=False)

    # Display model information if toggled
    if show_model_info:
        st.sidebar.markdown("### Model Details")
        st.sidebar.write(
            """
            **Pipeline**: Summarization  
            **Model**: Default Hugging Face summarization model  
            **Library**: [Transformers](https://huggingface.co/transformers/)
            """
        )

    # Main input area
    st.subheader("Input Text")

    input_text = st.text_area(
        "Enter the text you want to summarize (minimum length: 50 characters):",value = preloaded_from_pdf, height=300
    )

    # Action buttons
    if st.button("Summarize"):
        if input_text.strip() and len(input_text) >= 50:
            with st.spinner("Generating summary..."):
                try:
                    # Generate summary
                    summary = summarizer(
                        input_text,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=do_sample,
                    )
                    st.subheader("Generated Summary")
                    st.success(summary[0]["summary_text"])
                except Exception as e:
                    st.error(f"An error occurred while summarizing: {e}")
        else:
            st.warning("Please enter text with at least 50 characters.")

    # Footer
    st.markdown("---")
    st.markdown(
        "Developed with ❤️ "
    )
