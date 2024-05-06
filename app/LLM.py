import logging
import timeit
import json
import os
import torch
import streamlit as st
# This should stay above the import of transformers to have model downloaded in the same directory as the project
os.environ['TRANSFORMERS_CACHE'] = os.curdir + '/cache'
from transformers import pipeline


logging.basicConfig(
    level=logging.INFO,
    filename='llm.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@st.cache_resource
def init():
    summarizer = pipeline("summarization",
                          model="sshleifer/distilbart-cnn-12-6",
                          use_fast=True,
                          device=0 if torch.cuda.is_available() else -1
                          )
    detector = pipeline(
        "text-classification",
        model="1aurent/distilbert-base-multilingual-cased-finetuned-email-spam",
        use_fast=True)
    tagger = pipeline("text2text-generation",
                      model="fabiochiu/t5-base-tag-generation",
                      use_fast=True)
    return [summarizer, detector, tagger]


def summarize(prompt, summarizer):
    start = timeit.default_timer()
    summarized = summarizer(prompt[:2048], truncation=True)
    stop = timeit.default_timer()
    logging.info(f"Summary: {summarized}")
    logging.info(f"Time taken to summarize: {stop - start}")

    return summarized


def detect_spam(prompt, detector):
    spam = detector(prompt[:2048], truncation=True)
    return spam[0]['label']


def get_tags(prompt, tagger):
    tags = tagger(prompt[:2048], truncation=True)
    return tags
