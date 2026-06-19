

# TwelveLabs models
<a name="model-parameters-twelvelabs"></a>

This section describes the request parameters and response fields for TwelveLabs models. Use this information to make inference calls to TwelveLabs models. The TwelveLabs Pegasus 1.2 model supports [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) and [InvokeModelWithResponseStream](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) (streaming) operations. The TwelveLabs Marengo Embed 2.7 and TwelveLabs Marengo Embed 3.0 models support [StartAsyncInvoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html) operations. This section also includes code examples that show how to call TwelveLabs models. To use a model in an inference operation, you need the model ID for the model. To get the model ID, see [Supported foundation models in Amazon Bedrock](models-supported.md).

TwelveLabs is a leading provider of multimodal AI models specializing in video understanding and analysis. Their advanced models enable sophisticated video search, analysis, and content generation capabilities through state-of-the-art computer vision and natural language processing technologies.

Amazon Bedrock offers three TwelveLabs models:
+ TwelveLabs Pegasus 1.2 provides comprehensive video understanding and analysis.
+ TwelveLabs Marengo Embed 2.7 generates high-quality embeddings for video, text, audio, and image content.
+ TwelveLabs Marengo Embed 3.0 is the latest embedding model with enhanced performance and capabilities.

These models help you build applications that process, analyze, and derive insights from video data at scale.

**TwelveLabs Pegasus 1.2**

A multimodal model that provides comprehensive video understanding and analysis capabilities, including content recognition, scene detection, and contextual understanding. The model can analyze video content and generate textual descriptions, insights, and answers to questions about the video.

**TwelveLabs Marengo Embed 2.7**

A multimodal embedding model that generates high-quality vector representations of video, text, audio, and image content for similarity search, clustering, and other machine learning tasks. The model supports multiple input modalities and provides specialized embeddings optimized for different use cases.

**TwelveLabs Marengo Embed 3.0**

An enhanced multimodal embedding model that extends the capabilities of Marengo 2.7 with support for text and image interleaved input modality. This model generates high-quality vector representations of video, text, audio, image, and interleaved text-image content for similarity search, clustering, and other machine learning tasks.

**Topics**
+ [TwelveLabs Pegasus 1.2](model-parameters-pegasus.md)
+ [TwelveLabs Marengo Embed 2.7](model-parameters-marengo.md)
+ [TwelveLabs Marengo Embed 3.0](model-parameters-marengo-3.md)