import logging
import os
import yaml
from groq import Groq

# --- Configuration ---
# Add your Groq API key here
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
MODEL = 'llama3-8b-8192'

client = Groq(api_key=GROQ_API_KEY)

def generate_manifest(instruction, spec_content):
    """
    Generates a Kubernetes manifest using the Groq API.
    """
    logging.info("--- Generating manifest with Groq ---")

    if GROQ_API_KEY == "YOUR_GROQ_API_KEY":
        logging.error("Groq API key not configured. Please set the GROQ_API_KEY environment variable or update it in the script.")
        return "# ERROR: Groq API key not configured."

    try:
        prompt = f"""
Generate a Kubernetes manifest based on the following instruction and service specification.
The output should be a single YAML string with multiple documents separated by '---'.

Instruction:
{instruction}

Service Specification (YAML):
{spec_content}

Kubernetes Manifest (YAML):
"""
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL,
        )

        raw_manifest = chat_completion.choices[0].message.content
        
        # Clean up the response to ensure it's valid YAML
        try:
            # Remove markdown code blocks if they exist
            if "```" in raw_manifest:
                # Find content between ```yaml and ``` or just ``` and ```
                if "```yaml" in raw_manifest:
                    raw_manifest = raw_manifest.split("```yaml")[1].split("```")[0].strip()
                else:
                    raw_manifest = raw_manifest.split("```")[1].split("```")[0].strip()

            # Parse all YAML documents and then dump them back to a string
            # This effectively removes any non-YAML text before or after the documents.
            docs = list(yaml.safe_load_all(raw_manifest))
            manifest = yaml.dump_all(docs, default_flow_style=False, sort_keys=False)
            
        except yaml.YAMLError as e:
            logging.error(f"Error parsing generated YAML: {e}")
            logging.debug(f"Problematic manifest content:\n{raw_manifest}")
            # Fallback to simpler cleaning if parsing fails
            yaml_start_index = raw_manifest.find("---")
            if yaml_start_index != -1:
                manifest = raw_manifest[yaml_start_index:]
            else:
                manifest = raw_manifest # return as is if no --- is found
        
        logging.info("Successfully generated manifest with Groq.")
        return manifest

    except Exception as e:
        logging.error(f"Error generating manifest with Groq: {e}")
        return f"# ERROR: Could not generate manifest: {e}"