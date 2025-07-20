import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    # Load inputs
    swagger = swagger_file.read_text()
    requirements = requirements_file.read_text()

    # ------------------------
    # Step 1: Generate scenarios
    # ------------------------
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

    # ------------------------
    # Step 2: Generate pytest test code
    # ------------------------
    test_code = ["import requests", "BASE_URL = 'http://localhost:8000'"]

    for scenario in scenario_lines:
        prompt = (
            f"Given the following OpenAPI spec:\n{swagger}\n\n"
            f"And this test scenario:\n{scenario}\n\n"
            "Write a Python pytest test function using the requests library. Only include valid Python code."
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

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    formatted_lines.append("")
                elif stripped.startswith("def ") or stripped.startswith("import ") or stripped.startswith("@") or stripped.startswith("from ") or stripped.startswith("assert") or stripped.startswith("requests.") or stripped.startswith("BASE_URL") or line.startswith("    "):
                    formatted_lines.append(line)
                else:
                    formatted_lines.append(f"# {line}")

            test_code.append("\n".join(formatted_lines))

        except Exception as e:
            print(f"❌ Error generating test for scenario: {scenario}\n  ➤ {e}")
            test_code.append(f"# Error generating test for scenario: {scenario}\n# {e}")

    output_test_file.write_text("\n\n".join(test_code))
    print(f"✅ Tests written to: {output_test_file}")
