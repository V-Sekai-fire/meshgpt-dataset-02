# Copyright (c) 2023-present. This file is part of V-Sekai https://v-sekai.org/.
# K. S. Ernest (Fire) Lee & Contributors (see .all-contributorsrc).
# llama-cpp-grammar.py
# SPDX-License-Identifier: MIT

from llama_cpp import Llama, LlamaGrammar
import httpx
import os
import tempfile
from functools import lru_cache
from tqdm import tqdm
import json

@lru_cache(maxsize=1)
def get_model_file(model_url):
    with httpx.stream('GET', model_url, follow_redirects=True) as response:
        response.raise_for_status()

        total_length = int(response.headers.get('content-length'))
        download_so_far = 0

        import hashlib
        filename = hashlib.md5(model_url.encode('utf-8')).hexdigest() + '.gguf'
        model_path = os.path.join(tempfile.gettempdir(), filename)

        if not os.path.exists(model_path):
            print("Downloading the model...")

            with open(model_path, 'wb') as model_file, tqdm(total=total_length, unit='iB', unit_scale=True, desc=filename) as bar:
                for chunk in response.iter_bytes(1024):
                    download_so_far += len(chunk)
                    bar.update(len(chunk))
                    model_file.write(chunk)

    return model_path

model_url = "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q4_K_M.gguf?download=true"
model_path = get_model_file(model_url)
with open("json_arr.gbnf", 'r') as file:
    grammar_file_contents = file.read()
grammar = LlamaGrammar.from_string(grammar_file_contents)
import sys

max_tokens = -1
prompt = "JSON list of name strings of attractions in Vancouver, Canada:"
llm = Llama(model_path=model_path)
response = llm(prompt, grammar=grammar, max_tokens=max_tokens)
json_output = json.loads(response['choices'][0]['text'])
print(json.dumps(json_output, indent=4))
while True:
    prompt = input("Enter your prompt (or type 'exit' to quit): ")
    if prompt.lower() == 'exit': 
        print("Exiting...")
        break
    response = llm(prompt, grammar=grammar, max_tokens=max_tokens)
    json_output = json.loads(response['choices'][0]['text'])
    print(json.dumps(json_output, indent=4))
