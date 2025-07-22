# AI-Powered Kubernetes YAML Generator

This tool automates the creation of Kubernetes manifests from high-level YAML specifications. It watches a directory for changes to `spec` files and uses the Groq AI service to generate the corresponding Kubernetes `Deployment` and `Service` manifests.

## How it Works

1.  **Watch**: The script continuously monitors the `specs/` directory for any new or modified `.yaml` files.
2.  **Configure**: It reads the `config.yaml` file to get the generation instructions and output patterns.
3.  **Generate**: When a file is detected, its content is combined with the instructions from the config to form a prompt for the Groq API.
4.  **Write**: The AI-generated Kubernetes manifest is then saved to the `generated/` directory, with a filename derived from the original spec file.

## Project Structure

```
yaml-generator/
├── specs/
│   └── (Your input spec files go here, e.g., my-service.yaml)
├── generated/
│   └── (Generated Kubernetes manifests will appear here)
├── config.yaml
├── main.py
├── ai_generator.py
├── requirements.txt
└── README.md
```

## Setup and Installation

### Prerequisites

-   Python 3.6+
-   `pip` for installing dependencies

### Installation

1.  **Clone the repository (or download the files).**

2.  **Navigate to the project directory:**
    ```bash
    cd yaml-generator
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    Open the `ai_generator.py` file and add your Groq API key.
    ```python
    # ai_generator.py
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
    ```
    Alternatively, you can set it as an environment variable named `GROQ_API_KEY`.

## Usage

1.  **Configure the Generator:**
    Modify the `config.yaml` file to define your desired transformation. The `instruction` field is crucial as it tells the AI what to do.

2.  **Create a Spec File:**
    Add a new `.yaml` file inside the `specs/` directory. For example, create `specs/my-api.yaml` with content like:
    ```yaml
    serviceName: my-api
    image: my-company/my-api:1.2.3
    replicas: 2
    port: 8080
    env:
      - name: DATABASE_URL
        value: "production_db_url"
      - name: API_KEY
        valueFrom:
          secretKeyRef:
            name: api-secrets
            key: key
    ```

3.  **Run the Watcher:**
    Execute the main script from the root of the `yaml-generator` directory:
    ```bash
    python main.py
    ```
    The script will now be watching for file changes.

4.  **Check the Output:**
    After you save the spec file, the tool will process it, and a new file named `my-api-deployment.yaml` (based on the default `outputPattern`) will be created in the `generated/` directory.

## Note on the AI Model

This version uses the **Groq API** with the `llama3-8b-8192` model to generate manifests. The `ai_generator.py` script contains the logic for calling the API. Ensure you have a valid Groq API key configured for it to work.