import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import os

os.environ['OPENAI_API_KEY'] = "YOUR_API_KEY"

data = 'reviews.csv'
df = pd.read_csv(data, delimiter=",")

llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo", verbose=True)

reply_schema = ResponseSchema(name="Reply",
                             description="Check whether the match is Yes or No.\
                                 If the match is yes, write a suitable response for the review. (The reply should be polite and thankful for positive sentiments and should be apologetic for negative sentiments.)\
                                 If the match is no AND rating is above 3, write a suitable thankful response but sternly mention how the rating does not match the user's sentiment.\
                                 The output should be a single string response in 'Customer's Language' without any mention of match:Yes/No.")
tags_schema = ResponseSchema(name="Tags",
                                      description="Identify the key points mentioned in the review and create a list of those points.\
                                          For example: ['Affordable', 'cheap']. The output should be a single list")

response_schemas = [reply_schema, 
                    tags_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt1 = ChatPromptTemplate.from_template('''
    Translate the following review to English:
    \n\n {review}
    '''
)

chain1 = LLMChain(llm=llm, prompt=prompt1, output_key='English_review')

prompt2 = ChatPromptTemplate.from_template('''
    Identify the sentiment of the review and remember it as either POSTIVE, NEUTRAL OR NEGATIVE.
    \n\n Review: {English_review}
    \n\n Check whether the original rating: '{rating}' matches the sentiment you identified (Ratings are from 1-5 and positive sentiment correlates with \
        ratings above 3, neutral for 3 and below 3 is negative sentiment) and remember it as Match: Yes/No
    \n\n Identify the language used here: {review} and remember is as 'Customer's Language'.
    
    Return the following as output:
    {format_instructions}
    '''
)

chain2 = LLMChain(llm=llm, prompt=prompt2, output_key='Result_dictionary')

overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["review", "rating", "format_instructions"],
    output_variables=["Result_dictionary"],
    verbose=False)

output_df = pd.DataFrame(columns=['Name', 'Reply', 'Tags'])
for i in range(len(df)):
    review = df.Reviews[i]
    rating = df.Rating[i]
    name = df.Names[i]
    chain_output = overall_chain({'review':review, 'rating':rating, 'format_instructions':format_instructions})
    output_dict = output_parser.parse(chain_output.get('Result_dictionary'))
    output_dict['Names'] = name
    new_row = pd.DataFrame([output_dict])
    output_df = pd.concat([output_df, new_row], ignore_index=True)