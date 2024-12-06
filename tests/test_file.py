import os
import pytest
from fastapi.testclient import TestClient
from main import app
import logging

# Directories
TEST_UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "test_uploads")  # test file location
TEST_FILE_PATH = os.path.join(TEST_UPLOADS_DIR, "test.pdf")  # Path to the test file to upload
UPLOADS_DIR = os.path.join("resources", "uploads")  # Directory where file will be uploaded

@pytest.fixture(scope="session")
def client():
    """Fixture to create a TestClient for the entire test session."""
    return TestClient(app)

@pytest.fixture(scope="session")
def test_file():
    """Fixture to get the path of the test file."""
    file_path = os.path.join(TEST_UPLOADS_DIR, "test.pdf")

    # Ensure the test file exists for the tests
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    return file_path

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_file(request):
    """Fixture to clean up the uploaded test file after all tests are done."""
    
    # Register finalizer to clean up after all tests
    def cleanup():
        # Clean up the uploaded file in resources/uploads
        uploaded_file_path = os.path.join(UPLOADS_DIR, "test.pdf")
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
            logging.info(f"Removed uploaded test file: {uploaded_file_path}")
        else:
            logging.info(f"File not found for cleanup: {uploaded_file_path}")

    # Register the finalizer to run after all tests in the session
    request.addfinalizer(cleanup)

def test_upload_file(client, test_file):
    # Open the test file and prepare the file data
    with open(test_file, 'rb') as f:
        file_data = {
            "file": (os.path.basename(test_file), f, "application/pdf")  # (filename, file-like object, content type)
        }

        # Send a POST request to upload the file
        response = client.post("user/upload_file", files=file_data)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert the expected response content (JSON)
        response_json = response.json()
        assert response_json["filename"] == os.path.basename(test_file)
        assert response_json["message"] == "File uploaded successfully"

def test_upload_file_error(client):
    # Simulate a request with no file (to trigger the error case)
    response = client.post("user/upload_file")
    
    # Assert that the response status code is 422 (Internal Server Error)
    assert response.status_code == 422

def test_stream_file(client, test_file):
    # Test streaming the existing file
    response = client.get(f"user/stream_file?file_name={os.path.basename(test_file)}")

    # Check status code and headers
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"

    # Read file content as binary (since it might not be a UTF-8 file)
    with open(test_file, "rb") as f:
        expected_file_content = f.read()

    # Check that the binary content of the file matches
    assert response.content == expected_file_content

# Test case when the file doesn't exist
def test_file_not_found(client):
    # Test streaming a non-existent file
    response = client.get("user/stream_file?file_name=non_existent_file.txt")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}