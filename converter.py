import pandas as pd
import json
import xml.etree.ElementTree as ET
import yaml
import os
import logging
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uvicorn
#pip install fastapi pandas pyyaml openpyxl lxml uvicorn
#Running the Program:
#Save the code as file_converter.py.
#Run the server: python file_converter.py.
#The server will start at http://localhost:8000.
#Usage:
#Send a POST request to /convert with:
#A file upload (form-data field: file).
#A query parameter output_format (e.g., csv, json, xml, yaml, xlsx).

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="File Format Converter")

# Supported formats
SUPPORTED_FORMATS = {'csv', 'json', 'xml', 'yaml', 'xlsx'}

def validate_file_extension(filename: str, expected_extension: str) -> bool:
    """Validate if the file has the expected extension."""
    return filename.lower().endswith(f'.{expected_extension}')

def read_csv(file_path: str) -> pd.DataFrame:
    """Read CSV file into DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")

def read_json(file_path: str) -> pd.DataFrame:
    """Read JSON file into DataFrame."""
    try:
        return pd.read_json(file_path)
    except Exception as e:
        logger.error(f"Error reading JSON: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading JSON: {str(e)}")

def read_xml(file_path: str) -> pd.DataFrame:
    """Read XML file into DataFrame."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for elem in root:
            record = {}
            for subelem in elem:
                record[subelem.tag] = subelem.text
            data.append(record)
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error reading XML: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading XML: {str(e)}")

def read_yaml(file_path: str) -> pd.DataFrame:
    """Read YAML file into DataFrame."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error reading YAML: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading YAML: {str(e)}")

def read_xlsx(file_path: str) -> pd.DataFrame:
    """Read Excel file into DataFrame."""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        logger.error(f"Error reading Excel: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading Excel: {str(e)}")

def write_csv(df: pd.DataFrame, output_path: str):
    """Write DataFrame to CSV."""
    try:
        df.to_csv(output_path, index=False)
    except Exception as e:
        logger.error(f"Error writing CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error writing CSV: {str(e)}")

def write_json(df: pd.DataFrame, output_path: str):
    """Write DataFrame to JSON."""
    try:
        df.to_json(output_path, orient='records', indent=2)
    except Exception as e:
        logger.error(f"Error writing JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error writing JSON: {str(e)}")

def write_xml(df: pd.DataFrame, output_path: str):
    """Write DataFrame to XML."""
    try:
        root = ET.Element("root")
        for _, row in df.iterrows():
            record = ET.SubElement(root, "record")
            for col, value in row.items():
                field = ET.SubElement(record, col)
                field.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(output_path)
    except Exception as e:
        logger.error(f"Error writing XML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error writing XML: {str(e)}")

def write_yaml(df: pd.DataFrame, output_path: str):
    """Write DataFrame to YAML."""
    try:
        with open(output_path, 'w') as f:
            yaml.dump(df.to_dict('records'), f, default_flow_style=False)
    except Exception as e:
        logger.error(f"Error writing YAML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error writing YAML: {str(e)}")

def write_xlsx(df: pd.DataFrame, output_path: str):
    """Write DataFrame to Excel."""
    try:
        df.to_excel(output_path, index=False)
    except Exception as e:
        logger.error(f"Error writing Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error writing Excel: {str(e)}")

# File reader and writer mappings
READERS = {
    'csv': read_csv,
    'json': read_json,
    'xml': read_xml,
    'yaml': read_yaml,
    'xlsx': read_xlsx
}

WRITERS = {
    'csv': write_csv,
    'json': write_json,
    'xml': write_xml,
    'yaml': write_yaml,
    'xlsx': write_xlsx
}

@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    output_format: str = "csv"
):
    """Convert uploaded file to specified output format."""
    if output_format.lower() not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail=f"Unsupported output format. Choose from {SUPPORTED_FORMATS}")

    input_filename = file.filename
    input_extension = input_filename.split('.')[-1].lower()
    
    if input_extension not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail=f"Unsupported input format. Choose from {SUPPORTED_FORMATS}")

    # Save uploaded file temporarily
    temp_input_path = f"temp_{input_filename}"
    try:
        with open(temp_input_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Read input file
        df = READERS[input_extension](temp_input_path)

        # Generate output filename
        output_filename = f"converted_{input_filename.rsplit('.', 1)[0]}.{output_format}"
        output_path = f"output_{output_filename}"

        # Write to output format
        WRITERS[output_format](df, output_path)

        # Return the converted file
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type='application/octet-stream'
        )

    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

    finally:
        # Clean up temporary files
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)