import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, StorageContext, load_index_from_storage, download_loader
from llama_index.llms import OpenAI
import openai
import pandas as pd
#import plotly.express as px
import altair as alt

# openai.api_key = st.secrets.openai_key
openai.api_key = "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"
st.header("Chat with BCBS")

# excel_data = [["Blue Care Network of Michigan", 3.5, 4.5, 3.5],
# 				["Blue Cross Blue Shield of Michigan", 4, 3.5, 3.5],
# 				["Health Alliance Plan of Michigan", 3.5, 3.5, 3.5],
# 				["Priority Health", 3, 4.5, 3.5],
# 				["McLaren Health Plan Community", 2, 3, 3]
# ]

excel_data = [["BCNM", 3.5, 4.5, 3.5],
				["BCBSM", 4, 3.5, 3.5],
				["HAPM", 3.5, 3.5, 3.5],
				["Priority Health", 3, 4.5, 3.5],
				["MHPC", 2, 3, 3]
]

df = pd.DataFrame(excel_data, columns=["Plan Name", "Consumer Satisfaction", "Prevention", "Treatment"])

source=pd.melt(df, id_vars=['Plan Name'])

chart=alt.Chart(source).mark_bar(opacity=1).encode(
    x=alt.X('variable:N', axis=None),
    y=alt.Y('value:Q'),
    color=alt.Color('variable'),
    column=alt.Column('Plan Name:O', title="Plan Name", spacing =2, header = alt.Header(labelOrient = "bottom")),
).properties( width = 100, height = 200, ).configure_view(stroke='transparent').configure_axis(
    labelFontSize=20,
    titleFontSize=20
)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
	st.session_state.messages = [
		{"role": "assistant", "content": "What can I help you with?"}
	]


@st.cache_resource(show_spinner=False)
def load_data():
	with st.spinner(text="Loading and indexing the docs – hang tight! This should take a few minutes."):
		

		# ####reading local documents
		# reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
		# docs = reader.load_data()
		# service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
		# index = VectorStoreIndex.from_documents(docs, service_context=service_context)
		
		### Reading website - give URLs in an array
		SimpleWebPageReader = download_loader("SimpleWebPageReader")
		loader = SimpleWebPageReader()
		docs = loader.load_data(urls=[
			"https://www.hopkinsmedicine.org/-/media/johns-hopkins-health-plans/documents/2022_hedis_quality_measures_tip_sheet.pdf",
			"https://healthinsuranceratings.ncqa.org/2019/search/Commercial/MI",
			"https://healthinsuranceratings.ncqa.org/2019/HprPlandetails.aspx?id=1434"
			])

		service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=
			"You are expected to answer questions about HEDIS scores, factors influencing HEDIS, improvement suggestions, and any other information related to HEDIS. Also answer questions based on data shown in the 3 websites provided to you. Those websites contain very valuable data, but make sure the data is accurately depicted from the websites used in the tool. Providing information about Blue Cross Blue Shield of Michigan, or also referred to as BCBSM, is good."))
		index = VectorStoreIndex.from_documents(docs, service_context=service_context)


		return index

index = load_data()

# # Persist index to disk
# index.storage_context.persist("hedis_index")

# # Rebuild storage context
# storage_context = StorageContext.from_defaults(persist_dir="hedis_index")

# # Load index from the storage context
# new_index = load_index_from_storage(storage_context)


# LlamaIndex has four different chat engines:

# condense_question engine: Always queries the knowledge base. Can have trouble with meta questions like “What did I previously ask you?”
# context: Always queries the knowledge base and uses retrieved text from the knowledge base as context for following queries. The retrieved context from previous queries can take up much of the available context for the current query.
# React: Chooses whether to query the knowledge base or not. Its performance is more dependent on the quality of the LLM. You may need to coerce the chat engine to correctly choose whether to query the knowledge base.
# openai : Chooses whether to query the knowledge base or not—similar to ReAct agent mode, but uses OpenAI’s built-in fuOpenAI'salling capabilities.


chat_engine = new_index.as_chat_engine(chat_mode="context", verbose=True)

# chat_engine_external = index.as_chat_engine(chat_mode="openai", verbose=True)


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
	st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
	with st.chat_message(message["role"]):
		st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
	with st.chat_message("assistant"):
		with st.spinner("Thinking..."):
			# if "search the web" in (str(st.session_state.messages[-1]).lower()):
			#     response = chat_engine.chat(prompt)
			# else:
			#     response = chat_engine_external.chat(prompt)
			
			if "chart" in (str(st.session_state.messages[-1]).lower()):
				st.altair_chart(chart) #, use_container_width=True)
			else:
				response = chat_engine.chat(prompt)
				st.write(response.response)
				message = {"role": "assistant", "content": response.response}
				st.session_state.messages.append(message) # Add response to message history