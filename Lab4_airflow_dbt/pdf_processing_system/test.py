import requests

# Use a publicly accessible PDF URL
# pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"  # Example public PDF
pdf_url = "https://cfapublications.s3.us-east-1.amazonaws.com/assignment3/pdfs/A+Cash-Flow+Focus+for+Endowments+and+Trusts.pdf"
response = requests.post(
    'http://localhost:5001/submit',
    json={
        'pdf_url': pdf_url,
        'options': {'quality': 'high'},
        'submitted_by': 'test@example.com'
    }
)

print(response.json())