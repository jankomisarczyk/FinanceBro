from typing import List

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

from src.interns.step import Execution
from src.llmopenai import Argument, ItemsType
from src.plugins.plugin import Plugin

PLUGIN_NAME = "create_vector_store_from_pdfs"
PLUGIN_DESCRIPTION = "Creates vector store from a list of .pdf files."
ARGS_SCHEMA = {
    "pdfs_list": Argument(type="array", items=ItemsType(type="string"), minItems=1, uniqueItems=True, description="A list with .pdf file names.")
}
    

class CreateVectorStoreFromPDFs(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["pdfs_list"]
    categories = ["Vector Store"]
    
    @staticmethod
    async def arun(pdfs_list: List[str]) -> Execution:
        try:
            docs = []

            for pdf in pdfs_list:
                loader = PyPDFLoader(pdf)
                sub_docs = loader.load()
                for doc in sub_docs:
                    doc.metadata["source"] = pdf
                docs.extend(sub_docs)
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)

            for id, chunk in enumerate(chunks):
                chunk.metadata["UID"] = id
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(chunks, embeddings)
            # first ten char of first pdf name
            vs_name = f"vector_store_{pdfs_list[0][:10]}"
            vectorstore.save_local(vs_name)
            
            # ADD observtion for user in frontend so that ==>> If you want to query it, you can write e.g. 'Query {vs_name}: <list of questions separated with commas>'.
            return Execution(
                observation=f"Successfully created vector store under name {vs_name}.",
                set_files={vs_name: "Vector Store"},
                info=f'Vector store "{vs_name}" created'
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {CreateVectorStoreFromPDFs.name}: {e}"
            )
