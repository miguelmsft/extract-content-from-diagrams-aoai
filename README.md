# Extract Line Number from Diagram with Azure OpenAI  
   
## Description  
   
This repository contains a Python script that processes PDF documents to extract specific line number strings from diagrams using Azure OpenAI's API. The script performs the following steps:  
   
1. **PDF Processing**: Reads all PDF files from the `input_documents` directory.  
2. **Image Conversion**: Converts each page of the PDFs into high-resolution images.  
3. **Image Splitting**: Divides each page image into a 3x3 grid, resulting in 9 image pieces per page. This is so that the AI can better see the small fonts in the images. 
4. **Data Extraction**: Sends each image piece to Azure OpenAI with a custom prompt to extract desired line number strings.  
5. **Result Saving**: Saves the extracted information as JSON files in the `output_results` directory.  
6. **Image Saving**: Optionally saves the generated images and image pieces in the `output_images` directory.  
   
This tool is especially useful for extracting structured data from technical diagrams or schematics where specific line number patterns are present.  
   
---  
   
## Features  
   
- **Automated Batch Processing**: Handles multiple PDFs and pages seamlessly.  
- **High-Resolution Image Generation**: Ensures clarity in the images sent for data extraction.  
- **Customizable Image Grid**: Processes images in smaller pieces to enhance data extraction accuracy.  
- **Integration with Azure OpenAI**: Leverages powerful AI capabilities for image analysis and data extraction.  
- **Structured Output**: Provides results in a consistent JSON format for easy integration with other systems.  
   
---  
   
## Table of Contents  
   
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Environment Setup](#environment-setup)  
- [Usage](#usage)  
- [Configuration](#configuration)  
- [Input and Output](#input-and-output)  
- [Example](#example)  
- [Error Handling](#error-handling)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgments](#acknowledgments)  
- [Contact](#contact)  
- [Disclaimer](#disclaimer)  
   
---  
   
## Prerequisites  
   
- **Python 3.8 or higher**  
- **Azure OpenAI Account**: An account with access to Azure OpenAI services.  
- **API Credentials**: Azure OpenAI endpoint, API key, and deployment name.  
   
---  
   
## Installation  
   
1. **Clone the Repository**  
  
   ```bash  
   git clone https://github.com/your-username/pdf-line-number-extractor.git  
   cd pdf-line-number-extractor  
   ```  
   
2. **Install Required Packages**  
  
   ```bash  
   pip install -r requirements.txt  
   ```  
  
   **Note**: Ensure the `requirements.txt` file contains the following packages:  
  
   ```  
   azure-openai  
   pydantic  
   python-dotenv  
   PyMuPDF  
   Pillow  
   ```  
   
---  
   
## Environment Setup  
   
1. **Set Up Environment Variables**  
  
   Create a `.env` file in the root directory with your Azure OpenAI credentials:  
  
   ```dotenv  
   AOAI_ENDPOINT=your_azure_openai_endpoint  
   AOAI_API_KEY=your_azure_openai_api_key  
   AOAI_DEPLOYMENT=your_azure_openai_deployment_name  
   ```  
  
   Replace the placeholders with your actual credentials.  
   
2. **Directory Structure**  
  
   Ensure the following directories exist:  
  
   - `input_documents`: Place your PDF files here.  
   - `output_results`: The script will save extracted data here.  
   - `output_images`: The script will save images here.  
   
---  
   
## Usage  
   
1. **Prepare Input PDFs**  
  
   Place all the PDF files you want to process inside the `input_documents` directory.  
   
2. **Run the Script**  
  
   ```bash  
   python analyze_diagram.py  
   ```  
 
   
3. **View Results**  
  
   - Extracted data in JSON format will be available in the `output_results` directory.  
   - Generated images will be saved in the `output_images` directory.  
   
---  
   
## Configuration  
   
- **Customizing the Prompt**  
  
  The prompt used for data extraction can be adjusted within the script:  
  
  ```python  
  prompt = """Extract all the line numbers strings that are above a diagram line that represents a pipe. Make sure the extracted line number string follows this format: stars with a letter followed by numbers and hyphens. For example: 'WW61010601-2"-A1A2-N', 'P61010501-8"-A1A1-IH', or 'P61010502-4"-A1A1-IH'. Only extract values that follow this format. Do not extract anything else."""  
  ```  
  
  Modify the prompt as needed to suit your specific use case.  
   
- **Adjusting Zoom Level**  
  
  The zoom factor for image quality is set in the script:  
  
  ```python  
  zoom = 4  # Zoom factor for image quality  
  ```  
  
  Increase or decrease the value to adjust image resolution.  
   
- **Changing Image Grid Size**  
  
  The script currently splits images into a 3x3 grid. To change this, adjust the grid calculations:  
  
  ```python  
  # Calculate the size of each piece  
  piece_width = width // columns  
  piece_height = height // rows  
  
  # Adjust 'rows' and 'columns' variables as needed  
  ```  
   
---  
   
## Input and Output  
   
- **Input**  
  
  - PDF files located in the `input_documents` directory.  
   
- **Output**  
  
  - **Extracted Data**: JSON files in the `output_results` directory, named in the format `{pdf_name}_page{number}_piece{number}.json`.  
  - **Images**: PNG files in the `output_images` directory, including full-page images and split pieces.  
   
---  
   
## Example  
   
1. **Processing a Sample PDF**  
  
   Let's say you have `diagram.pdf` in the `input_documents` directory.  
   
2. **Running the Script**  
  
   ```bash  
   python analyze_diagram.py  
   ```  
   
3. **Script Output**  
  
   - **Console Output**:  
  
     ```  
     Processing diagram.pdf...  
     Saved image to diagram_page1.png  
     Image size: 204800 bytes  
     Image dimensions: 2480x3508  
     Saved image piece to diagram_page1_piece1.png  
     Saved extracted information to diagram_page1_piece1.json  
     ...  
     ```  
  
   - **Extracted Data** (`diagram_page1_piece1.json`):  
  
     ```json  
     {  
       "extractedText": [  
         "P61010501-8\"-A1A1-IH",  
         "WW61010601-2\"-A1A2-N"  
       ]  
     }  
     ```  
  
   - **Images**:  
  
     - Full-page image: `diagram_page1.png`  
     - Image pieces: `diagram_page1_piece1.png`, `diagram_page1_piece2.png`, ...  
   
---  
   
## Error Handling  
   
- **File Errors**: If a PDF cannot be opened, an error message is displayed, and the script continues with the next file.  
  
  ```python  
  except Exception as e:  
      print(f"Error opening {pdf_file.name}: {e}")  
      continue  
  ```  
   
- **Page Processing Errors**: Issues during page processing are caught and displayed.  
  
  ```python  
  except Exception as e:  
      print(f"Error processing page {page_number+1} of {pdf_file.name}: {e}")  
  ```  
   
- **API Errors**: Ensure your Azure OpenAI credentials are correct. API-related errors will halt the script unless additional error handling is implemented.  
      
---  
   
## License  
   
This project is licensed under the [MIT License](LICENSE).  
