import os
import pickle
from typing import Dict, List

from langchain.schema.document import Document
from langchain.vectorstores.faiss import FAISS
from mip import *

from src.interns.step import Execution
from src.llmopenai import Argument, ItemsType, Message, call_llm
from src.plugins.plugin import Plugin

PLUGIN_NAME = "query_vector_store"
PLUGIN_DESCRIPTION = "Answers a list of questions based on the relevant pieces of context found in a specified vector store."
ARGS_SCHEMA = {
    "vector_store_name": Argument(type="string", description="The name of the vector store which will be searched for answers to the list of questions asked."),
    "questions_list": Argument(type="array", items=ItemsType(type="string"), minItems=1, uniqueItems=True, description="A list of questions.")
}
    

class QueryVectorStore(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["vector_store_name", "questions_list"]
    categories = ["Vector Store"]
    
    @staticmethod
    async def arun(vector_store_name: str, questions_list: List[str]) -> Execution:
        try:
            if not os.path.exists(vector_store_name):
                return Execution(observation="Vector store not found")
            
            question_to_contexts = QueryVectorStore.retrive_chunks(vector_store_name, questions_list)

            output = (
                "The AI Assistant has searched the provided vector store and found the following answers:\n"
            )

            for question, contexts in question_to_contexts.items():
                context = QueryVectorStore.create_context([doc.page_content for doc in contexts])
                prompt = QUESTION_TEMPLATE.format(context=context, question=question)
                response = await call_llm(messages=[Message(role="user", content=prompt)])
                output += ANSWER_TEMPLATE.format(question=question, answer=response)
            
            return Execution(
                observation=output
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {QueryVectorStore.name}: {e}"
            )
    
    @staticmethod
    def create_context(contexts_list: List[str]) -> str:
        count = 0
        table = []
        for context in contexts_list:
            count += 1
            table.append(f"Context {count}: `{context}`")
        return "\n".join(table)

    @staticmethod
    def retrive_chunks(vector_store_name: str, questions: List[str]) -> Dict[str, List[Document]]:
        with open(vector_store_name, 'rb') as f:
            vectorstore: FAISS = pickle.load(f)
        ss_result = {}
        retrieved_k = 20
        for qi in questions:
            ss_result[qi] = vectorstore.similarity_search_with_relevance_scores(query=qi, k=retrieved_k)

        col = len(questions) # number of queries
        C = []
        index_to_id = {}
        id_to_index = {}
        id_to_doc = {}
        index = 0
        for j, qi in enumerate(ss_result):
            for tupl in ss_result[qi]:
                if tupl[0].metadata["UID"] in id_to_index:
                    C[id_to_index[tupl[0].metadata["UID"]]][j] = tupl[1]
                else:
                    index_to_id[index] = tupl[0].metadata["UID"]
                    id_to_index[tupl[0].metadata["UID"]] = index
                    id_to_doc[tupl[0].metadata["UID"]] = tupl[0]
                    C.append([-1] * col)
                    C[index][j] = tupl[1]
                    index += 1

        count = 0
        for i in C:
            for j in i:
                if j != -1:
                    count += 1
        assert count == col * retrieved_k, "C matrix was NOT created correctly"

        #generate model
        k = 3
        mip_model = Model()
        #variables in model
        x = {}
        row = len(C)
        assert k*col <= row, "Not enough unique chunks retrieved"

        for i in range(row):
            for j in range(col):
                x[i, j] = mip_model.add_var(var_type=BINARY, name='x({},{})'.format(i, j))

        #objective
        mip_model.objective = maximize(xsum(C[i][j] * x[i, j] for i, j in x))

        #constraints
        for j in range(col):
            mip_model.add_constr(xsum(x[i, j] for i in range(row)) == k)

        for i in range(row):
            mip_model.add_constr(xsum(x[i, j] for j in range(col)) <= 1)

        status = mip_model.optimize()
        assert status == OptimizationStatus(0), "No solution was found"

        #reading out solution
        sol = [[None for _ in range(col)] for _ in range(row)]
        for i, j in x:
            sol[i][j] = int(x[i, j].x)

        output = {}
        for j in range(col):
            output[questions[j]] = []
            for i in range(row):
                if sol[i][j] == 1:
                    output[questions[j]].append(id_to_doc[index_to_id[i]])

        return output

QUESTION_TEMPLATE = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just output `No information found in the vector store`, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
{context}
Question: {question}
Helpful Answer:"""

ANSWER_TEMPLATE = """Answer to "{question}": {answer}"""