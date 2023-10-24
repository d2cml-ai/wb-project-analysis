import Constants
import pinecone
import pandas as pd
import os

os.environ["PINECONE_API_KEY"] = Constants.PINECONE_API_KEY
os.environ["PINECONE_ENVIRONMENT"] = Constants.PINECONE_ENVIRONMENT
indexName = "wb-projects"
idColumn = "projectid"
updateColumns = ["repnb"]
data = pd.read_csv("vector_base/projects_data.csv")[[idColumn] + updateColumns]
pinecone.init()

def updateIndexEntry(row, pineconeIndex: pinecone.Index):
        vectorId = row[idColumn]
        updateMetadata = dict(zip(updateColumns, row[updateColumns]))
        pineconeIndex.update(
                id=vectorId,
                set_metadata=updateMetadata
        )

def main():
        pineconeIndex = pinecone.Index(indexName)
        for index, row in data.iterrows():
                updateIndexEntry(row, pineconeIndex)

if __name__ == "__main__":
        main()
