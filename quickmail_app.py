import streamlit as st
import string
import re
from collections import Counter

def extract_dates(text):
   date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b'
   dates = re.findall(date_pattern, text)
   return list(set(dates))

def extract_contacts(text):
   email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
   emails = re.findall(email_pattern, text)
   return list(set(emails))

def summarize_text(text, ratio=0.2):
   sentences = text.split('.')
   clean_sentences = [s.strip().translate(str.maketrans('', '', string.punctuation)) for s in sentences]
   word_counts = Counter(' '.join(clean_sentences).split())
   
   scored_sentences = []
   for sentence in clean_sentences:
       score = sum(word_counts.get(word, 0) for word in sentence.split())
       scored_sentences.append((sentence, score))
   
   scored_sentences.sort(key=lambda x: x[1], reverse=True)
   num_sentences = int(len(scored_sentences) * ratio)
   summary_sentences = [sent[0] for sent in scored_sentences[:num_sentences]]
   
   summary = '. '.join(summary_sentences) + '.'
   return summary

def main():
   if "page" not in st.session_state:
       st.session_state.page = "Façade Page"

   if st.session_state.page == "Façade Page":
       st.title("Welcome to QuickMail Summarizer")
       st.write("This app can help you quickly summarize and extract key information from emails.")
       if st.button("Get Started"):
           st.session_state.page = "Main Page"

   elif st.session_state.page == "Main Page":
       st.title("QuickMail Summarizer")

       input_option = st.radio("Input Option", ("Text Input", "File Upload"))

       if input_option == "Text Input":
           email_text = st.text_area("Enter email text:", height=300)
           if st.button("Summarize"):
               summary = summarize_text(email_text)
               st.subheader("Summary")
               st.write(summary)

               dates = extract_dates(email_text)
               if dates:
                   st.subheader("Dates")
                   st.write(", ".join(dates))

               contacts = extract_contacts(email_text)
               if contacts:
                   st.subheader("Contacts")
                   st.write(", ".join(contacts))

       elif input_option == "File Upload":
           uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
           if uploaded_file is not None:
               if uploaded_file.type == "text/plain":
                   file_text = uploaded_file.read().decode("utf-8")
               else:
                   st.warning("Please upload a text file (.txt) for summarization.")
                   return

               if st.button("Summarize"):
                   summary = summarize_text(file_text)
                   st.subheader("Summary")
                   st.write(summary)

                   dates = extract_dates(file_text)
                   if dates:
                       st.subheader("Dates")
                       st.write(", ".join(dates))

                   contacts = extract_contacts(file_text)
                   if contacts:
                       st.subheader("Contacts")
                       st.write(", ".join(contacts))

if __name__ == "__main__":
   main()
