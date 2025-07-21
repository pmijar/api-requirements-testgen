import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def generate_tests_for_api(api_dir):
    """Generate pytest test cases from scenarios and swagger spec for a single API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    swagger_file = api_dir / "swagger.yaml"
    scenario_file = api_dir / "scenarios.txt"
    output_base_dir = Path("tests")
    output_test_file = output_base_dir / api_dir.name / f"test_{api_dir.name}_generated.py"
    
    if not swagger_file.exists():
        print(f"❌ Swagger file not found: {swagger_file}")
        return
    
    if not scenario_file.exists():
        print(f"❌ Scenarios file not found: {scenario_file}")
        return
    
    output_test_file.parent.mkdir(parents=True, exist_ok=True)
    
    swagger = swagger_file.read_text()
    scenario_lines = scenario_file.read_text().splitlines()
    
    test_code = ["import requests", "BASE_URL = 'http://localhost:8000'"]
    
    for scenario in scenario_lines:
        if not scenario.strip():
            continue
            
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
                elif stripped.startswith(("def ", "import ", "@", "from ", "assert", "requests.", "BASE_URL")) or line.startswith("    "):
                    formatted_lines.append(line)
                else:
                    formatted_lines.append(f"# {line}")
            
            test_code.append("\n".join(formatted_lines))
            
        except Exception as e:
            print(f"❌ Error generating test for scenario: {scenario}\n  ➤ {e}")
            test_code.append(f"# Error generating test for scenario: {scenario}\n# {e}")
    
    output_test_file.write_text("\n\n".join(test_code))
    print(f"✅ Tests written to: {output_test_file}")

def generate_all_tests():
    """Generate test cases for all APIs in the apis directory."""
    api_base_dir = Path("apis")
    
    for api_dir in api_base_dir.iterdir():
        if api_dir.is_dir():
            generate_tests_for_api(api_dir)

if __name__ == "__main__":
    generate_all_tests()