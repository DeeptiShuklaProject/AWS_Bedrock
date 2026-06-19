

# Creating blueprints for images
<a name="bda-idp-images"></a>

Amazon Bedrock Data Automation (BDA) allows you to create custom blueprints for image modalities. You can use blueprints to define the desired output format and extraction logic for your input files. By creating custom blueprints, you can tailor BDA's output to meet your specific requirements. Within one project, you can apply a single image blueprint.

## Defining data fields for images
<a name="bda-images-defining-data-fields"></a>

BDA allows you to define the specific fields you want to identify from your images by creating a blueprint. This acts as a set of instructions that guide BDA on what information to extract and generate from your images.

### Blueprint fields examples for advertisement images
<a name="w2aac32c10c14c11b9b5b5"></a>

Here are some examples of blueprint fields to analyze advertisement images.




|  |  |  |  | 
| --- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | 
| product\_type | What is the primary product or service being advertised? Ex: Clothing, Electronics, Food & Beverage | inferred | string | 
| product\_placement | How is the product placed in the advertisement image, e.g., centered, in the background, held by a person, etc.? | inferred | string | 
| product\_size | Product size is small if size is less than 30% of the image, medium if it is between 30 to 60%, and large if it is larger than 60% of the image | inferred | string | 
| image\_style | Classify the image style of the ad. For example, product image, lifestyle, portrait, retro, infographic, none of the above. | inferred | string | 
| image\_background | Background can be" solid color, natural landscape, indoor, outdoor, or abstract.  | inferred | string | 
| promotional\_offer | Does the advertisement include any discounts, offers, or promotional messages? | inferred | boolean | 

### Examples of blueprint fields for media search
<a name="w2aac32c10c14c11b9b5b7"></a>

Here are some examples of blueprint fields to generate metadata from images for media search.




|  |  |  |  | 
| --- |--- |--- |--- |
| Field | Instruction | Extraction Type | Type | 
| person\_counting | How many people are in the image? | inferred | number | 
| indoor\_outdoor\_classification | Is the image indoor or outdoor? | inferred | string | 
| scene\_classification | Classify the setting or environment of the image. Ex: Urban, Rural, Natural, Historical, Residential, Commercial, Recreational, Public Spaces | inferred | string | 
| animal\_identification | Does the image contain any animals? | inferred | boolean | 
| animal\_type | What type of animals are present in the image? | inferred | string | 
| color\_identification | Is the image in color or black and white? | inferred | string | 
| vehicle\_identification | Is there any vehicle visible in the image? | inferred | string | 
| vehicle\_type | What type of vehicle is present in the image? | inferred | string | 
| watermark\_identification | Is there any watermark visible in the image? | inferred | boolean | 