
# API Test Generator using OpenAI and Swagger

This project automates the generation of **pytest-based API test cases** from informal requirements and OpenAPI (`swagger.yaml`) specifications using OpenAI's GPT models.

## 📦 Project Structure

```
api-testgen/
│
├── apis/
│   ├── login/
│   │   ├── swagger.yaml
│   │   ├── requirements.txt
│   │   └── scenarios.txt           # Auto-generated
│   └── register/
│       ├── swagger.yaml
│       ├── requirements.txt
│       └── scenarios.txt           # Auto-generated
│
├── tests/
│   ├── login/
│   │   └── test_login_generated.py
│   └── register/
│       └── test_register_generated.py
│
├── .env                            # Contains your OpenAI API key
├── generate_scenarios.py           # Main script to generate scenarios and tests
├── generate_test_cases.py          # Main script to generate scenarios and tests
├── requirements.txt                # Python dependencies
└── README.md
```

## 🚀 How It Works

1. **Requirements Extraction**  
   Each API module contains a `requirements.txt` file with informal user stories or test expectations.

2. **Scenario Generation (LLM)**  
   GPT is prompted to convert each `requirements.txt` into concise, testable scenarios.

3. **Test Generation (LLM)**  
   Using the scenarios and `swagger.yaml`, GPT generates pytest-compatible Python test functions using the `requests` library.

4. **Test Output**  
   Final test files are saved in `tests/<api>/test_<api>_generated.py`, ready to be run with `pytest`.

## ✅ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pmijar/api-requirements-testgen.git
cd api-requirements-testgen
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 📝 How to Add a New API

1. Create a new folder inside `apis/<your_api_name>/`
2. Add the following files:
   - `swagger.yaml` – OpenAPI spec for the API
   - `requirements.txt` – Informal requirements in bullet/numbered format
3. Run the generator:

```bash
python generate_scenarios.py
```

The script will:
- Generate scenarios within the api named folder and save to `scenarios.txt`

```bash
python generate_test_cases.py
```

The script will:
- Generate testcases and save to `tests/<your_api_name>/test_<your_api_name>_generated.py`


## 🧪 Run the Tests

After generating test files, run pytest:

```bash
pytest tests/
```

## 📄 Sample Requirement (`requirements.txt`)

```
1. The user must provide name, email, and password.
2. Email must be unique.
3. Return 201 Created upon success.
4. Return 409 Conflict if email already exists.
```

## 🤖 Powered By

- [OpenAI GPT-4 API](https://platform.openai.com/docs)
- [Pytest](https://docs.pytest.org/)
- [Swagger/OpenAPI](https://swagger.io/specification/)
- [Python `requests`](https://docs.python-requests.org/)

## 📌 Notes

- The system uses GPT to generate both **scenarios** and **test code**, so output may vary slightly depending on the prompt and model.



