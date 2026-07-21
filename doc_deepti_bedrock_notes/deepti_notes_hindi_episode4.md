# Amazon Bedrock AgentCore Deep Dive: Gateway (Hindi Notes 🇮🇳)

यह नोट्स **AWS Show & Tell: Amazon Bedrock AgentCore Deep dive series: Gateway** वीडियो के आधार पर बनाए गए हैं। इसे सरल, रोचक और स्पष्ट Hinglish में तैयार किया गया है ताकि शुरुआती (Beginner) डेवलपर्स इसे आसानी से समझ सकें।

---

## 🚪 AgentCore Gateway क्या है? (What is AgentCore Gateway?)

सरल शब्दों में, **AgentCore Gateway** आपके AI Agents और Tools (APIs, Databases, Lambda functions) के बीच की **कड़ी (Bridge)** है। यह एक **Fully Managed, Serverless Service** है जो सभी टूल्स को एक स्थान पर व्यवस्थित (Orchestrate) और सुरक्षित (Secure) करती है।

### 🔌 $M \times N$ की समस्या और Gateway का समाधान:
जब आपके पास कई सारे Agents ($M$) होते हैं और उन्हें कई सारे Tools ($N$) का उपयोग करना होता है, तो हर एजेंट को हर टूल से अलग-अलग कनेक्ट करना बहुत कठिन (Complex) हो जाता है। 

* **पुराना तरीका:** हर एजेंट में हर टूल का कोड और क्रेडेंशियल्स डालना पड़ता था।
* **Gateway का तरीका:** सभी एजेंट्स केवल एक Gateway से बात करते हैं, और वह Gateway सभी टूल्स को मैनेज करता है।

```mermaid
graph TD
    subgraph Agents Layer
        Agent1[Strands Agent]
        Agent2[LangGraph Agent]
    end

    subgraph Gateway Layer
        Gateway[AgentCore Gateway]
    end

    subgraph Tools Layer
        Tool1[AWS Lambda - Database]
        Tool2[OpenAPI - Slack API]
        Tool3[OpenAPI - NASA Weather]
    end

    Agent1 -->|Talks to| Gateway
    Agent2 -->|Talks to| Gateway

    Gateway -->|Routes & Translates| Tool1
    Gateway -->|Routes & Translates| Tool2
    Gateway -->|Routes & Translates| Tool3
```

### 💡 व्यावहारिक उदाहरण (Practical Example)
मान लीजिए हमारी कंपनी में **3 अलग-अलग AI Agents** हैं और उन्हें **3 अलग-अलग सिस्टम** का उपयोग करना है:

* **3 Agents (ग्राहक):**
  1. `HR-Agent` (कर्मचारियों की जानकारी के लिए)
  2. `Finance-Agent` (खर्च और सैलरी अप्रूवल के लिए)
  3. `IT-Support-Agent` (लैपटॉप टिकटिंग के लिए)
* **3 Systems (टूल्स):**
  1. `Workday API` (कर्मचारी डेटा - OAuth आधारित)
  2. `Concur API` (सैलरी और बिल - API Key आधारित)
  3. `Jira API` (IT टिकट्स - Bearer Token आधारित)

#### ❌ Gateway के बिना (Without Gateway - पुराना तरीका):
* आपको हर एक एजेंट के कोड में अलग-अलग सिस्टम से जुड़ने का लॉजिक लिखना होगा।
* आपको सभी API Keys और Secrets को हर एजेंट कंटेनर में इंजेक्ट करना होगा, जो सुरक्षा की दृष्टि से बेहद खतरनाक है (Security Risk!)।
* अगर कल को Jira API का वर्जन बदलता है, तो आपको सभी तीनों एजेंटों का कोड बदलना और उन्हें फिर से डिप्लॉय करना होगा।

#### 🛡️ Gateway के साथ (With Gateway - आधुनिक तरीका):
* आप Gateway में इन तीनों सिस्टम्स को **"Logical Targets"** के रूप में रजिस्टर कर देते हैं और उनके क्रेडेंशियल्स को **AWS Secrets Manager** में सेव कर देते हैं।
* सभी 3 एजेंट्स केवल एक ही सुरक्षित Gateway URL से बात करेंगे।
* जब `IT-Support-Agent` टिकटिंग के लिए कॉल करेगा, तो Gateway ऑटोमैटिकली Secrets Manager से Jira का Token लेकर रिक्वेस्ट में जोड़ देगा और Jira API पर भेज देगा।
* **बड़ा फायदा:** एजेंट्स के डेवलपर को कभी भी Concur, Jira या Workday का ओरिजिनल पासवर्ड या क्रेडेंशियल देखने को नहीं मिलता। सब कुछ गेटवे के भीतर सुरक्षित रहता है!

