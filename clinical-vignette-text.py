from openai import OpenAI
import os
import json
from datetime import datetime
import pandas as pd

class TextProcessor:
    def __init__(self, api_key: str, input_file: str):
        self.client = OpenAI(api_key=api_key)
        self.input_file = input_file
        
    def get_case(self, case_number: int) -> dict:
        """
        Extract case by number
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

    def process_case(self, case_number: int) -> dict:
        case = self.get_case(case_number)
        if not case:
            return {"error": f"Case {case_number} not found"}

        prompt = f"Answer this multiple choice challenge that contains a case using one of the answers provided.\n\nCase: {case['text']}\n\nAnswer Options: {case['options']}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-2024-04-09",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            result = {
                'case_number': case_number,
                'case_text': case['text'],
                'options': case['options'],
                'model_response': response.choices[0].message.content,
                'finish_reason': response.choices[0].finish_reason,
                'model': response.model,
                'timestamp': datetime.now().isoformat()
            }

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_base = f'gpt4_text_case{case_number}_{timestamp}'
            
            # Save as CSV
            pd.DataFrame([result]).to_csv(f'{filename_base}.csv', index=False)
            
            # Save as JSON
            with open(f'{filename_base}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)

            return result

        except Exception as e:
            return {"error": str(e)}

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    processor = GPT4TextProcessor(api_key, "clinical_vignettes.txt")
    
    case_number = int(input("Enter case number (1-160): ")) #randomized prior to input
    
    # Process  case
    result = processor.process_case(case_number)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nProcessed Case {case_number}")
        print(f"\nModel Response:\n{result['model_response']}")

if __name__ == "__main__":
    main()
