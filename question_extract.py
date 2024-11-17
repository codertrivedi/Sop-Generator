#!/usr/bin/env python
# coding: utf-8

# In[10]:


from docx import Document


# In[22]:


def extract_from_doc(docpath):
    document = Document(docpath)
    return [para.text.strip() for para in document.paragraphs if para.text.strip()]


# In[80]:


def extract_questions(questionnaire_path):
    questionnaire_text = extract_from_doc(questionnaire_path)
    questions = []
    question = None

    question = None
    for line in questionnaire_text:
        if line.startswith("Your answer:"):
            answer = line.replace("Your answer", '').strip()
            if question and answer:
                questions.append(question)
            question = None
        elif line and not line.startswith("Your answer"):
            question = line.strip()

    return questions



# In[81]:


questions = extract_questions("S:/datasets/Sop_dataset/Questionnaire/questionnaire_1.docx")


# In[82]:


questions


# In[ ]:





# In[ ]:




