from transformers import pipeline
import logging
import timeit
import json
import os
import torch
import streamlit as st
# This should stay above the import of transformers to have model downloaded in the same directory as the project
os.environ['TRANSFORMERS_CACHE'] = os.curdir + '/cache'

logging.basicConfig(
    level=logging.INFO,
    filename='llm.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@st.cache_resource
def init():
    # summarizer = pipeline("summarization",
    #                       model="sshleifer/distilbart-cnn-12-6",
    #                       use_fast=True, device=0)
    detector = pipeline(
        "text-classification",
        model="1aurent/distilbert-base-multilingual-cased-finetuned-email-spam",
        use_fast=True)
    tagger = pipeline("text2text-generation",
                      model="fabiochiu/t5-base-tag-generation",
                      use_fast=True)
    return [detector, tagger]


def summarize(prompt, summarizer):
    start = timeit.default_timer()
    summarized = summarizer(prompt, min_length=75)
    stop = timeit.default_timer()
    logging.info(f"Summary: {prompt}")
    logging.info(f"Time taken to summarize: {stop - start}")

    return summarized


def detect_spam(prompt, detector):
    spam = detector(prompt, truncation=True)
    return spam[0]['label']


def get_tags(prompt, tagger):
    tags = tagger(prompt)
    return tags


# if __name__ == "__main__":
#   llm = Summarizer()

#   summary = llm.summarize("""
# image.png


# Job Chahiye!?!?

# GDSC is here with another fantastic event
# DSA Busted
# This event will teach you about DATA STRUCTURES AND ALGORITHMS, as well as how to tackle coding rounds.
# Every Saturday, we will have live doubt sessions.
# Every Sunday, we will have a quiz.
# CERTIFICATE and  Exciting GOODIES from GOOGLE.

# So, don't pass up this excellent opportunity to begin or fast track your placement preparations.

# """)
#   print(summary)
