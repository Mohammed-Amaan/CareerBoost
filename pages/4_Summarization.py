import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import docx2txt as docx2txt
import fitz
import streamlit as st

nltk.download("punkt")
nltk.download("stopwords")


def extractive_summarization(text, num_sentences):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize the sentences into words
    words = word_tokenize(text)

    # Filter out stop words
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.casefold() not in stop_words]

    # Calculate the frequency of each word
    freq_dist = FreqDist(words)

    # Calculate the score for each sentence based on the word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if i in sentence_scores:
                    sentence_scores[i] += freq_dist[word]
                else:
                    sentence_scores[i] = freq_dist[word]

    # Sort the sentences by their scores in descending order
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Select the top 'num_sentences' sentences for the summary
    summary_sentences = ranked_sentences[:num_sentences]

    # Sort the summary sentences in the original order
    summary = " ".join([sentences[i] for i in sorted(summary_sentences)])

    return summary


# Example usage
def summarize_pdf(num_sentences):
    st.write("")
    st.markdown("##### Upload Job Description", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"])
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text")
        maintext = text.split(".")
        # st.write(maintext)

        summary = extractive_summarization(text, num_sentences)
        st.markdown(f"<h5> {summary}</h5>", unsafe_allow_html=True)
        st.markdown(
            "### Include these skills in your resume to get noticed by recruiters!",
            unsafe_allow_html=True,
        )


st.set_page_config(page_title="CareerBoost", page_icon="🚀", layout="wide")

st.markdown("<h1 style='color: #d66d22;'>Job Description Summarizer</h1>", unsafe_allow_html=True)
st.markdown(
    "### Tired of looking through lengthy job descriptions?", unsafe_allow_html=True
)
st.markdown(
    "#### Use our summarizer to extract important information.", unsafe_allow_html=True
)

num_sentences = 4
summary = summarize_pdf(num_sentences)
