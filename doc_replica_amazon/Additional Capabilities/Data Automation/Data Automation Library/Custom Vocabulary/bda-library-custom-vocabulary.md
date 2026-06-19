

# Custom Vocabulary
<a name="bda-library-custom-vocabulary"></a>

You can provide domain-specific words and phrases per language, which enables BDA to improve extraction accuracy for your audio and video content. You can include terminology unique to your industry or domain — such as brand names, acronyms, proper nouns, and specialized terms — which enables BDA to recognize and extract those terms accurately from your processed content.

**Important**  
You are responsible for the integrity of your own data when you use Bedrock Data Automation Library. Do not enter confidential information, personal information (PII), or protected health information (PHI) into a custom vocabulary.

You can find the list of supported languages for Custom Vocabulary [here](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-limits.html). Note that only the characters listed in your language's [character set](bda-library-character-sets.md) can be used in a custom vocabulary.

## How to use?
<a name="bda-library-cv-how-to-use"></a>

You can use Custom Vocabulary in your BDA project by creating a Data Automation Library, adding domain-specific vocabulary entities/lists for your target language, and associating the library with your project during project creation or by updating an existing project, which enables all audio and video processing jobs executed through that project to apply your custom vocabulary. This results in improved extraction accuracy for your domain-specific terms across both standard output and custom blueprint output.

**Considerations when using Custom Vocabulary:**
+ Focus on domain-specific terms that are frequently mis-recognized
+ Include common variations and spellings of important terms
+ Organize vocabulary by language for better management
+ Prioritize industry-specific jargon and technical terms
+ Include acronyms and abbreviations commonly used in your domain