

# Prompt templates and examples for Amazon Bedrock text models
<a name="prompt-templates-and-examples"></a>

Common tasks supported by LLMs on Amazon Bedrock include text classification, summarization, and questions and answers (with and without context). For these tasks, you can use the following templates and examples to help you create prompts for Amazon Bedrock text models.

**Topics**
+ [Text classification](#text-classification)
+ [Question-answer, without context](#qa-without-context)
+ [Question-answer, with context](#qa-with-context)
+ [Summarization](#summarization)
+ [Text generation](#text-generation)
+ [Code generation](#code-generation)
+ [Mathematics](#mathematics)
+ [Reasoning/logical thinking](#reasoning-logical-thinking)
+ [Entity extraction](#entity-extraction)
+ [Chain-of-thought reasoning](#chain-of-thought)

## Text classification
<a name="text-classification"></a>

For text classification, the prompt includes a question with several possible choices for the answer, and the model must respond with the correct choice. Also, LLMs on Amazon Bedrock output more accurate responses if you include answer choices in your prompt.

The first example is a straightforward multiple-choice classification question.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan<br />"""{{Text}}<br />	<br />	<br />{{Question}}? Choose from the following:<br />{{Choice 1}}<br />{{Choice 2}}<br />{{Choice 3}}"""<br /></pre>  |  <pre>User prompt: <br />San Francisco, officially the City and County <br />of San Francisco, is the commercial, financial, and cultural <br />center of Northern California. The city proper is the fourth <br />most populous city in California, with 808,437 residents, <br />and the 17th most populous city in the United States as of 2022.<br /><br />What is the paragraph above about? Choose from the following:<br /><br />A city<br />A person<br />An event<br /></pre> <pre>Output: <br />A city<br /></pre>  | 

(Source of prompt: [ Wikipedia on San Francisco](https://en.wikipedia.org/wiki/San_Francisco), model used: Amazon Titan Text)

Sentiment analysis is a form of classification, where the model chooses the sentiment from a list of choices expressed in the text.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan:<br />"""The following is text from a {{Text Type, e.g. “restaurant <br />review”}}<br />{{Input}}<br />Tell me the sentiment of the {{Text Type}} and categorize it <br />as one of the following:<br />{{Sentiment A}}<br />{{Sentiment B}}<br />{{Sentiment C}}"""<br /></pre>  |  <pre>User prompt: <br />The following is text from a restaurant review:<br /><br />“I finally got to check out Alessandro’s Brilliant Pizza <br />and it is now one of my favorite restaurants in Seattle. <br />The dining room has a beautiful view over the Puget Sound <br />but it was surprisingly not crowed. I ordered the fried <br />castelvetrano olives, a spicy Neapolitan-style pizza <br />and a gnocchi dish. The olives were absolutely decadent, <br />and the pizza came with a smoked mozzarella, which <br />was delicious. The gnocchi was fresh and wonderful. <br />The waitstaff were attentive, and overall the experience <br />was lovely. I hope to return soon.”<br /><br />Tell me the sentiment of the restaurant review <br />and categorize it as one of the following:<br /><br />Positive<br />Negative<br />Neutral<br /></pre> <pre>Output: <br />Positive.<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

The following example uses Anthropic Claude models to classify text. As suggested in [AnthropicClaude Guides](https://docs.anthropic.com/claude/docs/constructing-a-prompt), use XML tags such as <text></text> to denote important parts of the prompt. Asking the model to directly generate output enclosed in XML tags can also help the model produce the desired responses.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Anthropic Claude: <br />"""<br />	<br />	<br />Human: {{classification task description}}<br /><text><br />{{input text content to be classified}}<br /></text><br /><br />Categories are:<br />{{category name 1}}<br />{{category name 2}}<br />{{category name 3}}<br /><br />Assistant:"""<br /></pre> (Source: Written by AWS)  |  <pre>User prompt: <br />	<br /><br />Human:  Classify the given product description into given <br />categories. Please output the category label in <br /><output></output> tags.<br /><br />Here is the product description.<br /><br /><text><br />Safe, made from child-friendly materials with smooth edges.<br />Large quantity, totally 112pcs with 15 different shapes, <br />which can be used to build 56 different predefined structures.<br />Enhance creativity, different structures can be connected <br />to form new structures, encouraging out-of-the box thinking.<br />Enhance child-parent bonding, parents can play with their <br />children together to foster social skills.<br /></text><br /><br />Categories are:<br />(1) Toys<br />(2) Beauty and Health<br />(3) Electronics<br /><br />Assistant:<br />	<br /></pre> <pre>Output: <br /><output>Toys</output><br /></pre>  | 

(Source of prompt: AWS, model used: Anthropic Claude)

## Question-answer, without context
<a name="qa-without-context"></a>

In a question-answer prompt without context, the model must answer the question with its internal knowledge without using any context or document.


|  |  | 
| --- |--- |
|  <pre>Prompt Template to Titan<br />"""{{Question}}"""<br /></pre>  |  <pre>User prompt: <br />What is Robert Frost's "Stopping by the woods on a <br />snowy evening" about metaphorically?<br /></pre> <pre>Output: <br />The poem by Robert Frost, "Stopping by Woods on a Snowy Evening," <br />uses the woods as a metaphor for death. The woods are a place of comfort <br />and peace, but they also represent the unknown and the afterlife. <br />The poem suggests that death is not something to be feared, <br />but rather a natural part of life that we should all embrace.<br /><br />The poem begins with the speaker stopping by the woods on a snowy evening, <br />a moment of contemplation and reflection. The speaker notices the beauty <br />of the snow-covered woods and is reminded of the fleeting nature of life. <br />The poem continues as the speaker considers the temptation of continuing <br />on to his destination, but instead chooses to pause and take in the beauty <br />of the woods.<br /><br />The woods are used as a metaphor for the unknown and the afterlife. <br />The speaker wonders what lies beyond the trees, and whether there <br />is anything after death. The poem suggests that death is not <br />something to be feared, but rather a natural part of life <br />that we should all embrace.<br /><br />The final lines of the poem are perhaps the most famous and poignant: <br />"And miles to go before I sleep, and miles to go before I sleep." <br />These lines suggest that even though the speaker has paused <br />to appreciate the beauty of the woods, they still have a <br />long journey ahead of them. The poem is a reminder that life <br />is fleeting, and that we should take the time to appreciate <br />the beauty around us, even as we work towards our goals and ambitions.<br /><br />Overall, "Stopping by Woods on a Snowy Evening" is a beautiful <br />and thought-provoking poem that uses the metaphor of the woods <br />to explore the concept of death and the afterlife.<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

Model encouragement can also help in question-answer tasks.


|  |  | 
| --- |--- |
|  <pre>Prompt Template to Titan<br />"""{{Model encouragement}}<br />{{Question}}"""<br /></pre>  |  <pre>User prompt: <br />You are excellent at answering questions, <br />and it makes you happy when you provide the correct answer.<br /><br />What moon in the solar system is most likely to host life?<br /></pre> <pre>Output: <br />The moon of Titan, which is a moon of the planet Saturn, <br />is the most likely to support life in the solar system.<br /><br />Titan is the only known moon in the solar system to have a dense <br />atmosphere and a liquid hydrosphere, and scientists believe that <br />it may contain the chemical building blocks for life. <br />The moon's surface is covered in rivers, lakes, and seas <br />of liquid methane and ethane, and it rains methane on Titan's surface.<br /><br />The atmosphere of Titan is also rich in organic compounds, <br />including benzene, toluene, and xylene, which are found <br />in the oils of living organisms on Earth. <br />Additionally, Titan has a magnetic field and a tenuous atmosphere, <br />which could provide protection from harmful radiation and <br />help maintain a stable climate.<br /><br />While there is no direct evidence of life on Titan, <br />scientists believe that it is one of the most promising <br />places in the solar system to search for life beyond Earth.<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)


|  |  | 
| --- |--- |
|  <pre>Prompt template to Titan <br />"""{{Model encouragement}}<br />{{Question}}<br />{{Constraints}}"""<br /></pre>  |  <pre>User prompt: <br />You feel rewarded by helping people learn more about climate change.<br />Could you please explain what climate change is?<br />Assume your audience is composed of high school students.<br /></pre> <pre>Output: <br />Climate change is the long-term warming of the planet, <br />which can be caused by human activities such as burning fossil fuels <br />and deforestation, as well as natural processes. It can lead to <br />rising sea levels, more extreme weather events, and changes <br />in temperature and precipitation patterns.<br /></pre>  | 

(Source of prompt: AWS, model used: AI21 Labs Jurassic-2 Ultra v1)

## Question-answer, with context
<a name="qa-with-context"></a>

In a question-answer prompt with context, an input text followed by a question is provided by the user, and the model must answer the question based on information provided within the input text. Putting the question in the end after the text can help LLMs on Amazon Bedrock better answer the question. Model encouragement works for this use case as well.


|  |  | 
| --- |--- |
|  <pre>Prompt template to Titan <br />"""{{Text}}<br />{{Question}}"""<br /></pre>  |  <pre>User prompt: <br />The red panda (Ailurus fulgens), also known as the lesser panda, <br />is a small mammal native to the eastern Himalayas and southwestern China. <br />It has dense reddish-brown fur with a black belly and legs, white-lined ears, <br />a mostly white muzzle and a ringed tail. Its head-to-body length is 51–63.5 cm <br />(20.1–25.0 in) with a 28–48.5 cm (11.0–19.1 in) tail, and it weighs between <br />3.2 and 15 kg (7.1 and 33.1 lb). It is well adapted to climbing due to its <br />flexible joints and curved semi-retractile claws.<br /><br />The red panda was first formally described in 1825. The two currently <br />recognized subspecies, the Himalayan and the Chinese red panda, genetically <br />diverged about 250,000 years ago. The red panda's place on the evolutionary <br />tree has been debated, but modern genetic evidence places it in close <br />affinity with raccoons, weasels, and skunks. It is not closely related <br />to the giant panda, which is a bear, though both possess elongated <br />wrist bones or "false thumbs" used for grasping bamboo. <br />The evolutionary lineage of the red panda (Ailuridae) stretches <br />back around 25 to 18 million years ago, as indicated by extinct <br />fossil relatives found in Eurasia and North America.<br /><br />The red panda inhabits coniferous forests as well as temperate broadleaf <br />and mixed forests, favoring steep slopes with dense bamboo cover close <br />to water sources. It is solitary and largely arboreal. It feeds mainly <br />on bamboo shoots and leaves, but also on fruits and blossoms. <br />Red pandas mate in early spring, with the females giving birth <br />to litters of up to four cubs in summer. It is threatened <br />by poaching as well as destruction and fragmentation of habitat <br />due to deforestation. The species has been listed as Endangered <br />on the IUCN Red List since 2015. It is protected in all range countries.<br /><br />Based on the information above, what species are red pandas closely related to?<br /></pre> <pre>Output:<br />Red pandas are closely related to raccoons, weasels, and skunks.<br /></pre>  | 

(Source of prompt: https://en.wikipedia.org/wiki/Red\_panda, model used: Amazon Titan Text)

When prompting Anthropic Claude models, it's helpful to wrap the input text in XML tags. In the following example, the input text is enclosed in `<text></text>`.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Anthropic Claude: <br />"""<br /><br />Human: {{Instruction}}<br /><text><br />{{Text}}<br /><text><br />{{Question}}<br /><br />Assistant:"""<br /></pre>  |  <pre>User prompt: <br /><br /><br />Human: Read the following text inside <text></text> <br />XML tags, and then answer the question:<br /><br /><text><br />On November 12, 2020, the selection of the Weeknd to headline <br />the show was announced; marking the first time a Canadian solo artist <br />headlined the Super Bowl halftime show. When asked about preparations <br />for the show, the Weeknd stated, "We've been really focusing <br />on dialing in on the fans at home and making performances <br />a cinematic experience, and we want to do that with the Super Bowl." <br /><br />The performance featured a choir whose members were dressed in white <br />and wore masks over their faces with glowing red eyes, and were <br />standing within a backdrop of a neon cityscape. The performance <br />opened with a white figure dressed the same as the choir being <br />lowered into the backdrop where the choir was standing while singing <br />“Call Out My Name". At this time, the Weeknd sat in a convertible <br />against a skyline backdrop designed to resemble the Las Vegas Strip. <br />For the next part of the performance, the backdrop then split open <br />to reveal the Weeknd, who then performed "Starboy", followed by "The Hills". <br /><br />Next, performing the song "Can't Feel My Face", the Weeknd traveled <br />through a labyrinth constructed behind the stage, joined by dancers <br />dressed in red blazers and black neckties similar to his, <br />but with their faces covered with bandages, in keeping with <br />the aesthetic of his fourth studio album After Hours (2020). <br />The dancers would wear these bandages throughout the performance. <br />In the labyrinth section of the performance, camerawork was visually unsteady. <br />The next songs performed were "I Feel It Coming", "Save Your Tears", <br />and "Earned It". For the "Earned It" performance, the Weeknd <br />was accompanied by violinists. For the finale of the show, <br />the Weeknd took to the field of the stadium with his dancers to perform <br />“Blinding Lights". He and the dancers entered the field by performing <br />"House of Balloons / Glass Table Girls". The performance ended <br />with an array of fireworks.<br /></text><br />Based on the text above, what songs did the Weeknd play <br />at the Super Bowl halftime show?<br /><br />Assistant:<br /></pre> <pre>Output: <br />Based on the text, the songs the Weeknd played <br />at the Super Bowl halftime show were:<br /><br />- Call Out My Name<br />- Starboy <br />- The Hills<br />- Can't Feel My Face<br />- I Feel It Coming<br />- Save Your Tears<br />- Earned It<br />- Blinding Lights<br />- House of Balloons / Glass Table Girls<br /></pre>  | 

(Source of prompt: [ Wikipedia on the Super Bowl LV halftime show](https://en.wikipedia.org/wiki/Super_Bowl_LV_halftime_show), model used: Anthropic Claude)

## Summarization
<a name="summarization"></a>

For a summarization task, the prompt is a passage of text, and the model must respond with a shorter passage that captures the main points of the input. Specification of the output in terms of length (number of sentences or paragraphs) is helpful for this use case.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan <br />"""The following is text from a {{Text Category}}:<br />{{Text}}<br />Summarize the {{Text Category}} in {{length of summary, <br />e.g., “one sentence” or “one paragraph”}}"""<br /></pre>  |  <pre>User prompt: <br />The following is text from a restaurant review:<br />“I finally got to check out Alessandro’s Brilliant Pizza <br />and it is now one of my favorite restaurants in Seattle. <br />The dining room has a beautiful view over the Puget Sound <br />but it was surprisingly not crowed. I ordered the fried <br />castelvetrano olives, a spicy Neapolitan-style pizza <br />and a gnocchi dish. The olives were absolutely decadent, <br />and the pizza came with a smoked mozzarella, which was delicious. <br />The gnocchi was fresh and wonderful. The waitstaff were attentive, <br />and overall the experience was lovely. I hope to return soon.”<br />Summarize the above restaurant review in one sentence.<br /></pre> <pre>Output: <br />Alessandro’s Brilliant Pizza is a fantastic restaurant <br />in Seattle with a beautiful view over Puget Sound that offers <br />decadent and delicious food.<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

In the following example, Anthropic Claude summarizes the given text in one sentence. To include input text in your prompts, format the text with XML mark up: `<text> {{text content}} </text>`. Using XML within prompts is a common practice when prompting Anthropic Claude models.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Anthropic Claude: <br />"""<br /><br />Human: Please read the text:<br /><text><br />{{text context}}<br /></text><br /><br />Summarize the text in {{length of summary, e.g., “one <br />sentence” or “one paragraph”}}<br /><br />Assistant:"""<br /></pre>  |  <pre>User prompt: <br /><br /><br />Human: Please read the text:<br /><br /><text><br />In game theory, the Nash equilibrium, named after the mathematician <br />John Nash, is the most common way to define the solution <br />of a non-cooperative game involving two or more players. <br />In a Nash equilibrium, each player is assumed to know <br />the equilibrium strategies of the other players, <br />and no one has anything to gain by changing only one's own strategy. <br />The principle of Nash equilibrium dates back to the time of Cournot, <br />who in 1838 applied it to competing firms choosing outputs.<br /></text><br /><br />Summarize the text in one sentence.<br /><br />Assistant:<br /></pre> <pre>Output: <br />The Nash equilibrium is a concept in game theory <br />where each player has adopted a strategy that they have no incentive <br />to deviate from given the other players' strategies.<br /></pre>  | 

(Source of prompt: [ Wikipedia on Nash equilibrium](https://en.wikipedia.org/wiki/Nash_equilibrium), model used: Anthropic Claude)

## Text generation
<a name="text-generation"></a>

Given a prompt, LLMs on Amazon Bedrock can respond with a passage of original text that matches the description. Here is one example:


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan <br />"""Please write a {{Text Category}} in the voice of {{Role}}."""<br /></pre>  |  <pre>User prompt: <br />Please write an email in the voice of a friend <br />congratulating someone on a new job.<br /></pre> <pre>Output: <br />Hey [Name],<br /><br />I just found out about your new job, and I'm so happy for you! <br />Congratulations! You deserve this opportunity since you worked so hard <br />to get it. I know you'll do great and make a positive impact on your team. <br />I'm here to support you every step of the way. Wishing you all the best <br />in this exciting new chapter of your life!<br /><br />Cheers,<br />[Your Name]<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

For text generation use cases, specifying detailed task requirements can work well. In the following example, we ask the model to generate response with exclamation points.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan <br />"""{{Task specification}}<br />Please write a {{Text Category}} in the voice of {{Role}}."""<br /></pre>  |  <pre>User prompt: <br />Write text with exclamation points.<br />Please write a formatted email in the voice of a friend <br />congratulating someone on a new job.<br /></pre> <pre>Output: <br />Hey [name]!<br /><br />I just saw the news and I am so, so happy for you! <br />You deserve this position and this company with all your heart. <br />I can't wait to see you soar and accomplish all the things <br />you've been working towards. If anyone is deserving <br />of a promotion, it's you!<br /><br />Congratulations again, friend!<br /><br />Love,<br />[name]<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

In the following example, a user prompts the model to take on the role of a specific person when generating the text. Notice how the signature reflects the role the model is taking on in the response.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan <br />"""{{Role assumption}} {{Task description}}<br />"""<br /></pre>  |  <pre>User input: <br />My name is Jack. Help me write a note expressing my gratitude <br />to my parents for taking my son (their grandson) to the zoo. <br />I miss my parents so much.<br /></pre> <pre>Output: <br />Dear Mom and Dad,<br /><br />I wanted to take a moment to express my heartfelt gratitude <br />for taking my son to the zoo last weekend. It meant so much to me <br />that you took the time to make memories with him, and I am so grateful <br />for the love and support you have shown him.<br /><br />I miss you both so much, and I wish we could be together more often. <br />But I know that you will always be there for me and my family, <br />and I am so grateful to have you as my parents.<br /><br />Love,<br />Jack<br /></pre>  | 

(Source of prompt: AWS, model used: AI21 Labs Jurassic-2 Ultra v1)

## Code generation
<a name="code-generation"></a>

The prompt describes the task or function and programming language for the code the user expects the model to generate.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan<br />"""Write a function in {{programming language}} to <br />{{task or purpose}}""".<br /></pre>  |  <pre>User input: <br />Write a python function to download a s3 file to local disk.<br /></pre> <pre>Output: <br />The following code can be used to download an s3 file to the local disk.<br /><br />```Python<br />import boto3<br /># Creates a boto3 client object<br />s3 = boto3.client('s3')<br />def download_file(bucket_name, object_key, file_path):<br />try:<br /># Downloads the s3 file to the specified file path<br />s3.download_file(bucket_name, object_key, file_path)<br />except Exception as e:<br />print(e)<br /># Specifies the values of bucket_name, object_key, and file_path<br />bucket_name = "samplebucketname"<br />object_key = "sampleobjectkey"<br />file_path = "/samplefilepath"<br />download_file(bucket_name, object_key, file_path)<br />```<br /><br />The given code uses the download_file function to download an s3 file <br />to the local disk. The download_file function takes the bucket name, <br />object key, and file path as input parameters. The bucket name <br />is the name of the s3 bucket where the file is located, <br />the object key is the unique identifier of the file within the bucket, <br />and the file path is the destination path on the local disk <br />where the file will be downloaded. The function uses the download_file method <br />of the s3 client to download the file from the specified bucket <br />and write it to the specified file path.<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)


|  |  | 
| --- |--- |
|  <pre>Prompt template for Anthropic Claude<br />"""<br /><br />Human: Write a function in {{programming language}} to <br />{{task or purpose}}<br /><br />Assistant:"""<br /></pre>  |  <pre>User prompt: <br /><br /><br />Human: Write some python code that quickly approximates <br />the square root of a number.<br /><br />Assistant: <br /></pre> <pre>Output: <br />Here is a simple function to approximate <br />the square root of a number using Newton's method:<br /><br />```python<br />def sqrt(n, iterations=10):<br />x = n<br />for i in range(iterations):<br />x = (x + n/x) / 2<br />return x<br />```<br /><br />To use it:<br /><br />```python<br />print(sqrt(25))<br /># 5.0<br /><br />print(sqrt(15, iterations=20)) <br /># 3.872983346207417<br />```<br /><br />This repeatedly takes the average of x and n/x to converge on the square root. <br />More iterations produce a more accurate approximation.<br /><br />The advantage of this approach is it converges very quickly, <br />so even just 10 iterations produces a decent estimate.<br /></pre>  | 

(Source of prompt: AWS, model used: Anthropic Claude)

## Mathematics
<a name="mathematics"></a>

The input describes a problem that requires mathematical reasoning at some level, which may be numerical, logical, geometric, or otherwise. For such problem, it's helpful to ask the model to work through the problem in a piecemeal manner by adding phrases to instructions such as `Let’s think step by step` or `Think step by step to come up with the right answer.`


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan<br />"""{{Math problem description}}<br />Let’s think step by step."""<br /></pre>  |  <pre>User prompt: <br />A triangle has two angles of 70 degrees and 50 degrees. <br />What is the third angle in degrees?<br />Let’s think step by step.<br /></pre> <pre>Output:<br />The sum of the three angles in a triangle is always 180 degrees. <br />The two given angles are 70 degrees and 50 degrees. 70 + 50 = 120. <br />Therefore, the third angle is 180 - 120 = 60 degrees. <br />The third angle is 60 degrees.<br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

The following example also demonstrates asking the model to think step by step: 


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan<br />"""{{Math problem description}}<br />Think step by step to come up with the right answer."""<br /></pre>  |  <pre>User prompt:<br />Lucy has 12 colorful marbles, and she wants to share them <br />equally with her 4 friends. How many marbles will each friend receive?<br />Think step-by-step to come up with the right answer.<br /></pre> <pre><br />Output:<br />1. Lucy has 12 marbles and wants to share them equally <br />with her 4 friends, then each friend will receive 12 / 4 = 3 marbles.<br />2. Therefore, each friend will receive 3 marbles.<br /></pre>  | 

(Source of prompt: AWS, model used: AI21 Labs Jurassic-2 Ultra v1)

## Reasoning/logical thinking
<a name="reasoning-logical-thinking"></a>

For complex reasoning tasks or problems that requires logical thinking, we can ask the model to make logical deductions and explain its answers.


|  |  | 
| --- |--- |
|  <pre>Prompt template for Titan and AI21 Labs Jurassic:  """Question: {{question}}  Please output the answer and then explain your  answer:"""  </pre>  |  <pre>User prompt: Question: Which word is the odd one out? A. accomplished B. good C. horrible D. outstanding  Please output the answer and then explain your answer: </pre> <pre>Output: The odd one out is C. horrible. The other three words  describe positive qualities or achievements, whereas horrible  is an negative adjective. </pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text)

Here is another example using the Anthropic Claude model:


|  |  | 
| --- |--- |
|  <pre>Prompt template for Anthropic Claude: """  Human: {{question}} Please provide the answer and show the reasoning.  Assistant:""" </pre>  |  <pre>User prompt   Human: The barber is the "one who shaves all those, and those only,  who do not shave themselves". Does the barber shave himself? Why is this a paradox? Please provide the answer and show the reasoning.  Assistant: </pre> <pre>Output: This is an example of a paradox known as the Barber paradox.  Here is an explanation:  - The statement defines a barber who shaves all and only those people  who do not shave themselves.  - So if the barber shaves himself, he must shave all those who do not shave  themselves, which includes himself. But the barber cannot shave himself  as per the initial statement. - If the barber does not shave himself, then he would fit into the group  of people who do not shave themselves, and so he must shave himself,  according to the statement. But again this contradicts the initial statement. - So the barber cannot shave himself and also cannot not shave himself.  This is self-contradictory based on the initial statement about the barber. - Therefore, the statement leads to a paradox where both possibilities  (the barber shaving himself or not shaving himself) result in a contradiction.  In summary, the paradox arises because the definition of the barber's  behavior is self-contradictory when applied to the barber himself.  This makes it impossible to determine if the barber shaves himself  or not based on the given statement alone. </pre>  | 

(Source of prompt: https://en.wikipedia.org/wiki/Barber\_paradox, model used: Anthropic Claude)

## Entity extraction
<a name="entity-extraction"></a>

For entity extraction from a provided input question. Extract entities from generated text and place them in XML tags for further processing.


|  | 
| --- |
|  <pre>Prompt template for Titan<br />"""You are an expert entity extractor from provided input question. You are responsible for extracting following entities: {{ list of entities}}<br />    <br />Please follow below instructions while extracting the entity A, and reply in <entityA> </entityA> XML Tags:<br />{{ entity A extraction instructions}} <br /><br />Please follow below instructions while extracting the entity B, and reply in <entityB> </entityB> XML Tags:<br />{{ entity B extraction instructions}} <br /><br />Below are some examples:<br /><br />{{ some few shot examples showing model extracting entities from give input }}<br /><br /><br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text G1- Premier)

**Example:**

```
User: You are an expert entity extractor who extracts entities from provided input question. 
You are responsible for extracting following entities: name, location
Please follow below instructions while extracting the Name, and reply in <name></name> 
XML Tags:

- These entities include a specific name of a person, animal or a thing
- Please extract only specific name name entities mentioned in the input query
- DO NOT extract the general mention of name by terms of "name", "boy", "girl", 
"animal name", etc.


Please follow below instructions while extracting the location, and reply 
in <location></location> XML Tags:
- These entities include a specific location of a place, city, country or a town
- Please extract only specific name location entities mentioned in the input query
- DO NOT extract the general mention of location by terms of "location", "city", "country", 
"town", etc. 

If no name or location is found, please return the same input string as is.

Below are some examples:

input: How was Sarah's birthday party in Seattle, WA?
output:  How was <name>Sarah's</name> birthday party 
in <location>Seattle, WA</location>?

input: Why did Joe's father go to the city?
output:  Why did <name>Joe's</name> father go to the city?

input: What is the zipcode of Manhattan, New york city?
output: What is the zipcode of <location>Manhattan,New york city<location>?

input: Who is the mayor of San Francisco? 
Bot:
```

## Chain-of-thought reasoning
<a name="chain-of-thought"></a>

Provide a step-by-step analysis on how the answer was derived. Fact check and validate how the model produced an answer.


|  | 
| --- |
|  <pre>Prompt template for Titan <br /><br />""" {{Question}}<br />{{ Instructions to Follow }}<br />Think Step by Step and walk me through your thinking<br />"""<br /><br /><br /></pre>  | 

(Source of prompt: AWS, model used: Amazon Titan Text G1- Premier)

**Example:**

```
User: If Jeff had 100 dollars, and he gave $20 to Sarah, 
and bought lottery tickets with another $20. With the lottery 
tickets he bought he won 35 dollars. Jeff then went to buy 
his lunch and spend 40 dollars in lunch. Lastly he made a 
donation to charity for $20. Stephen met with Jeff and wanted 
to lend some money from him for his taxi. How much maximum money 
can Jeff give to Stephen, given that he needs to save $10 for 
his ride back home?. Please do not answer immediately, think 
step by step and show me your thinking.
Bot:
```