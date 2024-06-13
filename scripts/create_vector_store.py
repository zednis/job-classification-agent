from openai import OpenAI
from collections.abc import Iterator
import os

client = OpenAI()

VECTOR_STORE_NAME = "ONET 28 Vector Store"

vector_store = client.beta.vector_stores.create(name=VECTOR_STORE_NAME)
print("Vector Store ID: ", vector_store.id)
os.environ["VECTOR_STORE_ID"] = vector_store.id

# # Ready the files for upload to OpenAI
def get_files(directory: str, file_ext=".json") -> Iterator[str]:
    for filename in os.listdir(directory):
        if filename.endswith(file_ext):
            yield os.path.join(directory, filename)


file_paths = [f for f in get_files("../data/processed")]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
print("Uploading files to vector store...")
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)

# # You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)