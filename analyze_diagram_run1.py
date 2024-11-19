import base64    
import os    
import json    
from dotenv import load_dotenv    
from openai import AzureOpenAI    
from pydantic import BaseModel    
from pathlib import Path    
import fitz  # PyMuPDF    
  
# Load environment variables    
load_dotenv()    
  
# Azure OpenAI environment variables    
aoai_endpoint = os.getenv("AOAI_ENDPOINT")    
aoai_api_key = os.getenv("AOAI_API_KEY")    
aoai_deployment_name = os.getenv("AOAI_DEPLOYMENT")    
  
# Initialize the Azure OpenAI client    
client = AzureOpenAI(    
    azure_endpoint=aoai_endpoint,    
    api_key=aoai_api_key,    
    api_version="2024-10-21"    
)    
  
def image_to_data_url(image_bytes, mime_type='image/png'):    
    """    
    Convert image bytes to a data URL.    
  
    Parameters:    
    -----------    
    image_bytes : bytes    
        The image data in bytes.    
    mime_type : str    
        The MIME type of the image.    
  
    Returns:    
    --------    
    str    
        A data URL representing the image.    
    """    
    base64_encoded_data = base64.b64encode(image_bytes).decode('utf-8')    
    return f"data:{mime_type};base64,{base64_encoded_data}"    
  
def call_azure_openai(prompt, image_data_url, client=client, aoai_deployment_name=aoai_deployment_name):    
    """    
    Call the Azure OpenAI service to analyze an image.    
  
    Parameters:    
    -----------    
    prompt : str    
        The prompt to send to the model.    
    image_data_url : str    
        The data URL of the image.       
    client : AzureOpenAI    
        The Azure OpenAI client instance.    
    aoai_deployment_name : str    
        The deployment name of the Azure OpenAI model.    
  
    Returns:    
    --------    
    dict    
        The parsed response from the Azure OpenAI model.    
    """    
  
    response = client.chat.completions.create(
        model=aoai_deployment_name,
        messages=[{
            "role": "system", 
            "content": "You are an AI helpful assistant that extracts information from documents."
        }, {
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt
            }, {
                "type": "image_url",
                "image_url": {
                    "url": image_data_url
                }
            }]
        }],
        max_tokens=12000,
        temperature=0.4)
    
    print("AOAI response: ", response)
    extracted_information = response['choices'][0]['message']['content']    
  
    return extracted_information    
  
def main():    
    # Define input and output directories    
    input_dir = Path('input_documents')    
    output_dir = Path('output_results_run1')    
    output_dir.mkdir(exist_ok=True)    
  
    # Define output images directory    
    output_images_dir = Path('output_images_run1')    
    output_images_dir.mkdir(exist_ok=True)   
  
    # Prompt to extract specific information    
    prompt = """Extract all the text from this image. Save it in an organized format."""    
      
    # Iterate over each PDF in the input directory    
    for pdf_file in input_dir.glob('*.pdf'):    
        if pdf_file.is_file():    
            print(f"Processing {pdf_file.name}...")    
  
            # Open the PDF file    
            try:    
                doc = fitz.open(pdf_file)    
            except Exception as e:    
                print(f"Error opening {pdf_file.name}: {e}")    
                continue    
  
            # Iterate over each page in the PDF    
            for page_number in range(len(doc)):    
                try:    
                    # Load the page    
                    page = doc.load_page(page_number)    
                    zoom = 3  # Zoom factor for image quality  
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))    
                    image_bytes = pix.tobytes()    
  
                    # Optional: save the image to output_images directory    
                    image_output_path = output_images_dir / f"{pdf_file.stem}_page{page_number+1}.png"    
                    pix.save(str(image_output_path))    
                    print(f"Saved image to {image_output_path.name}")    
  
                    # Print the image size and dimensions  
                    image_size = os.path.getsize(str(image_output_path))  
                    print(f"Image size: {image_size} bytes")  
                    print(f"Image dimensions: {pix.width}x{pix.height}")  
  
                    # Convert image to data URL    
                    image_data_url = image_to_data_url(image_bytes)    
  
                    # Call Azure OpenAI to extract structured information    
                    extracted_info = call_azure_openai(prompt, image_data_url) 

                    print(extracted_info)   
  
                #     # Define output file path    
                #     output_file = output_dir / f"{pdf_file.stem}_page{page_number+1}.json"    
  
                #     # Save the result as a JSON file    
                #     with open(output_file, 'w', encoding='utf-8') as json_file:    
                #         json.dump(extracted_info, json_file, ensure_ascii=False, indent=2)    
  
                #     print(f"Saved extracted information to {output_file.name}")    
  
                except Exception as e:    
                    print(f"Error processing page {page_number+1} of {pdf_file.name}: {e}")  
  
if __name__ == "__main__":    
    main()    