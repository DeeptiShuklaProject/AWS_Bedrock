

# Amazon Titan Multimodal Embeddings G1 model
<a name="titan-multiemb-models"></a>

Amazon Titan Foundation Models are pre-trained on large datasets, making them powerful, general-purpose models. Use them as-is, or customize them by fine tuning the models with your own data for a particular task without annotating large volumes of data.

There are three types of Titan models: embeddings, text generation, and image generation.

There are two Titan Multimodal Embeddings G1 models. The Titan Multimodal Embeddings G1 model translates text inputs (words, phrases or possibly large units of text) into numerical representations (known as embeddings) that contain the semantic meaning of the text. While this model will not generate text, it is useful for applications like personalization and search. By comparing embeddings, the model will produce more relevant and contextual responses than word matching. The Multimodal Embeddings G1 model is used for use cases like searching images by text, by image for similarity, or by a combination of text and image. It translates the input image or text into an embedding that contain the semantic meaning of both the image and text in the same semantic space.

Titan Text models are generative LLMs for tasks such as summarization, text generation, classification, open-ended QnA, and information extraction. They are also trained on many different programming languages, as well as rich text format like tables, JSON, and .csv files, among other formats.

**Amazon Titan Multimodal Embeddings model G1**
+ **Model ID** – `amazon.titan-embed-image-v1`
+ **Max input text tokens** – 256
+ **Languages** – English 
+ **Max input image size** – 25 MB
+ **Max input image resolution** – 2048 x 2048 pixels
+ **Output vector size** – 1,024 (default), 384, 256
+ **Inference types** – On-Demand, Provisioned Throughput
+ **Supported use cases** – Search, recommendation, and personalization.

Titan Text Embeddings V1 takes as input a non-empty string with up to 8,192 tokens and returns a 1,024 dimensional embedding. The characters to token ratio in English is 4.7 char/token, on average. Note on RAG uses cases: While Titan Text Embeddings V2 is able to accommodate up to 8,192 tokens, we recommend to segment documents into logical segments (such as paragraphs or sections). 

## Embedding length
<a name="titanmm-embedding"></a>

Setting a custom embedding length is optional. The embedding default length is 1024 characters which will work for most use cases. The embedding length can be set to 256, 384, or 1024 characters. Larger embedding sizes create more detailed responses, but will also increase the computational time. Shorter embedding lengths are less detailed but will improve the response time. 

```
    # EmbeddingConfig Shape
    {
     'outputEmbeddingLength': {{int}} // Optional, One of: [256, 384, 1024], default: 1024
    }
    
    # Updated API Payload Example
    body = json.dumps({
     "inputText": "hi",
     "inputImage": image_string,
     "embeddingConfig": { 
     "outputEmbeddingLength": 256
     }
    })
```

## Finetuning
<a name="titanmm-finetuning"></a>
+ Input to the Amazon Titan Multimodal Embeddings G1 finetuning is image-text pairs. 
+ Image formats: PNG, JPEG
+ Input image size limit: 25 MB
+ Image dimensions: min: 256 px, max: 4,096 px
+ Max number of tokens in caption: 128
+ Training dataset size range: 1000 - 500,000
+ Validation dataset size range: 8 - 50,000
+ Caption length in characters: 0 - 2,560
+ Maximum total pixels per image: 2048\*2048\*3
+ Aspect ratio (w/h): min: 0.25, max: 4

## Preparing datasets
<a name="titanmm-datasets"></a>

For the training dataset, create a `.jsonl`file with multiple JSON lines. Each JSON line contains both an `image-ref` and `caption` attributes similar to [Sagemaker Augmented Manifest format](https://docs.aws.amazon.com/sagemaker/latest/dg/augmented-manifest.html). A validation dataset is required. Auto-captioning is not currently supported.

```
   {"image-ref": "s3://bucket-1/folder1/0001.png", "caption": "some text"}
   {"image-ref": "s3://bucket-1/folder2/0002.png", "caption": "some text"}
   {"image-ref": "s3://bucket-1/folder1/0003.png", "caption": "some text"}
```

For both the training and validation datasets, you will create `.jsonl`files with multiple JSON lines.

The Amazon S3 paths need to be in the same folders where you have provided permissions for Amazon Bedrock to access the data by attaching an IAM policy to your Amazon Bedrock service role. For more information on granting an IAM policies for training data, see [Grant custom jobs access to your training data](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-model-customization).

## Hyperparameters
<a name="titanmm-hyperparameters"></a>

These values can be adjusted for the Multimodal Embeddings model hyperparameters. The default values will work well for most use cases.
+ Learning rate - (min/max learning rate) – default: 5.00E-05, min: 5.00E-08, max: 1
+ Batch size - Effective batch size – default: 576, min: 256, max: 9,216 
+ Max epochs – default: "auto", min: 1, max: 100