

**API Documentation**
=======================

**Overview**
------------

This API provides a set of endpoints for interacting with our system. The API is built using FastAPI and is designed to be easy to use and understand.

**Endpoints**
------------

### 1. Report Endpoint

* **URL:** `/report`
* **Method:** `POST`
* **Parameters:**
	+ `question`: a string parameter representing the question to generate a report for
* **Description:** Generates html report for the provided question
* **Returns:** The report contains an overview,sql query used,the sql query output and graph based
               on question asked

### 2. RAG PDF Endpoint

* **URL:** `/rag-pdf`
* **Method:** `POST`
* **Parameters:**
	+ `question`: a string parameter representing the question asked
* **Description:** Provides a response based on the uploaded PDF vectors stored on AWS S3.
* **Returns:** The result of running the RAG query for the provided question

### 3. Text-to-SQL Endpoint

* **URL:** `/text-sql`
* **Method:** `POST`
* **Parameters:**
	+ `question`: a string parameter representing the question to generate a SQL query for
	+ `session_id`: an optional string parameter representing the session ID
* **Description:** Generates a SQL query for the provided question
* **Returns:** The result of running the text-to-SQL query for the provided question

### 4. Extract Image Endpoint

* **URL:** `/extract-image`
* **Method:** `POST`
* **Parameters:**
	+ `file`: an uploaded image file
	+ `question`: a string parameter representing the question related to the image
* **Description:** Extracts text from the uploaded image and generates a vector representation
* **Returns:** The result of running the image extraction and vector generation for the provided image and question

**API Reference**
-----------------

### Report Endpoint

* **Function:** `report`
* **Path:** `/report`
* **Method:** `POST`
* **Parameters:**
	+ `question`: `str` = `Form(...)`
* **Returns:** `run_agents(question)`

### RAG PDF Endpoint

* **Function:** `rag_pdf`
* **Path:** `/rag-pdf`
* **Method:** `POST`
* **Parameters:**
	+ `question`: `str` = `Form(...)`
* **Returns:** `run_rag_query(question)`

### Text-to-SQL Endpoint

* **Function:** `rag_text_sql`
* **Path:** `/text-sql`
* **Method:** `POST`
* **Parameters:**
	+ `question`: `str` = `Form(...)`
	+ `session_id`: `str` = `Form(None)`
* **Returns:** `run_txt_sql_query(session_id, memory_store, question)`

### Extract Image Endpoint

* **Function:** `rag_image`
* **Path:** `/extract-image`
* **Method:** `POST`
* **Parameters:**
	+ `file`: `UploadFile` = `File(...)`
	+ `question`: `str` = `Form(...)`
* **Returns:** `run_extract_image(file, question)`

**Tools**
--------

### `tools.db_utils`

* **Function:** `get_sql_database`
* **Description:** Returns a SQL database connection

### `tools.chart_utils`

* **Function:** `generate_chart`
* **Description:** Returns different types of charts, such as bar or pie, based on the data provided.

**Services**
------------

### `services.generate_report`

* **Function:** `run_agents`
* **Description:** Runs the autogen agents for the provided question
* **Returns:** The result of running the agents

### `services.text_to_sql`

* **Function:** `run_txt_sql_query`
* **Description:** Runs the text-to-SQL query for the provided question and session ID
* **Returns:** The result of running the text-to-SQL query

### `services.rag_process`

* **Function:** `run_rag_query`
* **Description:** Runs the RAG query for the provided question
* **Returns:** The result of running the RAG query

### `services.image_process`

* **Function:** `run_extract_image`
* **Description:** Extracts text from the uploaded image and generates a vector representation
* **Returns:** The result of running the image extraction and vector generation
