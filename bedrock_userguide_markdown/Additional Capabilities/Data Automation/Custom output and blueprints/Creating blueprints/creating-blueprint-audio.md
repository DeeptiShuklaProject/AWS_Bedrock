

# Creating blueprints for audio
<a name="creating-blueprint-audio"></a>

Similar to image blueprints, you can only have one audio blueprint per project.

Below are some example fields for audio processing.

## Blueprint field examples for audio files
<a name="example-audio-fields"></a>


|  |  |  |  | 
| --- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | 
| transcript\_summary | Generate a concise abstractive summary of the conversation, focusing on the main topics and key themes. Ensure accuracy by summarizing only what is explicitly discussed, without adding specific details not present in the conversation. Keeping the response within 100 words. | inferred | string | 
| topics | The main topics of the audio transcript, listed as single words. | inferred | [string] (Array of strings) | 
| category | The category of the audio (not the topic). Choose from General conversation, Media, Hospitality, Speeches, Meetings, Education, Financial, Public sector, Healthcare, Sales, Audiobooks, Podcasts, 911 calls, Other. | inferred | string | 
| spoken\_named\_entities | Any named entities (typically proper nouns) explicitly mentioned in the audio transcript including locations, brand names, company names, product names, services, events, organizations, etc. Do not include names of people, email addresses or common nouns.  | extractive | [string] (Array of strings) | 

## Blueprint field examples for conversational analytics
<a name="example-audio-analytics"></a>


|  |  |  |  | 
| --- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | 
| call\_summary | Summarize the caller-agent conversation in under 100 words. Start with the caller's request, then the agent's response and actions, ending with outcomes or follow-ups. Include key details like emails, links, or callbacks. For multiple issues, summarize each with its outcome and next steps. | inferred | string | 
| call\_categories | The category (or categories) of the call. Choose one or more from Billing, Tech support, Customer service, Account support, Sales, Complaints, Product issues, Service issues, General inquiries, Other. | inferred | [string] (Array of strings) | 
| spoken\_locations | Locations explicitly mentioned in the conversation, including cities, states, and countries. | extractive | [string] | 
| call\_opening | Did the agent greet the caller and introduce themselves at the beginning of the call?  | extractive | boolean | 