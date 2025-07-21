import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def generate_scenarios_for_api(api_dir):
    """Generate test scenarios from requirements and swagger spec for a single API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    requirements_file = api_dir / "requirements.txt"
    swagger_file = api_dir / "swagger.yaml"
    scenario_output_file = api_dir / "scenarios.txt"
    
    if not requirements_file.exists():
        print(f"❌ Requirements file not found: {requirements_file}")
        return None
    
    if not swagger_file.exists():
        print(f"❌ Swagger file not found: {swagger_file}")
        return None
    
    requirements = requirements_file.read_text()
    swagger = swagger_file.read_text()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a QA analyst. Generate clear API test scenarios from requirements and OpenAPI specifications."},
                {"role": "user", "content": f"Based on the following API requirements:\n\n{requirements}\n\nAnd this OpenAPI specification:\n\n{swagger}\n\nGenerate concise test scenarios that cover both the requirements and API endpoints. Each scenario should be one line only."}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        scenario_text = response.choices[0].message.content
        scenario_lines = [line.strip("- ").strip() for line in scenario_text.splitlines() if line.strip()]
        scenario_output_file.write_text("\n".join(scenario_lines))
        print(f"✅ Scenarios generated: {scenario_output_file}")
        return scenario_lines
        
    except Exception as e:
        print(f"❌ Error generating scenarios for {api_dir.name}: {e}")
        return None

def generate_all_scenarios():
    """Generate scenarios for all APIs in the apis directory."""
    api_base_dir = Path("apis")
    
    for api_dir in api_base_dir.iterdir():
        if api_dir.is_dir():
            generate_scenarios_for_api(api_dir)

if __name__ == "__main__":
    generate_all_scenarios()