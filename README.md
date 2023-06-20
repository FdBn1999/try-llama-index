# try-llama-index

[LlamaIndex🦙](https://gpt-index.readthedocs.io/en/latest/)<br>
[FastApi](https://fastapi.tiangolo.com/)

I use FastApi and LlamaIndex libraries to create a simple api for querying own private documents. <br>
This is a proof of concept for the LlamaIndex Framework. The idea is to improve this development through research on LLMs, GPT models, indexes, and other related aspects.

**How to use?**

1. Create your own virtual environment (using venv).
2. Install dependencies (using the `requirements.txt` file).
3. Create a dotenv file at the root of the project and add the following three values:
    - `CONNECTION_STRING` - A MongoDB connection string.
    - `DBNAME` - MongoDB database name.
    - `OPENAI_API_KEY` - OpenAI API Key.
4. Create `documents` folder at the root of the project and insert some document.
5. If you don't have an index created yet, set the index_exists variable to `false`, and your index will be created using the documents from the documents folder. Otherwise, set it to `true`.
6. Use the following command to run the application: `uvicorn main:app`

**Limitations** (From the project, not the Framework)

1. Only support `.txt` files.
2. The first time the application is executed, it is necessary to have the `documents` folder created at the root of the project.
3. You can only insert new documents, existing ones cannot be deleted or updated.

**Next steps** <br>
????
