

# generate_tests.py
# -----------------
# This script generates API test scenarios and pytest test code using OpenAI's GPT models.
# It ensures all generated test functions accept an 'access_token' parameter for authentication.


import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (e.g., OPENAI_API_KEY, BASE_URL)
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get BASE_URL from environment
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Define base directories for APIs and output tests
api_base_dir = Path("apis")
output_base_dir = Path("tests")

for api_dir in api_base_dir.iterdir():
    if not api_dir.is_dir():
        continue

    swagger_file = api_dir / "swagger.yaml"
    requirements_file = api_dir / "requirements.txt"
    scenario_output_file = api_dir / "scenarios.txt"

    output_test_file = output_base_dir / api_dir.name / f"test_{api_dir.name}_generated.py"
    output_test_file.parent.mkdir(parents=True, exist_ok=True)

    # Load API requirements and OpenAPI spec
    swagger = swagger_file.read_text()
    requirements = requirements_file.read_text()

    # --------------------------------------------------
    # Step 1: Generate test scenarios from requirements
    # --------------------------------------------------
    try:
        scenario_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a QA analyst. Generate clear API test scenarios from the given software requirements."},
                {"role": "user", "content": f"Based on the following API requirements, list concise test scenarios:\n\n{requirements}\n\nEach scenario should be one line only."}
            ],
            temperature=0.3,
            max_tokens=500
        )
        scenario_text = scenario_response.choices[0].message.content
        scenario_lines = [line.strip("- ").strip() for line in scenario_text.splitlines() if line.strip()]
        scenario_output_file.write_text("\n".join(scenario_lines))
        print(f"✅ Scenarios generated: {scenario_output_file}")
    except Exception as e:
        print(f"❌ Error generating scenarios for {api_dir.name}: {e}")
        continue

    # --------------------------------------------------
    # Step 2: Generate pytest test code for each scenario
    # --------------------------------------------------


    # Header for generated test file
    test_code = [
        "import requests",
        "import pytest",
        "import os",
        "from dotenv import load_dotenv",
        "",
        "load_dotenv()  # Load environment variables from .env",
        "BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')",
        "",
        "def get_endpoint_url(path):",
        "    \"\"\"Helper to get the full endpoint URL from BASE_URL and a path (e.g. '/login').\"\"\"",
        "    return f'{BASE_URL.rstrip('/')}/{path.lstrip('/')}';",
        "",
        "# The 'access_token' fixture is provided by conftest.py and reads sensitive values from your .env file.",
        "# Do NOT store secrets in source code. Use a .env file (not committed to git) for sensitive info.",
        "# All test functions below require 'access_token' as a parameter.",
    ]

    for scenario in scenario_lines:
        prompt = (
            f"Given the following OpenAPI spec:\n{swagger}\n\n"
            f"And this test scenario:\n{scenario}\n\n"
            "Write a Python pytest test function using the requests library. "
            "Assume there is a pytest fixture called 'access_token' that provides a valid token string. "
            "The test function should accept 'access_token' as a parameter and use it in the Authorization header as 'Bearer {access_token}'. "
            "Do NOT hardcode any client_id, client_secret, or sensitive info. Only include valid Python code. "
            "Use the helper function get_endpoint_url(path) to construct the full endpoint URL from BASE_URL and the endpoint path (e.g., '/login'). "
            "Do NOT hardcode the full URL in the test."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes Python test functions using pytest and requests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )

            raw_content = response.choices[0].message.content
            lines = raw_content.splitlines()
            formatted_lines = []
            inside_func = False

            for line in lines:
                stripped = line.strip()
                # Detect function definition and ensure 'access_token' is present
                if stripped.startswith("def "):
                    inside_func = True
                    if "access_token" not in stripped:
                        # Insert access_token as a parameter
                        name, rest = stripped.split("(", 1)
                        params = rest.split(")", 1)[0]
                        params = params.strip()
                        params = (params + ", ") if params else ""
                        new_def = f"{name}({params}access_token):"
                        formatted_lines.append(new_def)
                    else:
                        formatted_lines.append(line)
                elif inside_func and stripped == "":
                    # End of function
                    inside_func = False
                    formatted_lines.append("")
                elif inside_func or (
                    stripped.startswith("import ") or
                    stripped.startswith("@") or
                    stripped.startswith("from ") or
                    stripped.startswith("assert") or
                    stripped.startswith("requests.") or
                    stripped.startswith("BASE_URL") or
                    stripped.startswith("get_endpoint_url") or
                    line.startswith("    ")
                ):
                    # Replace any hardcoded URLs with get_endpoint_url if found
                    if '"http' in line and '/"' in line:
                        # Try to extract the path
                        import re
                        match = re.search(r'"http[^"]+(/[^"\s]*)"', line)
                        if match:
                            path = match.group(1)
                            new_line = line.replace(match.group(0), f'get_endpoint_url("{path}")')
                            formatted_lines.append(new_line)
                        else:
                            formatted_lines.append(line)
                    else:
                        formatted_lines.append(line)
                else:
                    # Comment out any non-code lines
                    formatted_lines.append(f"# {line}")

            test_code.append("\n".join(formatted_lines))

        except Exception as e:
            print(f"❌ Error generating test for scenario: {scenario}\n  ➤ {e}")
            test_code.append(f"# Error generating test for scenario: {scenario}\n# {e}")

    # Write all generated test code to output file
    output_test_file.write_text("\n\n".join(test_code))
    print(f"✅ Tests written to: {output_test_file}")
