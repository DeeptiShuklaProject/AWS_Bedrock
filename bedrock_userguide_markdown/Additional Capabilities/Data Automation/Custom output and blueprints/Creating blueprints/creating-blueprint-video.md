

# Creating blueprints for video
<a name="creating-blueprint-video"></a>

Blueprints for video files have a few unique qualities compared to other blueprints, particularly in field creation. Video blueprints have a parameter called granularity, which lets you set a field to either Video, or Chapter. When the field is set to video, it will be detected across an entire video. For example, if you wanted a summary of the entire clip, you would want to set that field's granularity to video. 

A field with granularity set to Chapter will instead return a response for each chapter of the video. The field will return a value for each video chapter. Continuing from the previous example, if you wanted a summary of each portion of a video, you'd set the granularity to chapter.

When you create a chapter granularity field, you can set a unique data type, an array of entities. For example, if you want to detect the visually prominent objects in your video, you could create a field called `key-visual-objects`, and set the type it an array of entities. This field would then return the names of the entities in an array object.

Below are some example fields for video processing. All fields in video blueprints are considered inferred, except for entities and entity arrays.

## Blueprint field examples for media search
<a name="example-video-fields-search"></a>


|  |  |  |  |  | 
| --- |--- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | Granularity | 
| key-visual-objects | Please detect all the visually prominent objects in the video | extractive | Array of entities | [ "chapter" ] | 
| keywords | Searchable terms that capture key themes, cast, plot elements, and notable aspects of TV shows and movies to enhance content discovery. | inferred | Array of strings | ["video"] | 
| genre | The genre of the content. | inferred | string | ["video"] | 
| video-type | Identify the type of video content | inferred | enums: ["Movie", "TV series", "News", "Others"] | [ "video" ] | 

## Blueprint field examples for keynote highlights
<a name="example-video-fields-keynote"></a>


|  |  |  |  |  | 
| --- |--- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | Granularity | 
| broadcast-setting | The physical setting or environment where the broadcast or training session is taking place. | inferred | enums["conference hall", "classroom", "outdoor venue", "Others", "Not applicable to the video"] | [ "video" ] | 
| broadcast-audience-engagement | The level of engagement or interaction between the speakers and the audience. | inferred | enums["interactive", "passive", "Not applicable to the video"] | ["video"] | 
| broadcast-visual-aids | A list of notable visual aids or materials used during the presentation, such as slides, diagrams, or demonstrations. | inferred | Array of strings | ["video"] | 
| broadcast-audience-size | The size of the audience present at the event. | inferred | enums["large crowd", "medium crowd", "small group", "Not applicable to this video"] | [ "chapter" ] | 
| broadcast-presentation-topics | A list of key topics, subjects, or themes covered in the presentation or training session. | inferred | enums: ["Movie", "TV series", "News", "Others"] | [ "video" ] | 

## Blueprint field examples for advertisement analysis
<a name="example-video-fields-ad"></a>


|  |  |  |  |  | 
| --- |--- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | Granularity | 
| ads-video-ad-categories | The ad categories for the video | inferred | enums["Health and Beauty", "Weight Loss", "Food and Beverage", "Restaurants", "Political", "Cryptocurrencies and NFT", "Money Lending and Finance", "Tobacco", "Other", "Video is not an advertisement"] | [ "video" ] | 
| ads-video-language | The primary language of the advertisement | inferred | string | ["video"] | 
| ads-video-primary-brand | The main brand or company being advertised in the video. | inferred | string | ["video"] | 
| ads-video-main-message | The primary message or tagline conveyed in the advertisement | inferred | string | [ "video" ] | 
| ads-video-message-clarity | How clear and understandable the main message of the advertisement is | inferred | enums: ["clear", "ambiguous", "Not applicable to the video"] | [ "video" ] | 
| ads-video-target-audience-interests | Specific interests or hobbies that the target audience is likely to have | inferred | Array of strings | [ "video" ] | 
| ads-video-product-type | The category or type of product being advertised | inferred | enums: ["electronics", "apparel", "food\_and\_beverage", "automotive", "home\_appliances", "other", "Not applicable to the video"] | [ "video" ] | 
| ads-video-product-placement | The way the product is positioned or showcased in the advertisement | inferred | enums: ["front\_and\_center", "background", "held\_by\_person", "other", "Not applicable to the video"] | [ "video" ] | 
| ads-video-product-features | The key features or specifications of the advertised product highlighted in the video | inferred | Array of strings | [ "video" ] | 
| ads-video-number-of-products | The number of distinct products or variations featured in the advertisement | inferred | number | [ "video" ] | 

Video also supports array of entities type which helps identify and locate specific entities within video content. This feature returns an array of detected entities. Below is an example of an array of entities in a customer blueprint:

```
  "field_name": {
        "items": {
            "$ref": "bedrock-data-automation#/definitions/Entity"
        },
        "type": "array",
        "instruction": "Please detect all the visually prominent objects in the video",
        "granularity": [
            "chapter"
        ]
    }
```

**Note**  
`bedrock-data-automation#/definitions/Entity` is a BDA owned service type. To parse the results you can use the following schema.

```
       {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "bedrock-data-automation",
        "type": "object",
        "definitions": {
            "BoundingBox": {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                    "left": {
                        "type": "number"
                    },
                    "top": {
                        "type": "number"
                    },
                    "width": {
                        "type": "number"
                    },
                    "height": {
                        "type": "number"
                    }
                }
            },
            "Entity": {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                    "label": {
                        "type": "string"
                    },
                    "bounding_box": {
                        "$ref": "bedrock-data-automation#/definitions/BoundingBox"
                    },
                    "confidence": {
                        "type": "number"
                    }
                }
            }
        },
        "properties": {}
    }
```