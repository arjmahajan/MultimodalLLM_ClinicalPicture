# Lancet Clinical Picture Quiz Multimodal LLM Analysis

This project contains code to analyze clinical vignettes using multiple Large Language Models (LLMs), comparing performance between text-only and text+image inputs. The project is designed to process Lancet Clinical Picture Quiz cases, evaluating LLMs' diagnostic reasoning capabilities.

## Models Used
- **GPT-4 Turbo** (gpt-4-turbo-2024-04-09)
- **LLaVA** (LlaVA-v1.6-34b)
- **Claude 3 Opus** (claude-3-opus-20240229)
  - All cases were input using Claude's browser-based graphical user interface (GUI) in the format detailed in the supplement, as the Claude 3 application programming interface (API) did not support image upload functionality at the time of data collection.

## Project Structure
```
project_folder/
├── README.md
├── clinical_vignettes.txt       # Template format only, actual quiz content not included
├── vignette_images/            # Template folder structure only, images not included
│   ├── 1_1.png                # Case 1, image 1
│   ├── 1_2.png                # Case 1, image 2
│   ├── 2_1.png                # Case 2, image 1
│   └── ...
├── text_processor.py          # Script for text-only analysis
└── multimodal_processor.py    # Script for text+image analysis
```

## Content Notice
- The `clinical_vignettes.txt` file provided contains only the template and exact format required for the prompts. **Actual Lancet Clinical Picture Quiz content is not included** to ensure compliance with copyright and usage guidelines.
- The `vignette_images` folder structure is provided as a template. Actual Lancet Clinical Picture Quiz images are not included to ensure compliance with copyright and usage guidelines.
- Users must obtain appropriate permissions and licenses to use Lancet Clinical Picture Quiz content.

## File Format Requirements

### clinical_vignettes.txt Format
Each case must follow this exact format:
```
Case: [number] [case text]
Answer Options:
[option 1]
[option 2]
[option 3]
[option 4]

```
Key formatting rules:
- Each case starts with "Case: " followed by the case number
- Case text on the same line as "Case: "
- "Answer Options:" on a new line
- Each option on its own line
- One blank line between cases
- No additional formatting or numbering
- UTF-8 encoding required

### Image Files
- Images must be PNG format
- Naming convention: `[case_number]_[image_number].png`
- Example: Case 1 with 2 images would have:
  - `1_1.png`
  - `1_2.png`

##Randomization
A randomized list of integers [1, 160] without replacement was generated to determine the order of case reports to input. In our original iteration, the order was:
[98, 73, 105, 144, 3, 29, 41, 86, 97, 83, 60, 69, 66, 17, 138, 124, 20, 34, 50, 18, 7, 65, 23, 145, 102, 107, 56, 154, 93, 91, 37, 53, 8, 54, 72, 114, 133, 28, 128, 24, 149, 68, 48, 67, 99, 44, 150, 49, 75, 10, 140, 21, 70, 64, 79, 25, 63, 109, 90, 57, 151, 42, 85, 113, 5, 110, 116, 157, 22, 135, 43, 15, 89, 74, 147, 101, 1, 47, 146, 31, 131, 96, 103, 40, 112, 122, 100, 136, 80, 92, 156, 26, 152, 55, 52, 118, 84, 87, 45, 108, 2, 9, 33, 16, 119, 159, 127, 51, 139, 32, 78, 11, 61, 158, 59, 77, 104, 117, 160, 121, 148, 4, 62, 115, 71, 95, 36, 111, 153, 14, 58, 130, 30, 141, 94, 126, 46, 88, 76, 125, 19, 134, 81, 35, 129, 132, 142, 137, 155, 12, 106, 123, 38, 6, 13, 143, 120, 27, 82, 39]

##Adjustable Feature Settings Used
llava-v1.6-34b and GPT-4T:
- temperature: 0.0, max_tokens: 1024, top_p: 0.9, top_k: 1
 
## Disclaimer
This project is intended for research purposes only. Users must ensure they have appropriate permissions and licenses for any clinical content used with this code. The provided code and templates do not include any proprietary content from the Lancet Clinical Picture Quiz.