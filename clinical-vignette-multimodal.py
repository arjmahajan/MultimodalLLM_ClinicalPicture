from openai import OpenAI
import os
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import base64

class MultimodalProcessor:
    def __init__(self, api_key: str, input_file: str, image_folder: str):
        self.client = OpenAI(api_key=api_key)
        self.input_file = input_file
        self.image_folder = Path(image_folder)
        
    def get_case(self, case_number: int) -> dict:
        """
        Extract case
        """
        with open(self.input_file, 'r', encoding='utf-8') as f:
            cases = f.read().split('\n\n')
            
        for case in cases:
            if case.startswith(f"Case: {case_number} "):
                case_parts = case.split('Answer Options:')
                if len(case_parts) == 2:
                    return {
                        'text': case_parts[0].replace('Case:', '').strip(),
                        'options': case_parts[1].strip()
                    }
        return None

    def get_case_images(self, case_number: int) -> list:
        """
        Get case's corresponding images
        """
        images = []
        for img_path in sorted(self.image_folder.glob(f"{case_number}_*.png")):
            with open(img_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                images.append(base64_image)
        return images

    def process_case(self, case_number: int) -> dict:
        case = self.get_case(case_number)
        if not case:
            return {"error": f"Case {case_number} not found"}

        images = self.get_case_images(case_number)
        if not images:
            return {"error": f"No images found for case {case_number}"}

        # Create prompt
        content = [
            {
                "type": "text",
                "text": "Answer this multiple choice challenge that contains a case, and associated public domain image(s) using one of the answers provided and explain your answer."
            }
        ]

        content.append({
            "type": "text",
            "text": f"Case: {case['text']}\n\nAnswer Options: {case['options']}"
        })

        for img_base64 in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_base64}"
                }
            })

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-2024-04-09",
                messages=[{"role": "user", "content": content}],
                temperature=0.7
            )

            result = {
                'case_number': case_number,
                'case_text': case['text'],
                'options': case['options'],
                'num_images': len(images),
                'model_response': response.choices[0].message.content,
                'finish_reason': response.choices[0].finish_reason,
                'model': response.model,
                'timestamp': datetime.now().isoformat()
            }

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_base = f'gpt4_multimodal_case{case_number}_{timestamp}'
            
            pd.DataFrame([result]).to_csv(f'{filename_base}.csv', index=False)
            
            # JSON backup
            with open(f'{filename_base}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)

            return result

        except Exception as e:
            return {"error": str(e)}

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    processor = GPT4MultimodalProcessor(
        api_key,
        "clinical_vignettes.txt",
        "vignette_images"
    )
    
    # Get case number from user
    case_number = int(input("Enter case number (1-160): "))
    
    result = processor.process_case(case_number)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nProcessed Case {case_number}")
        print(f"Number of images: {result['num_images']}")
        print(f"\nModel Response:\n{result['model_response']}")

if __name__ == "__main__":
    main()
