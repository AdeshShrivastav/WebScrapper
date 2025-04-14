import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Device name{device}"*10)

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {cont}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Give the result in the form of table without code just table"

)

template2 = ("arrange the table data: {result} into a single tanble and return the table as it is without code or any other text"
             "only provide table as output do not explain anything"
             "dont repeate the collomn name twice")

model = OllamaLLM(model = "llama3.2", device = device, temprature = 0.5)

def parse(chunks,description):
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    result = []

    for i,chunk in enumerate(chunks,start=1):
        responce = chain.invoke({"cont": chunk, "description":description})

        print(f"Parsed batch{i} of {len(chunks)}")

        result.append(responce)


    def final_result(result):
        prompt2 = ChatPromptTemplate.from_template(template2)
        chain = prompt2 | model

        res = chain.invoke({"result":result})
        return res


    finalres = final_result(result)
    return finalres

