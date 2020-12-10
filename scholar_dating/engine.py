from transformers import pipeline
import torch
import re
import numpy as np
import os

class ConversationMemory:
    def __init__(self, max_size):
        self.memory = []
        self.max_size = max_size

    def add(self, question, answer):
        self.memory.append((question, answer))
        if len(self.memory) > self.max_size:
            del self.memory[0]

    def prompt(self):
        pass

class ConversationEngine:
    def __init__(self, qa_threshold, top_k, max_length, temp, penalty):
        self.qa_threshold = qa_threshold
        self.top_k = top_k
        self.max_length = max_length
        self.temp = temp
        self.penalty = penalty
        self.verbose = False

    def load_pipeline(self, qa_name, qa_folder, gpt2_name, gpt2_folder):
        if os.path.exists(qa_folder):
            self.qa_pipeline = pipeline('question-answering', model=qa_folder, tokenizer=qa_folder)
        else:
            self.qa_pipeline = pipeline('question-answering', model=qa_name, tokenizer=qa_name)
            self.qa_pipeline.save_pretrained(qa_folder)
        if os.path.exists(gpt2_folder):
            self.gpt2_pipeline = pipeline('text-generation', model=gpt2_folder, tokenizer=gpt2_folder)
        else:
            self.gpt2_pipeline = pipeline('text-generation', model=gpt2_name, tokenizer=gpt2_name)
            self.gpt2_pipeline.save_pretrained(gpt2_folder)

    def test_qa(self, question, context):
        response = self.qa_pipeline(question=question, context=context)
        answer = response['answer']
        if (len(answer) > 0 and len(answer) < len(inputData) - 1) and response['score'] >= self.qa_threshold:
            return answer.strip()

    def test_gpt2(self, prompt):
        response = self.gpt2_pipeline(prompt,
                pad_token_id = self.gpt2_pipeline.tokenizer.eos_token_id,
                do_sample=True,
                max_length=len(self.gpt2_pipeline.tokenizer.encode(prompt)) + self.max_length,
                top_k=self.top_k,
                temperature=self.temp,
                repetition_penalty=self.penalty
                )[0]
        answer = response['generated_text'][len(prompt):]
        answer = re.sub('[〈♥✪✌~ǫ]*', '', answer)
        answer = re.sub('\n', ' ', answer)
        index = len(answer)
        if answer.find('.') > self.max_length / 10:
            index = min(index, answer.find('.'))
        if answer.find('?') > self.max_length / 10:
            index = min(index, answer.find('?'))
        if answer.find('!') > self.max_length / 10:
            index = min(index, answer.find('!'))
        if index == len(answer):
            return ""
        answer = answer[0:index+1]
        return answer.strip()

    def get_response(self, player, user, question):
        prompt = user.get_prompt(player, question)
        response = self.gpt2_pipeline(
                prompt,
                pad_token_id = self.gpt2_pipeline.tokenizer.eos_token_id,
                do_sample=True,
                max_length=len(self.gpt2_pipeline.tokenizer.encode(prompt)) + 2 * self.max_length,
                top_k=self.top_k,
                temperature=self.temp,
                repetition_penalty=self.penalty
            )[0]
        if self.verbose:
            print(response)
        answer = response['generated_text'][len(prompt):]
        answer = re.sub('[〈♥✪✌~]*', '', answer)
        answer = re.sub('\n', ' ', answer)
        index = len(answer)
        if answer.find('.') > self.max_length / 10:
            index = min(index, answer.find('.'))
        if answer.find('?') > self.max_length / 10:
            index = min(index, answer.find('?'))
        if answer.find('!') > self.max_length / 10:
            index = min(index, answer.find('!'))
        gpt2_answer = answer[0:index+1]

        response = self.qa_pipeline(question=question, context=user.context[0] + " " + gpt2_answer)
        if self.verbose:
            print(response)
        answer = response['answer']
        if (len(answer) > 0 and len(answer) < len(prompt + " " + gpt2_answer) - 1) and response['score'] >= self.qa_threshold:
            return answer.strip()

        for inputData in user.context:
            response = self.qa_pipeline(question=question, context=inputData)
            if self.verbose:
                print(response)
            answer = response['answer']
            if (len(answer) > 0 and len(answer) < len(inputData) - 1) and response['score'] >= self.qa_threshold:
                return answer.strip()

        return gpt2_answer.strip()