---

## 🌟 Gateway की 4 मुख्य विशेषताएं (Key Features)

### 1. Zero-Code MCP-ification (बिना कोडिंग के टूल बनाना)
आपको टूल्स के लिए खुद से कोई MCP (Model Context Protocol) सर्वर बनाने या JSON-RPC 2.0 स्पेसिफिकेशन कोड लिखने की ज़रूरत नहीं है।
* आप सीधे अपनी **OpenAPI/Swagger Spec** (JSON/YAML फ़ाइल) या **AWS Lambda Function** को Gateway में रजिस्टर कर सकते हैं।
* Gateway खुद-ब-खुद MCP रिक्वेस्ट को संबंधित API फ़ॉर्मेट में बदल (translate) देता है।

### 2. Semantic Tool Search (स्मार्ट टूल खोज)
यदि किसी कंपनी के पास 500 से अधिक टूल्स हैं और वे सभी टूल्स एक ही बार में LLM (मॉडल) को दे दिए जाएं, तो:
1. **Context Bloat (बजट और लेटेंसी बढ़ना):** इनपुट पेलोड बहुत बड़ा हो जाएगा।
2. **Hallucination:** मॉडल भ्रमित (confuse) होकर गलत टूल चुन सकता है।

* **समाधान:** AgentCore Gateway **Semantic Search (राग/RAG पैटर्न)** का उपयोग करता है। यूजर की क्वेरी के आधार पर यह केवल सबसे प्रासंगिक (जैसे Top 10) टूल्स को ढूँढकर एजेंट को देता है।

### 3. Inbound Authorization (आने वाले कॉल्स की सुरक्षा)
Gateway पर केवल वही क्लाइंट्स एक्सेस कर सकते हैं जो अधिकृत (Authorized) हों:
* यह **Cognito, Auth0, Octa** जैसे OAuth 2.0 प्रोवाइडर्स के साथ सीधे जुड़ता है।
* आने वाले हर रिक्वेस्ट में JWT/Bearer Token होना अनिवार्य है।

### 4. Outbound Authorization (बाहरी APIs के क्रेडेंशियल्स की सुरक्षा)
जब एजेंट को किसी बाहरी API (जैसे Slack, NASA API) को कॉल करना होता है, तो क्रेडेंशियल्स (API Keys) को सुरक्षित रखने की आवश्यकता होती है:
* क्रेडेंशियल्स को **AWS Secrets Manager** में रखा जाता है।
* Gateway खुद बैकएंड से इन सीक्रेट्स को निकालता है और बाहरी API को कॉल करते समय लगाता है। 
* **फायदा:** आपके एजेंट क्लाइंट या यूजर को कभी भी Slack/NASA की ओरिजिनल API Key देखने की ज़रूरत नहीं पड़ती।

---

## 💻 Step-by-Step Demo Workflow (वीडियो के आधार पर)

वीडियो में देव और निक ने Python Starter Toolkit का उपयोग करके Gateway को सेटअप करके दिखाया है।

### Step 1: Gateway Client और Cognito Authorizer बनाना
सबसे पहले, Starter Toolkit का उपयोग करके इनबाउंड ऑथराइजेशन (Cognito User Pool) और Gateway को खड़ा किया जाता है:

```python
from bedrock_agent_core_starter_toolkit import GatewayClient

# 1. Gateway Client शुरू करना
client = GatewayClient(region="us-east-1")

# 2. Cognito Authorizer बनाना (यह एक ही कमांड में यूजर पूल, डोमेन और IAM रोल्स सेट करता है)
cognito_authorizer = client.create_cognito_authorizer(name="MyGatewayUserPool")

# 3. Gateway बनाना
gateway = client.create_mcp_gateway(
    name="MyFirstGateway",
    authorizer_config=cognito_authorizer
)

# यह आपको एक यूनीक Gateway URI देगा:
print(f"Gateway URL: {gateway.url}")
```

### Step 2: AWS Lambda को टूल बनाना (MCP-ify Lambda)
एक डिफ़ॉल्ट या कस्टम Lambda फ़ंक्शन को Gateway में 'Target' के रूप में जोड़ना:

