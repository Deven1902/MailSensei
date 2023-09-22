from transformers import pipeline
import logging
import timeit
import json
import os
import torch
os.environ['TRANSFORMERS_CACHE'] = os.curdir + '/cache'


# Open and read the article
to_tokenize = """
Subject: Exclusive Limited-Time Offer - Act Now!

Dear Atharv,

Congratulations! You've been selected as the lucky winner of our exclusive offer. This is your chance to claim amazing prizes and discounts like never before. But act fast - this offer is available for a limited time only!

🎉 Win an all-expenses-paid luxury vacation to a tropical paradise!
🎁 Get 90% off on the latest gadgets and electronics!
💰 Earn $10,000 a week working from home - no experience needed!
🌟 Boost your love life with our miracle solution - guaranteed results!

To claim your prizes and discounts, simply click on the link below and provide your personal information. Hurry, this offer won't last!

https://yarro.onrender.com

Don't miss out on this once-in-a-lifetime opportunity. Act now to transform your life!

Sincerely,

Not Ayush Deshpande
notaspamipromise@email.com
"""

# Initialize the HuggingFace summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
detector = pipeline("text-classification",
                    model="1aurent/distilbert-base-multilingual-cased-finetuned-email-spam")
tagger = pipeline("text2text-generation",
                  model="fabiochiu/t5-base-tag-generation")


summarized = summarizer(to_tokenize, min_length=75, max_length=300)
detect = detector(to_tokenize)
tags = tagger(to_tokenize)

print(detect)

# Print summarized text
print(
    f"{summarized = }, \nspam/ham: {detect[0]['label']}, \ntags: {tags[0]['generated_text']}")
