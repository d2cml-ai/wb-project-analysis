import pinecone
import os
import pandas as pd
import numpy as np
import itertools
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()
indexName = "wb-projects"
embeddings = OpenAIEmbeddings()
projects = pd.read_csv("vector_base/projects_data.csv")
projectDataFieldNames = [
        "projectid",
        "pdfurl",
        "project_components_2"
]
vectorBatchSize = 50
dataBatchSize = 100

def getVectorsFromData(data):
        vectorIds = list(data["projectid"])
        textEmbeddings = embeddings.embed_documents(list(data["project_components_2"]))
        textMetadatas = [{"url": row["pdfurl"], "text": row["project_components_2"]} for index, row in data.iterrows()]
        return tuple(zip(vectorIds, textEmbeddings, textMetadatas))

def createBatchOfVectors(vectors, batchSize):
        vectorIterations = iter(vectors)
        vectorBatch = itertools.islice(vectorIterations, batchSize)

        while vectorBatch:
                yield vectorBatch
                vectorBatch = tuple(itertools.islice(vectorIterations, batchSize))

def batchUpsertVectors(vectors, batchSize, pineconeIndex):
        for batch in createBatchOfVectors(vectors, batchSize):
                pineconeIndex.upsert(
                        vectors=vectors,
                )

def main():
        projectDataFields = projects[projectDataFieldNames]
        projectDataFields = projectDataFields[projectDataFields["project_components_2"].notna()]
        pinecone.init()
        
        if indexName not in pinecone.list_indexes():
                pinecone.create_index(
                        name=indexName,
                        metric="cosine",
                        dimension=1536
                )
        
        pineconeIndex = pinecone.Index(indexName)

        for batch in np.array_split(projectDataFields, dataBatchSize):
                vectors = getVectorsFromData(batch)
                batchUpsertVectors(vectors, vectorBatchSize, pineconeIndex)

        

if __name__ == "__main__":
        main()