```python
# AWS Lambda को टूल के रूप में रजिस्टर करना
lambda_target = client.create_gateway_target(
    gateway_name="MyFirstGateway",
    target_type="lambda",
    # आप अपना कस्टम Lambda ARN और स्कीमा भी दे सकते हैं
)
```

### Step 3: MCP Inspector के साथ टेस्ट करना
निक ने दिखाया कि कैसे हम एंथ्रोपिक के ओपन-सोर्स **MCP Inspector** का उपयोग करके गेटवे को टेस्ट कर सकते हैं:
1. MCP Inspector UI खोलें।
2. **Transport Type** में `Streamable HTTP` चुनें।
3. **Gateway URL** डालें।
4. Cognito से प्राप्त **Bearer JWT Token** को Authorization हेडर में डालें।
5. `List Tools` पर क्लिक करें। आपको Lambda वाले टूल्स (जैसे `get_weather`, `get_time`) दिखाई देंगे।

---

## 🌐 OpenAPI Target जोड़ना (NASA Mars Weather Example)

वीडियो में NASA की सार्वजनिक **Mars Weather API** को क्रेडेंशियल्स के साथ जोड़कर दिखाया गया है:

### 1. API Key के लिए Credential Provider बनाना:
```python
# API Key को Secrets Manager में सुरक्षित स्टोर करना
credential_provider = client.create_api_credential_provider(
    name="NASA-API-Key",
    api_key="DEMO_KEY" # NASA API key
)
```

### 2. OpenAPI Spec (S3 URI) के साथ Target रजिस्टर करना:
```python
# NASA API के OpenAPI YAML/JSON का S3 पाथ देकर टारगेट बनाना
nasa_target = client.create_gateway_target(
    gateway_name="MyFirstGateway",
    target_type="openapi",
    schema_s3_uri="s3://my-specs-bucket/nasa_mars_spec.yaml",
    credential_provider=credential_provider
)
```
जब आप `List Tools` करेंगे, तो **`get_mars_weather`** टूल आपके गेटवे में अपने आप जुड़ जाएगा और इसके लिए NASA की API Key गेटवे द्वारा ऑटो-इन्जेक्ट की जाएगी।

---

## 🧬 Strands Agent को Gateway से जोड़ना (Code Example)

आप अपने Strands या LangChain एजेंट को इस सिक्योर गेटवे से कनेक्ट कर सकते हैं:

```python
from strands.clients.mcp import McpClient
from strands.clients.mcp.transports import StreamableHttpClientTransport
from strands import Agent

# 1. Secure Transport तैयार करना (Bearer Token के साथ)
transport = StreamableHttpClientTransport(
    url="https://your-gateway-id.agentcore.us-east-1.amazonaws.com",
    headers={"Authorization": "Bearer YOUR_COGNITO_JWT_TOKEN"}
)

# 2. MCP Client बनाना
mcp_client = McpClient(transport=transport)

# 3. Agent बनाना और उसे Gateway के टूल्स सौंपना
agent = Agent(
    model="bedrock/anthropic.claude-3-5-sonnet-v2",
    tools=mcp_client.list_tools() # ये टूल्स गेटवे से आ रहे हैं
)

# 4. रन करना
response = agent.run("What is the current weather on Mars?")
print(response)
```

---

## ❓ FAQ (Frequently Asked Questions)

### Q1. क्या गेटवे का उपयोग करने के लिए केवल Bedrock LLM का उपयोग करना होगा?
**नहीं।** यह एक ओपन और डिकपल्ड (Decoupled) सिस्टम है। आप OpenAI, Gemini, या लोकल Ollama मॉडल्स के साथ भी इस गेटवे का उपयोग कर सकते हैं।

### Q2. क्या गेटवे चलाने की कोई मासिक फिक्स्ड कॉस्ट है?
**नहीं।** गेटवे पूरी तरह **Serverless** है। जब कोई कॉल नहीं आ रही होती, तो इसका खर्च **$0** होता है। आप केवल प्रति रिक्वेस्ट (pay-per-request) भुगतान करते हैं।

### Q3. क्या मैं एक ही Lambda पर अलग-अलग गेटवे के लिए अलग-अलग टूल्स दिखा सकता हूँ?
**हाँ।** आप एक ही Lambda फ़ंक्शन के लिए अलग-अलग OpenAPI/Tool Schemas बनाकर अलग-अलग गेटवे पर अलग-अलग टूल्स एक्सपोज़ कर सकते हैं।
