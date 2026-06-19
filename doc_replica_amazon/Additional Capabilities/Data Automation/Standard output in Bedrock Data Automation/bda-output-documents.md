

# Documents
<a name="bda-output-documents"></a>

Standard output for documents lets you set the granularity of response you're interested in as well as establishing output format and text format in the output. Below are some of the outputs you can enable.

**Note**  
BDA can process DOCX files. To process DOCX files, they are converted into PDFs. This means page number mapping will not work for DOCX files. Images of the converted PDFs will be uploaded to your output bucket if the if the JSON\+ option and page granularity are selected.

## Response Granularity
<a name="document-granularity"></a>

Response granularity determines what kind of response you want to receive from document text extraction. Each level of granularity gives you more and more separated responses, with page providing all of the text extracted together, and word providing each word as a separate response. The available granularity levels are:
+ Page level granularity – This is enabled by default. Page level granularity provides each page of the document in the text output format of your choice. If you're processing a PDF, enabling this level of granularity will detect and return embedded hyperlinks.
+ Element level granularity (Layout) – This is enabled by default. Provides the text of the document in the output format of your choice, separated into different elements. These elements, such as figures, tables, or paragraphs. These are returned in logical reading order based off the structure of the document. If you're processing a PDF, enabling this level of granularity will detect and return embedded hyperlinks.
+ Word level granularity – Provides information about individual words without using broader context analysis. Provides you with each word and its location on the page.

## Output Settings
<a name="document-output-settings"></a>

Output settings determine the way your downloaded results will be structured. This setting is exclusive to the console. The options for output settings are:
+ JSON – The default output structure for document analysis. Provides a JSON output file with the information from your configuration settings.
  + Async [InvokeDataAutomationAsync](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomationAsync.html) API: JSON output for Async API is S3 only.
  + Sync [InvokeDataAutomation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomation.html) API: JSON output can be set to S3 or inline by using `outputconfiguration`. If S3 is selected, then output JSON goes to S3 only (not inline). If S3 not provided, Sync API output supports JSON inline only.
+ JSON\+files – Only available for Async [InvokeDataAutomationAsync](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomationAsync.html) API. Using this setting generates both a JSON output and files that correspond with different outputs. For example, this setting gives you a text file for the overall text extraction, a markdown file for the text with structural markdown, and CSV files for each table that's found in the text. Figures located inside a document will be saved as well as figure crops and rectified images. These outputs are located in `standard_output/{{logical_doc_id}}/assets/` in your output folder.

**Note**  
The sync API does not output any additional files beyond the JSON. The output JSON contains only the text format that was selected as part of the Standard Output Text format. Sync API will not output Figure crops or rectified images.
DocX not supported by Sync API.

## Text Format
<a name="document-text-format"></a>

Text format determines the different kinds of texts that will be provided via various extraction operations. You can select any number of the following options for your text format.
+ Plaintext – This setting provides a text-only output with no formatting or other markdown elements noted.
+ Text with markdown – The default output setting for standard output. Provides text with markdown elements integrated.
+ Text with HTML – Provides text with HTML elements integrated in the response.
+ CSV – Provides a CSV structured output for tables within the document. This will only give a response for tables, and not other elements of the document.

## Bounding Boxes and Generative Fields
<a name="additional-response-document"></a>

For Documents, there are two response options that change their output based on the selected granularity. These are Bounding Boxes, and Generative Fields. Selecting Bounding Boxes will provide a visual outline of the element or word you choose in the console response dropdown. This lets you track down particular elements of your response more easily. Bounding Boxes are returned in your JSON as the coordinates of the four corners of the box.

When you select Generative Fields, you are generated a summary of the document, both a 10 word and 250 word version. Then, if you select elements as a response granularity, you generate a descriptive caption of each figure detected in the document. Figures include things like charts, graphs, and images.

------
#### [ Async ]

This section focuses on the different response objects you receive from running the API operation InvokeDataAutomationAsync on a document file. Below we'll break down each section of the response object and then see a full, populated response for an example document. The first section we'll receive is `metadata`.

