#!/usr/bin/env python
# coding: utf-8

# In[40]:


from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from langchain.llms import HuggingFaceHub
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import PromptTemplate

#hugging face
from huggingface_hub import login


# In[36]:


#quantization 
quantization_config = BitsAndBytesConfig(load_in_8bit = True, llm_int8_enable_fp32_cpu_offload=True)


# In[37]:


#Initialize tokenizer and model

t5_tokenizer = T5Tokenizer.from_pretrained("flan_t5_finetuned")
t5_model = T5ForConditionalGeneration.from_pretrained("flan_t5_finetuned", quantization_config=quantization_config, device_map="auto")


# In[42]:


#Define pipelines

flan_pipeline = pipeline("text2text-generation", model=t5_model, tokenizer=t5_tokenizer)


# In[43]:


#prompts

generation_prompt_template = PromptTemplate(
    template = "Generate an SOP based on the following answers: {answers}", 
    input_variables = ["answers"]
)

refinement_prompt_template = PromptTemplate(
    template = "Polish this SOP to sound more professional and natural: {sop}",
    input_variables = ["sop"]
)


# In[44]:


#Runnable sequence

sop_generator_refiner = generation_prompt_template | flan_pipeline | refinement_prompt_template | flan_pipeline


# In[1]:


# function for generating and refining sop

def generate_refine_sop(answers):
    sop_data = {"answers" : answers}
    refined_sop = sop_generator_refiner.invoke(sop_data)
    print("Refined SOP: ", refined_sop)
    return refined_sop


# In[ ]:




