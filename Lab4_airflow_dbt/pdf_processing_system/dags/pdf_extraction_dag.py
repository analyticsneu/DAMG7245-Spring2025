# dags/pdf_extraction_dag.py
from airflow.decorators import dag, task
from datetime import datetime
import requests
import PyPDF2
import io
import markdown
import os
import base64

@dag(
    dag_id="pdf_extraction_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
)
def pdf_extraction_pipeline():
    
    @task
    def download_pdf(**context):
        """Download PDF from URL."""
        try:
            conf = context['dag_run'].conf
            if not conf or 'pdf_url' not in conf:
                raise ValueError("PDF URL not provided in DAG configuration")
            
            pdf_url = conf['pdf_url']
            response = requests.get(pdf_url)
            response.raise_for_status()
            # Convert binary content to base64 string for XCom
            return base64.b64encode(response.content).decode('utf-8')
            
        except Exception as e:
            print(f"Error downloading PDF: {str(e)}")
            raise
    
    @task
    def extract_text(pdf_content_b64):
        """Extract text from PDF content."""
        try:
            # Decode base64 back to binary
            pdf_content = base64.b64decode(pdf_content_b64)
            pdf_file = io.BytesIO(pdf_content)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for i, page in enumerate(reader.pages):
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            raise
    
    @task
    def convert_to_markdown(text):
        """Convert text to Markdown format."""
        try:
            paragraphs = text.split('\n\n')
            md_text = '\n\n'.join(f'{p.strip()}' for p in paragraphs if p.strip())
            return md_text
        except Exception as e:
            print(f"Error converting to markdown: {str(e)}")
            raise
    
    @task
    def save_result(content, **context):
        """Save the markdown result."""
        try:
            conf = context['dag_run'].conf
            task_id = conf.get('task_id', 'unknown')
            
            output_dir = "/opt/airflow/output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = f"{output_dir}/output_{task_id}.md"
            
            with open(output_path, "w") as f:
                f.write(content)
            return output_path
        except Exception as e:
            print(f"Error saving result: {str(e)}")
            raise

    # Define the task flow
    pdf_content = download_pdf()
    text = extract_text(pdf_content)
    md_content = convert_to_markdown(text)
    final_path = save_result(md_content)

dag_instance = pdf_extraction_pipeline()