```
"metadata":{
   "logical_subdocument_id":"XXXX-XXXX-XXXX-XXXX",
   "semantic_modality":"DOCUMENT",
   "s3_bucket":"bucket",
   "s3_prefix":"prefix"
},
```

The first section above provides an overview of the metadata associated with the document. Along with the S3 information, this section also informs you which modality was selected for your response.

```
"document":{
   "representation":{
      "text":"document text",
      "html":"document title document content",
      "markdown":"# text"
   },
   "description":"document text",
   "summary":"summary text",
   "statistics":{
      "element_count":5,
      "table_count":1,
      "figure_count":1,
      "word_count":1000,
      "line_count":32
   }
},
```

The above section provides document level granularity information. The description and summary sections are the generated fields based on the document The representation section provides the actual content of the document with various formatting styles. Finally statistics contains information on the actual content of the document, such as how many semantic elements there are, how many figures, words, lines, etc.

When you process a PDF, the statistics section of the response will also contain `hyperlinks_count` which tells you how many hyperlinks exist in your document.

```
{
   "id":"entity_id",
   "type":"TEXT",
   "representation":{
      "text":"document text",
      "html":"document title document content",
      "markdown":"# text"
   },
   "reading_order":2,
   "page_indices":[
      0
   ],
   "locations":[
      {
         "page_index":0,
         "bounding_box":{
            "left":0.0,
            "top":0.0,
            "width":0.05,
            "height":0.5
         }
      }
   ],
   "sub_type":"TITLE/SECTION_TITLE/HEADER/FOOTER/PARAGRAPH/LIST/PAGE_NUMBER"
},
```

This is the entity used for text within a document, indicated by the `TYPE` line in the response. Again representation shows the text in different formats. `reading_order` shows when a reader would logically see the text. This is a semantic ordering based on associated keys and values. For example, it associates titles of paragraphs with their respective paragraph in reading order. `page_indices` tells you which pages the text is on. Next is location information, with a provided text bounding box if it was enabled in response. Finally, we have the entity subtype. This subtype provides more detailed information on what kind of text is being detected. For a complete list of subtypes see the API Reference.

```
{
   "id":"entity_id",
   "type":"TABLE",
   "representation":{
      "html":"table.../table",
      "markdown":"| header | ...",
      "text":"header \t header",
      "csv":"header, header, header\n..."
   },
   "csv_s3_uri":"s3://",
   "headers":[
      "date",
      "amount",
      "description",
      "total"
   ],
   "reading_order":3,
   "title":"Title of the table",
   "footers":[
      "the footers of the table"
   ],
   "crop_images":[
      "s3://bucket/prefix.png",
      "s3://bucket/prefix.png"
   ],
   "page_indices":[
      0,
      1
   ],
   "locations":[
      {
         "page_index":0,
         "bounding_box":{
            "left":0,
            "top":0,
            "width":1,
            "height":1
         }
      },
      {
         "page_index":1,
         "bounding_box":{
            "left":0,
            "top":0,
            "width":1,
            "height":1
         }
      }
   ],
   "sub_type":"TITLE/SECTION_TITLE/HEADER/FOOTER/PARAGRAPH/LIST/PAGE_NUMBER"
},
```

This is the information for a table entity. For an InvokeDataAutomationAsync (async) request, in addition to location information, the different formats of the text, tables, and reading order, BDA also returns csv information and cropped images of the table in S3 buckets. The CSV information shows the different headers, footers, and titles. The images will be routed to the S3 bucket of the prefix set in the InvokeDataAutomationAsync request. For an InvokeDataAutomation (sync) request, csv and cropped images of the table in S3 buckets are not supported.

```
{

   "id":"entity_id",

   "type":"FIGURE",

   "summary":"",

   "representation":{

      "text":"document text",

      "html":"document title document content",

      "markdown":"# text"

   },

   "crop_images":[

      "s3://bucket/prefix.png",

      "s3://bucket/prefix.png"

   ],

   "locations":[

      {

         "page_index":0,

         "bounding_box":{

            "left":0,

            "top":0,

            "width":1,

            "height":1

         }

      }

   ],

   "sub_type":"CHART",

   "title":"figure title",

   "rai_flag":"APPROVED/REDACTED/REJECTED",

   "reading_order":1,

   "page_indices":[

      0

   ]

}
,
```

