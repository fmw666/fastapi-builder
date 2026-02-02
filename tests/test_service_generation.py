import os

from fastapi_builder.constants import Language
from fastapi_builder.context import AppContext
from fastapi_builder.generator import generate_app


def test_service_generation(tmp_path):
    """
    Test that generate_app creates a service.py file.
    """
    # Create a dummy AppContext
    app_name = "test_service_app"
    context = AppContext(
        name=app_name,
        language=Language.EN
    )
    
    # Define output directory
    output_dir = str(tmp_path)
    
    # Run the generator
    generate_app(context, output_dir)
    
    # Expected path for service.py
    # Based on generator.py:
    # filepath = os.path.join(output_dir, f"app_{context.folder_name}")
    app_dir = os.path.join(output_dir, f"app_{context.folder_name}")
    service_file = os.path.join(app_dir, "service.py") 
    
    # Verify the file exists
    assert os.path.exists(service_file), f"service.py was not created at {service_file}"
    
    # Optional: Verify it's not empty or contains expected content if needed, 
    # but existence is the primary goal here.
    with open(service_file) as f:
        content = f.read()
        assert len(content) > 0
