

# Images
<a name="bda-ouput-image"></a>

The Amazon Bedrock Data Automation (BDA) feature offers a comprehensive set of standard outputs for image processing to generate insights from your images. You can use these insights to enable a wide range of applications and use cases, such as content discovery, contextual ad placement, and brand safety. Here's an overview of each operation type available as part of standard outputs for images:

## Image Summary
<a name="image-summarization"></a>

Image summary generates a descriptive caption for an image. This feature is enabled within the standard output configuration by default.

## IAB Taxonomy
<a name="iab-classification"></a>

The Interactive Advertising Bureau (IAB) classification applies a standard advertising taxonomy to classify image content. For Preview, BDA will support 24 top-level (L1) categories and 85 second-level (L2) categories. To download the list of IAB categories supported by BDA, click [here](samples/iab-taxonomy.zip).

## Logo Detection
<a name="image-logo-detection"></a>

This feature identifies logos in an image and provides bounding box information, indicating the coordinates of each detected logos within the image, and confidence scores. This feature is not enabled by default.

## Image Text Detection
<a name="image-text-detection"></a>

This feature detects and extracts text that appears visually in an image and provides bounding box information, indicating the coordinates of each detected text element within the image, and confidence scores. This feature is enabled within the standard output configuration by default.

## Content Moderation
<a name="content-moderation"></a>

Content moderation detects inappropriate, unwanted, or offensive content in an image. For Preview, BDA will support 7 moderation categories: Explicit, Non-Explicit Nudity of Intimate parts and Kissing, Swimwear or Underwear, Violence, Drugs & Tobacco, Alcohol, Hate symbols. Explicit text in images is not flagged.

 Bounding boxes and the associated confidence scores can be enabled or disabled for relevant features like text detection to provide location coordinates in the image. By default, image summary and image text detection are enabled. 

## Image Standard Output
<a name="image-standard-output-example"></a>

The following is an example of a standard output for an image processed through BDA. Each section has been shortened and separated with an explanation.

```
{
"metadata": {
    "id": "image_123",
    "semantic_modality": "IMAGE",
    "s3_bucket": "my-s3-bucket",
    "s3_prefix": "images/",
    "image_width_pixels": 1920,
    "image_height_pixels": 1080,
    "color_depth": 24,
    "image_encoding": "JPEG"
},
```

The first part of a response is the metadate of an image. It gives you the file name, encoding type, s3 bucket location and further information about the content.

```
"image": {
    "summary": "Lively party scene with decorations and supplies",
```

At the beginning of the response is the generative summary of the image.

```
    "iab_categories": [
        {
            "id": "iab_12345",
            "type": "IAB",
            "category": "Party Supplies",
            "confidence": 0.9,
            "parent_name": "Events & Attractions",
            "taxonomy_level": 2
        },
        {
            "id": "iab_67890",
            "type": "IAB",
            "category": "Decorations",
            "confidence": 0.8,
            "parent_name": "Events & Attractions",
            "taxonomy_level": 1
        }
    ],
```

Next, we see the IAB catagories attached to a response. These represent different types of advertising classifications, using the standard IAB taxonomy. Each one has a confidence score, taxonomy\_level, and parent\_name for the general high level catagory.

```
    "content_moderation": [
        {
            "id": "mod_12345",
            "type": "MODERATION",
            "category": "Drugs & Tobacco Paraphernalia & Use",
            "confidence": 0.7,
            "parent_name": "Drugs & Tobacco",
            "taxonomy_level": 2
        }
    ], 
    ...
```

Content moderation contains information about possible explicit content in an image. These each have a confidence score and category, aligning with the content moderation categories discussed earlier in the section.

```
    "text_words": [
        {
            "id": "word_1",
            "text": "lively",
            "confidence": 0.9,
            "line_id": "line_1",
            "locations": [
                {
                    "bounding_box": {
                        "left": 100,
                        "top": 200,
                        "width": 50,
                        "height": 20
                    },
                    "polygon": [
                        {"x": 100, "y": 200},
                        {"x": 150, "y": 200},
                        {"x": 150, "y": 220},
                        {"x": 100, "y": 220}
                    ]
                }
            ]
        },
        ...
```

This section breaks down each detected word within an image, including confidence and an on screen location within the image. It also flags which line the word is in, using `line_id`.

```
    "text_lines": [
        {
            "id": "line_1",
            "text": "lively party",
            "confidence": 0.9,
            "locations": [
                {
                    "bounding_box": {
                        "left": 100,
                        "top": 200,
                        "width": 200,
                        "height": 20
                    },
                    "polygon": [
                        {"x": 100, "y": 200},
                        {"x": 300, "y": 200},
                        {"x": 300, "y": 220},
                        {"x": 100, "y": 220}
                    ]
                }
            ]
        }
    ]
},
```

Here, words are detected in their collective lines, with confidence score and bounding box. 

```
"statistics": {
    "entity_count": 7,
    "object_count": 3,
    "line_count": 2,
    "word_count": 9
}
}
```

Finally, we have statistics. These break down all content within an image, including object