This is the entity used for figures such as in document graphs and charts. Similar to tables, these figures will be cropped and images sent to the s3 bucket set in your prefix. Additionally, you'll receive a `sub_type` and a figure title response for the title text and an indication on what kind of figure it is.

```
"pages":[
   {
      "id":"page_id",
      "page_index":0,
      "detected_page_number":1,
      "representation":{
         "text":"document text",
         "html":"document title document content",
         "markdown":"# text"
      },
      "statistics":{
         "element_count":5,
         "table_count":1,
         "figure_count":1,
         "word_count":1000,
         "line_count":32
      },
      "asset_metadata":{
         "rectified_image":"s3://bucket/prefix.png",
         "rectified_image_width_pixels":1700,
         "rectified_image_height_pixels":2200
      }
   }
],
```

The last of the entities we extract through standard output is Pages. Pages are the same as Text entities, but additionally contain page numbers, for which detected page number is on the page.

```
"text_lines":[
   {
      "id":"line_id",
      "text":"line text",
      "reading_order":1,
      "page_index":0,
      "locations":{
         "page_index":0,
         "bounding_box":{
            "left":0,
            "top":0,
            "width":1,
            "height":1
         }
      }
   }
],
```

```
"text_words":[
   {
      "id":"word_id",
      "text":"word text",
      "line_id":"line_id",
      "reading_order":1,
      "page_index":0,
      "locations":{
         "page_index":0,
         "bounding_box":{
            "left":0,
            "top":0,
            "width":1,
            "height":1
         }
      }
   }
]
```

These final two elements are for individual text portions. Word level granularity returns a response for each word, while default output reports only lines of text.

------
#### [ Sync ]

This section focuses on the different response objects you receive from running the API operation InvokeDataAutomation on a document file. Below we'll break down each section of the response object and then see a full, populated response for an example document. The first section we'll receive is `metadata`.

```
            "metadata": {
                "logical_subdocument_id": "1",
                "semantic_modality": "DOCUMENT",
                "number_of_pages": X,
                "start_page_index": "1",
                "end_page_index": X,
                "file_type": "PDF"
            },
```

The first section above provides an overview of the metadata associated with the document. Since the Synchronous InvokeDataAutomation API does not currently support document splitting, logical\_subdocument\_id is always equal to 1.

```
"document":{
   "representation":{
      "text":"document text",
      "html":"document title document content",
      "markdown":"# text"
   },
   "description":"document text",
   "summary":"summary text",
   "statistics":{
      "element_count":5,
      "table_count":1,
      "figure_count":1,
      "word_count":1000,
      "line_count":32
   }
},
```

The above section provides document level granularity information. The description and summary sections are the generated fields based on the document The representation section provides the actual content of the document with various formatting styles. Finally statistics contains information on the actual content of the document, such as how many semantic elements there are, how many figures, words, lines, etc.

Note: Unlike the asynchronous InvokeDataAutomationAsync request, the synchronous InvokeDataAutomation request does not support returning csv information and cropped image of the table in S3 buckets. 

```
{
"id":"entity_id",
   "type":"TEXT",
   "representation":{
"text":"document text",
      "html":"document title document content",
      "markdown":"# text"
   },
   "reading_order":2,
   "page_indices":[
      0
   ],
   "locations":[
      {
"page_index":0,
         "bounding_box":{
"left":0.0,
            "top":0.0,
            "width":0.05,
            "height":0.5
         }
      }
   ],
   "sub_type":"TITLE/SECTION_TITLE/HEADER/FOOTER/PARAGRAPH/LIST/PAGE_NUMBER"
},
```

 This is the entity used for text within a document, indicated by the TYPE line in the response. Again representation shows the text in different formats. reading\_order shows when a reader would logically see the text. This is a semantic ordering based on associated keys and values. For example, it associates titles of paragraphs with their respective paragraph in reading order. page\_indices tells you which pages the text is on. Next is location information, with a provided text bounding box if it was enabled in response. Finally, we have the entity subtype. This subtype provides more detailed information on what kind of text is being detected. For a complete list of subtypes see the API Reference. 

