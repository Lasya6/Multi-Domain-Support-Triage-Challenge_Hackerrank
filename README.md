My Solution
# Support Ticket Classification & Response System

## Overview

This project processes customer support tickets and automatically generates structured outputs including request type classification, product area, status, justification, and a relevant response based on documentation.

The goal is to simulate an intelligent support system that can understand user issues and map them to appropriate categories while providing helpful responses from existing knowledge base.

--------------------------------------------------------------------------------

## How It Works

### 1. Data Loading

* Support tickets are loaded from 'support_tickets/support_tickets.csv'
* Documentation is loaded from the 'data/' directory (supports '.txt' and '.md' files)

### 2. Request Classification

Each ticket is analyzed and classified into:

*Request Type*

  * 'bug' -system issues (eg.:error, not working)
  * 'invalid' -greetings or non-actionable queries
  * 'product_issue' -general support requests

*Product Area*

  * 'screen' -tests, interviews, submissions
  * 'community - login, account, signup issues
  * 'conversation_management' -chat-related issues
  * 'privacy' - data/privacy concerns
  * 'travel_support' / 'general_support' - card/visa-related issues

*Status*

  * 'Escalated' - for bugs
  * 'Replied' - for others

### 3. Justification Generation

* A short explanation is generated explaining:
Why the request was classified as bug / invalid / product_issue based on detected keywords

### 4. Response Generation

Responses are generated using documentation:

Filters documents based on company relevance.
Extracts meaningful sentences
Uses keyword matching + scoring to find best match
Avoids:

  * Short or irrelevant lines
  * URLs or metadata
  * Questions

If no good match is found: 
* Please refer to official documentation.

### 5. Output

Final output is saved as: support_tickets/output.csv

Includes:

* Issue
* Subject
* Company
* Response
* Product Area
* Status
* Request Type
* Justification
------------------------------------------------------------------------------------
## How to Run

1. Install dependencies:
pip install pandas

2. Run the script:
python main.py

3. Output will be generated in:
support_tickets/output.csv

## Key Features

* Rule-based classification (simple & explainable)
* Documentation-driven response generation
* Company-specific filtering for better accuracy
* Noise filtering for cleaner responses
* Lightweight and fast (no heavy ML required)


## Possible Improvements

* Use NLP embeddings, like cosine similarity for better matching
* Add typo handling and fuzzy matching
* Improve keyword extraction
* Use LLMs for response generation

## Conclusion

This system demonstrates a practical approach to automating support ticket handling using rule-based logic and documentation matching. It is simple, scalable, and easy to extend with more advanced techniques.

