import time
import logging
import yaml
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai_generator import generate_manifest

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def load_config():
    """Loads the configuration from config.yaml."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def process_file(file_path):
    """
    Processes a single spec file based on the configuration.
    """
    try:
        config = load_config()
        
        with open(file_path, 'r') as f:
            spec_content = f.read()
        
        logging.info(f"--- Processing Spec: {file_path} ---")
        
        # Call the AI to get the generated YAML
        generated_yaml = generate_manifest(config['instruction'], spec_content)

        # Determine the output path
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_pattern = config.get('outputPattern', 'generated/{{name}}.yaml')
        output_path = output_pattern.replace('{{name}}', base_name)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the generated content to the output file
        with open(output_path, 'w') as f:
            f.write(generated_yaml)
            
        logging.info(f"Successfully generated manifest at: {output_path}")

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")


class SpecChangeHandler(FileSystemEventHandler):
    """Handles file system events for spec files."""
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".yaml"):
            logging.info(f"Detected change in: {event.src_path}")
            process_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".yaml"):
            logging.info(f"New file detected: {event.src_path}")
            process_file(event.src_path)

import sys

def main():
    """Main function to start the file watcher or run once."""
    path = 'specs'
    if not os.path.exists(path):
        logging.error(f"Directory not found: '{path}'. Please run this script from the 'yaml-generator' root.")
        return

    # If any command-line argument is provided, run once and exit
    if len(sys.argv) > 1:
        logging.info("Running in single-run mode...")
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".yaml"):
                    process_file(os.path.join(root, file))
        logging.info("Single run finished.")
        return

    # Default behavior: watch for changes
    event_handler = SpecChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    logging.info(f"Watching for changes in '{path}' directory...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Observer stopped.")
    
    observer.join()

if __name__ == "__main__":
    main()