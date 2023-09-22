import logging
import timeit
import json
import os
import torch
os.environ['TRANSFORMERS_CACHE'] = os.curdir + '/cache'
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


class Summarizer():
    def __init__(self):
        model = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7b-Chat-GPTQ",
                                                     torch_dtype=torch.float16,
                                                     device_map="auto",
                                                     revision="main")

        tokenizer = AutoTokenizer.from_pretrained(
            "TheBloke/Llama-2-7b-Chat-GPTQ", use_fast=True)

        self._summarizer = pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=1024
        )

    def summarize(self, prompt):
        start = timeit.default_timer()
        txt = f'''[INST] <<SYS>>
        You are a helpful, respectful and honest summarization software, you will summarize given email body and only print a json object containing summary of the email with tags to classify the email, do not output anything else other than json, the json must contain two fields only: summary and tags, remember generate a json output
        <</SYS>>
        {prompt}[/INST]'''
        summary = self._summarizer(txt)
        logging.info(f"Summarization took {stop - start} seconds")
        txt = summary[0]["generated_text"]
        summary = json.loads(txt[txt.index("{"):])
        stop = timeit.default_timer()
        return summary


if __name__ == "__main__":
    llm = Summarizer()
    summary = llm.summarize(
        """
    Dear Atharv,

        I hope this email finds you and your loved ones in good health. I want to start by expressing my deepest empathy and understanding for the challenging journey you have been on with your health.

        I recently received the results of your medical tests, and I feel it's my responsibility to share this information with you as soon as possible. The news I have to deliver is undoubtedly difficult, and it pains me to be the bearer of such news.

        After a thorough evaluation, it is with great sadness that I must inform you that your condition has progressed to an advanced stage, and the available treatment options are no longer effective. I understand that this news may be overwhelming, and I am here to support you and your family in any way that I can.

        Please know that my entire team is committed to providing you with the utmost care, comfort, and dignity during this challenging time. We will work together to ensure your comfort and address any questions or concerns you may have. It is important for us to honor your wishes and help you make the best decisions for your well-being.

        I encourage you to reach out to me at any time to discuss your treatment preferences and to have open and honest conversations about your feelings and concerns. You are not alone in this journey, and we will do everything we can to make it as peaceful and comfortable as possible.

        I am here to support you every step of the way, and I want you to know that you are in our thoughts and prayers.

        Sincerely,

        Dr. Ayush Deshpande
"""
    )

    print(summary)