```
{
    "id": "entity_id",
    "type": "TABLE",
    "representation": {
        "html": "table.../table",
        "markdown": "| header | ...",
        "text": "header \t header",
        "csv": "header, header, header\n..."
    },
    "headers": ["date", "amount", "description", "total"],
    "reading_order": 3,
    "title": "Title of the table",
    "footers": ["the footers of the table"],
    "page_indices": [0, 1],
    "locations": [{
        "page_index": 0,
        "bounding_box": {
            "left": 0,
            "top": 0,
            "width": 1,
            "height": 1
        }
    }, {
        "page_index": 1,
        "bounding_box": {
            "left": 0,
            "top": 0,
            "width": 1,
            "height": 1
        }
    }]
},
```

This is the information for a table entity. The CSV information shows the different headers, footers, and titles. 

```
{

    "id": "entity_id",
    "type": "FIGURE",
    "summary": "",
    "representation": {
        "text": "document text",
        "html": "document title document content",
        "markdown": "# text"
    },

    "locations": [

        {
            "page_index": 0,
            "bounding_box": {
                "left": 0,
                "top": 0,
                "width": 1,
                "height": 1
            }
        }
    ],

    "sub_type": "CHART",
    "title": "figure title",
    "reading_order": 1,
    "page_indices": [
        0
    ]
},
​
```

This is the entity used for figures such as in document graphs and charts. You'll receive a `sub_type` and a figure title response for the title text and an indication on what kind of figure it is.

```
"pages":[
   "pages":[
   {
"id":"page_id",
      "page_index":0,
      "detected_page_number":1,
      "representation":{
"text":"document text",
         "html":"document title document content",
         "markdown":"# text"
      },
      "statistics":{
"element_count":5,
         "table_count":1,
         "figure_count":1,
         "word_count":1000,
         "line_count":32
      },
      "asset_metadata":{
"rectified_image":"s3://bucket/prefix.png",
         "rectified_image_width_pixels":1700,
         "rectified_image_height_pixels":2200
      }
   }
],
```

The last of the entities we extract through standard output is Pages. Pages are the same as Text entities, but additionally contain page numbers, for which detected page number is on the page.

```
"text_lines":[
   {
      "id":"line_id",
      "text":"line text",
      "reading_order":1,
      "page_index":0,
      "locations":{
         "page_index":0,
         "bounding_box":{
            "left":0,
            "top":0,
            "width":1,
            "height":1
         }
      }
   }
],
```

```
"text_words":[
   {
      "id":"word_id",
      "text":"word text",
      "line_id":"line_id",
      "reading_order":1,
      "page_index":0,
      "locations":{
         "page_index":0,
         "bounding_box":{
            "left":0,
            "top":0,
            "width":1,
            "height":1
         }
      }
   }
]
```

These final two elements are for individual text portions. Word level granularity returns a response for each word, while default output reports only lines of text.

------

## Additional file format metadata JSON
<a name="output-json-plus"></a>

When you receive your additional files from the additional file formats flag, you will get a JSON file for any rectified images that are extracted. BDA rectifies rotated images by using a homography to rotate the image to be at a 90 degree angle. An example of the JSON is below:

```
        "asset_metadata": {
            "rectified_image": "s3://bucket/prefix.png",
            "rectified_image_width_pixels": 1700,
            "rectified_image_height_pixels": 2200,
            "corners": [
                [
                    0.006980135689736235,
                    -0.061692718505859376
                ],
                [
                    1.10847711439684,
                    0.00673927116394043
                ],
                [
                    0.994479346419327,
                    1.050548828125
                ],
                [
                    -0.11249661383904497,
                    0.9942819010416667
                ]
            ]
        }
```

Corners represent the detected corners of an image, used to form a homography of the document. This homography is used to rotate the image while maintaining its other properties.