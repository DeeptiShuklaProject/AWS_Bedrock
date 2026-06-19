

# Prerequisites for using Bedrock Data Automation
<a name="bda-limits"></a>

Files for BDA need to meet certain requirements to be processed. The following tables show what those requirements are for different file types.

------
#### [ Async ]

**Async document file requirements**

The following tables show the requirements for files processed using the Invoke Data Automation Async API.


**Document file requirements**  

|  Requirement Description  |  Requirement Details  | 
| --- | --- | 
| (Console) Maximum number of pages per document file | 20 | 
| Maximum Number of pages per document while splitter is enabled | 3000 | 
| (Console) Maximum file size (MB) | 200 | 
| Maximum file size (MB) | 500 | 
| Supported File Formats | PDF, TIFF, JPEG, PNG, DOCX | 
| PDF Specific Limits | The maximum height and width is 40 inches and 9000 points. PDFs cannot be password protected. PDFs can contain JPEG 2000 formatted images. | 
| Document Rotation and Image Size | BDA supports all in-plane document rotations, for example 45-degree in-plane rotation.<br />BDA supports images with a resolution less than or equal to 10000 pixels on all sides. | 
| Text Alignment |  Text can be text aligned horizontally within the document. Horizontally arrayed text can be read regardless of the degree of rotation of a document. BDA does not support vertical text (text written vertically, as is common in languages like Japanese and Chinese) alignment within the document. | 
| Character Size | The minimum height for text to be detected is 15 pixels. At 150 DPI, this would be the same as 8 point font. | 
| Character Type | BDA supports both handwritten and printed character recognition.  | 
| Supported Input Languages | English, German, Spanish, French, Italian, Portuguese. | 

**Note**  
To process DOCX files, they are converted into PDFs. This means page number mapping will not work for DOCX files. Images of the converted PDFs will be uploaded to your output bucket if the JSON\+ option and page granularity are selected.

**Note**  
For BDA Custom Output for documents, you can author blueprint prompts and instructions in any of the supported languages. For BDA Standard Output, document summaries and figure captions are returned in the detected language of the document.

Blueprint instruction optimization supports all the limits above for documents with the following differences:
+ A total of 10 document asset examples
+ 20 pages per document asset example on console and API
+ 200MB for the total document asset example
+ Only PDF, DOCX, and TIFF document file formats

------
#### [ Sync ]

**Sync document file requirements**

The following tables show the requirements for files processed using the Invoke Data Automation API.


**Document file requirements**  

|  Requirement Description  |  Requirement Details  | 
| --- | --- | 
| (Console) Maximum number of pages per document file | 10 | 
| Maximum number of pages per document file (splitter is not available) | 10 | 
| (Console) Maximum file size (MB) | 50 | 
| Maximum file size (MB) | 50 | 
| Supported File Formats | PDF, TIFF, JPEG, PNG | 
| PDF Specific Limits | The maximum height and width is 40 inches and 9000 points. PDFs cannot be password protected. PDFs can contain JPEG 2000 formatted images. | 
| Document Rotation and Image Size | BDA supports all in-plane document rotations, for example 45-degree in-plane rotation.<br />BDA supports images with a resolution less than or equal to 10000 pixels on all sides. | 
| Text Alignment |  Text can be text aligned horizontally within the document. Horizontally arrayed text can be read regardless of the degree of rotation of a document. BDA does not support vertical text (text written vertically, as is common in languages like Japanese and Chinese) alignment within the document. | 
| Character Size | The minimum height for text to be detected is 15 pixels. At 150 DPI, this would be the same as 8 point font. | 
| Character Type | BDA supports both handwritten and printed character recognition.  | 
| Supported Input Languages | English, German, Spanish, French, Italian, Portuguese. | 

**Note**  
Figure captioning works on 20 images per 10 page docuement (sync) and 20 images per page (async).

**Tip**  
Tips to speed up sync API processing:  
Disable Generative fields unless absolutely required.
Select only the granularity and Output text format that you need (vs selecting multiple).
Simplify your Blueprint to reduce the number of fields extracted as much as possible.
Reduce the number of table and list fields in your blueprint where possible.

------


**Blueprint requirements**  

|  Requirement Description  |  Requirement Details  | 
| --- | --- | 
| Maximum number of blueprints per project | 40 | 
| Maximum number of projects per account | 100 | 
| Maximum number of blueprints per account | 1000 | 
| Maximum number of blueprint versions | 100 | 
| Maximum number of blueprint leaf fields | 100 | 
| Maximum number of blueprint list leaf fields | 30 | 
| Maximum blueprint name length | 60 characters | 
| Maximum blueprint field description length | 600 characters (document), 500 characters (image/video/audio) | 
| Maximum blueprint field name length | 60 characters | 
| Maximum blueprint size | 100,000 characters (JSON formatted) | 


**Image file requirements**  

|  Requirement Description  |  Requirement Details  | 
| --- | --- | 
| Maximum File Size (MB) | 5 | 
| Maximum Resolution | 8k | 
| Supported File Formats | JPEG, PNG | 


**Video file requirements**  

|  Requirement Description  |  Requirement Details  | 
| --- | --- | 
| Maximum File Size (MB) | 10240 | 
| Maximum Video Length (Minutes) | 240 | 
| Supported File Formats | MP4, MOV, AVI, MKV, or WEBM container formats with H.264, H.265/HEVC, VP8, VP9, AV1, MPEG-4 Visual, or Apple ProRes video codecs | 
| Maximum Video Blueprints per Project | 1 | 
| Maximum Video Blueprints per Start Inference request | 1 | 
| Minimum resolution | 224 | 
| Maximum resolution | 7680 | 
| Minimum framerate (Frames per second) | 1 | 
| Maximum framerate (Frames per second) | 60 | 


**Audio file requirements**  

|  Requirement Description  |  Requirement Details  | 
| --- | --- | 
| Supported Input Languages | English, German, Spanish, French, Italian, Portuguese, Japanese, Korean, Chinese, Taiwanese and Cantonese.<br />*\*All locales supported of the above languages.* | 
| Supported Output Languages | English, or the dominant language of the audio. | 
| Minimum Audio Sample Rate (Hz) | 8000 | 
| Maximum Audio Sample Rate (Hz) | 48000 | 
| Maximum File Size (MB) | 2048 | 
| Maximum Audio Length (Minutes) | 240 | 
| Minimum Audio Length (Milliseconds) | 500 | 
| Supported File Formats | AMR, FLAC, M4A, MP3, Ogg, WAV | 
| Maximum Audio Blueprints per Project | 1 | 
| Maximum Audio Blueprints per Start Inference request | 1 | 
| Maximum Audio Channels for Audio files | 2 | 


**Data automation library requirements**  

|  Resource  |  Limit  | 
| --- | --- | 
| Maximum number of data automation libraries per account | 10 | 
| Supported Languages for Custom Vocabulary | English, Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese (Simplified), Chinese (Traditional), and Cantonese.<br />Only the characters listed in your language's [Character Sets](bda-library-character-sets.md) can be used in a custom vocabulary. | 
| Maximum number of custom vocabulary phrases that can be configured per library (all languages) | 500 | 
| Maximum total number of characters across all vocabulary phrases per library | 30000 | 
| Maximum number of concurrent vocabulary ingestion jobs that can run per library | 1 | 