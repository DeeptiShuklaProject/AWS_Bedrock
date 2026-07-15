# AWS Bedrock AgentCore Deep Dive: Identity (Hindi Notes 🇮🇳)

यह नोट्स **AWS Show & Tell: Secure your agent workflows using AgentCore Identity** वीडियो पर आधारित हैं। इसे सरल, रोचक और स्पष्ट Hinglish में तैयार किया गया है ताकि शुरुआती डेवलपर्स को AI Agent Security और Identity Management की अवधारणाएं आसानी से समझ आ सकें।

---

## 🔐 AgentCore Identity क्या है? (What is AgentCore Identity?)

**AgentCore Identity** एक स्वतंत्र (Independent) AWS सुरक्षा सेवा है, जो AI Agents के लिए **Zero-Trust Security** मॉडल लागू करती है। 

### ❓ पारंपरिक वर्कलोड (Microservices) बनाम AI Agent में क्या अंतर है?
* **पारंपरिक वर्कलोड:** दो सर्विसेज आपस में जुड़ने के लिए एक स्थायी, हार्डकोडेड ट्रस्ट कनेक्शन का उपयोग करती हैं।
* **AI Agents:** एजेंट्स अत्यधिक गतिशील (Dynamic) और अप्रत्याशित (Unpredictable) होते हैं, क्योंकि वे LLMs (लार्ज लैंग्वेज मॉडल्स) द्वारा संचालित होते हैं। वे अलग-अलग यूजर्स की ओर से अलग-अलग फाइलों और संवेदनशील डेटा (Resources) को एक्सेस करते हैं।

इसलिए हमें **Zero-Trust मॉडल** की आवश्यकता होती है: **"Do not trust hop-to-hop"**। यानी रिक्वेस्ट के हर चरण (hop) पर अपनी पहचान साबित करना अनिवार्य है।

```
[ User ]  ---> Authenticates via Identity Provider (Cognito/Okta)
    |
    v (JWT Token)
[ Application ]  ---> Calls Agent on Runtime
    |
    v (Inbound Auth: User Identity + Agent Identity)
[ Agent Core Identity ] 
    |
    v (Token Vault: Secure Access)
[ External Resources ] (GitHub, Slack, Google Drive)
```

---

## 🛠️ Identity के 4 मुख्य स्तंभ (Four Key Pillars)

AgentCore Identity मुख्य रूप से चार बड़े स्तंभों पर काम करती है:

### 1. Inbound Authorizer (आने वाले कॉल्स की पहचान)
यह एजेंट के पास आने वाली हर रिक्वेस्ट को वेरिफाई करता है।
* यह **Decoupled (स्वतंत्र)** है। आप किसी भी OAuth 2.0 / OIDC प्रोवाइडर (जैसे **Cognito, Microsoft Entra ID, Okta, Auth0, Ping Identity, Cisco Duo**) का उपयोग कर सकते हैं।
* यह आने वाले **JWT (JSON Web Token)** को वैलिडेट करता है।

### 2. Workload Identity (एजेंट की खुद की पहचान)
परम्परागत रूप से, AWS में परमिशन देने के लिए IAM Role का उपयोग होता है, लेकिन कई एजेंट्स एक ही IAM Role शेयर कर सकते हैं, जिससे सुरक्षा कमजोर होती है।
* AgentCore **`Workflow Identity`** (या Workload Identity) नाम का एक अनूठा रिसोर्स बनाता है। 
* यह हर एजेंट को एक **यूनीक और स्टेबल ARN (Amazon Resource Name)** प्रदान करता है।

### 3. Outbound Authorizer & Token Vault (बाहरी रिसोर्सेज की सुरक्षा)
जब एजेंट को किसी यूजर के लिए बाहरी API (जैसे Gmail, GitHub, Salesforce) को एक्सेस करना हो, तो क्रेडेंशियल्स को सुरक्षित रखना सबसे मुश्किल काम होता है।
* **Token Vault** यूजर के टोकन्स और API Keys को सुरक्षित रूप से स्टोर करता है।
* एजेंट का कोड केवल तभी इन टोकन्स को निकाल सकता है जब वह अपनी पहचान (Workload Identity) और यूजर की सहमति (User Context) साबित करे।
* यह मुख्य रूप से 3 प्रकार के फ्लो को सपोर्ट करता है:
  * **Three-Legged OAuth (3LO):** यूजर की सहमति से पर्सनल अकाउंट एक्सेस करना (जैसे: यूजर के Google Drive से फाइलें पढ़ना)।
  * **Machine-to-Machine (M2M / 2LO):** सर्विस-टू-सर्विस ऑथराइजेशन।
  * **API Keys:** थर्ड-पार्टी मॉडल्स या सर्विसेज (जैसे Perplexity, OpenAI) की स्टेटिक कीज़।

### 4. Observability (निगरानी)
* एजेंट ने किस यूजर के लिए, किस समय, किस टूल को एक्सेस किया, यह सब **AWS CloudTrail** में रिकॉर्ड होता है। इसे ऑडिट करना बेहद आसान हो जाता है।

---

## 💡 व्यावहारिक उदाहरण: GitHub Private Repo Listers

मान लीजिए अमित एक डेवलपर है और वह अपनी कंपनी के **"GitAssistant" AI Agent** से पूछता है: *"मेरे कौन-कौन से प्राइवेट गिटहब रिपोजिटरी पर काम चल रहा है, उनकी लिस्ट दिखाओ?"*

#### ❌ बिना AgentCore Identity के (असुरक्षित तरीका):
* GitAssistant एजेंट को अमित के गिटहब अकाउंट का पर्सनल एक्सेस टोकन (PAT) चाहिए होगा। 
* डेवलपर को अमित का टोकन डेटाबेस में स्टोर करना होगा और एजेंट के कोड के भीतर उस टोकन को हैंडल करना होगा। 
* यदि एजेंट के कोड में कोई हैक या सुरक्षा लूप हुआ, तो अमित का टोकन लीक हो सकता है।

#### 🛡️ AgentCore Identity के साथ (सुरक्षित तरीका):
1. **Inbound Login:** अमित सबसे पहले **Cognito** के ज़रिए ऐप में लॉगिन करता है।
2. **First Call:** एजेंट रनटाइम अमित की तरफ से गिटहब को कॉल करने की कोशिश करता है।
3. **Consent URL (3LO Flow):** एजेंट टोकन वॉल्ट को गिटहब एक्सेस टोकन के लिए कहता है। गिटहब वॉल्ट देखता है कि अमित ने अभी तक सहमति नहीं दी है, तो वह एक **User Consent URL** वापस करता है।
4. **सहमति देना:** अमित अपने ब्राउज़र में उस गिटहब यूआरएल को खोलता है और ऐप को एक्सेस की अनुमति देता है।
5. **Secure Storage:** गिटहब अमित का एक्सेस टोकन सीधे **Token Vault** में भेज देता है। एजेंट का कोड अमित का असली पासवर्ड या टोकन कभी नहीं देख पाता। 
6. **Execution:** एजेंट केवल वॉल्ट से गिटहब रिसोर्स की रिक्वेस्ट करता है और वॉल्ट अमित के टोकन का उपयोग करके बैकएंड में लिस्ट प्राप्त कर लेता है।

---

## 💻 Code Snippet 1: Standalone Agent (बिना Runtime/Gateway के चलाना)

यदि आप अपना एजेंट AWS Lambda या Runtime पर होस्ट नहीं कर रहे हैं (जैसे लोकल मशीन या EKS पर चला रहे हैं), तो भी आप AgentCore Identity का standalone उपयोग कर सकते हैं:

```python
from bedrock_agent_core_starter_toolkit import IdentityClient

# 1. Identity Client शुरू करें
identity_client = IdentityClient(region="us-east-1")

# 2. एक स्वतंत्र वर्कलोड आइडेंटिटी (Workload Identity) बनाएं
workload_identity = identity_client.create_workload_identity(
    name="MyLocalResearchAgent"
)
print(f"Agent ARN: {workload_identity.arn}")

# 3. Google Drive (3LO) के लिए रिसोर्स क्रेडेंशियल प्रोवाइडर रजिस्टर करें
credential_provider = identity_client.create_credential_provider(
    name="GoogleDriveProvider",
    provider_vendor="GoogleOAuth2",
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET"
)
```

---

## 💻 Code Snippet 2: 3LO (User Consent) Flow को एजेंट में लागू करना

पायथन एजेंट कोड में यूजर का गिटहब टोकन प्राप्त करने के लिए डेकोरेटर का उपयोग:

```python
from strands.hooks import resource_requests_access_token
from strands import Agent

# GitHub से डेटा लेने के लिए डेकोरेटर
@resource_requests_access_token(
    provider_name="GitHubProvider-Sept16",
    scope="repo:read",                 # केवल रिपोजिटरी पढ़ने का स्कोप
    flow_type="3LO",                   # Three-legged OAuth Flow
    callback_function="on_oauth_url"
)
async def list_github_repos(access_token: str):
    # यह फ़ंक्शन सीधे टोकन प्राप्त करता है और गिटहब API कॉल करता है
    import requests
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get("https://api.github.com/user/repos", headers=headers)
    return response.json()

# ओथ यूआरएल मिलने पर यूजर को ब्राउज़र में रीडायरेक्ट करने के लिए
def on_oauth_url(consent_url: str):
    print(f"कृपया इस यूआरएल पर जाकर अनुमति दें: {consent_url}")
```

---

---

## 📋 Summary of Key Takeaways

| फ़ीचर (Feature) | विवरण (Description) |
| :--- | :--- |
| **Inbound Auth** | किसी भी OAuth IDP (Cognito, Okta, Entra ID) के JWT टोकन्स को वैलिडेट करना। |
| **Workload Identity** | हर एजेंट का अपना यूनीक ARN होना जिससे IAM अनुमतियाँ दी जा सकें। |
| **Token Vault** | थर्ड-पार्टी टोकन्स और API Keys को सुरक्षित रूप से मैनेज करना। |
| **3LO Support** | एंड-यूज़र की अनुमति (User Consent) के बाद ही बाहरी सर्विसेज़ को कॉल करना। |

---

## 💡 व्यावहारिक उदाहरण 2: Research & Save Agent (Google Drive + Perplexity AI)

यह उदाहरण दिखाता है कि कैसे एक एजेंट **Perplexity API** (API Key) का उपयोग करके रिसर्च करता है और परिणाम को यूजर के **Google Drive** (3LO OAuth) में सेव करता है।

```python
import requests
from bedrock_agent_core_starter_toolkit import IdentityClient

# 1. Initialize standalone Identity Client
client = IdentityClient(region="us-east-1")

# 2. Perplexity API Key प्राप्त करना (Token Vault से)
perplexity_provider = "PerplexityKeyProvider"
perplexity_secret = client.get_api_key(
    provider_name=perplexity_provider,
    workload_identity_arn="arn:aws:agentcore:us-east-1:123456789012:workload/ResearchAgent"
)

# 3. Google Drive Access Token प्राप्त करना (3LO Flow)
drive_provider = "GoogleDriveProvider"
drive_token = client.get_outbound_token(
    provider_name=drive_provider,
    user_id="user_amit_123",
    scope="https://www.googleapis.com/auth/drive.file"
)

# 4. Research on Perplexity and Save to Google Drive
def run_research_task(query: str):
    # A. Search using Perplexity
    search_url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {perplexity_secret}"}
    payload = {
        "model": "llama-3-sonar-large-32k-online",
        "messages": [{"role": "user", "content": query}]
    }
    search_response = requests.post(search_url, json=payload, headers=headers).json()
    research_text = search_response['choices'][0]['message']['content']

    # B. Upload report to Google Drive
    upload_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"
    upload_headers = {
        "Authorization": f"Bearer {drive_token}",
        "Content-Type": "text/plain"
    }
    drive_response = requests.post(upload_url, data=research_text, headers=upload_headers)
    
    if drive_response.status_code == 200:
        print("रिसर्च सफलतापूर्वक Google Drive में सेव हो गई है!")
```

---

## ❓ अक्सर पूछे जाने वाले सवाल (Frequently Asked Questions)

### Q1. Workload Identity क्या है और यह पारंपरिक IAM Role से कैसे अलग है?
**उत्तर:** पारंपरिक IAM Role कई अलग-अलग कंप्यूटर या ऐप्स द्वारा शेयर किया जा सकता है। लेकिन **Workload Identity** प्रत्येक विशिष्ट एजेंट/वर्कफ़्लो को एक **यूनीक ARN (Amazon Resource Name)** और पहचान देता है। इससे यह ट्रैक करना आसान हो जाता है कि कौन सा कार्य किस विशिष्ट एजेंट द्वारा किया गया था।

### Q2. Three-Legged OAuth (3LO) और Two-Legged OAuth (2LO) में क्या अंतर है?
**उत्तर:**
* **3LO (Three-Legged):** इसमें तीन पक्ष शामिल होते हैं—यूजर, क्लाइंट ऐप, और डेटा सर्वर। यह तब उपयोग होता है जब एजेंट को यूजर के पर्सनल अकाउंट (जैसे Google Drive, GitHub) को एक्सेस करना हो। इसके लिए यूजर की प्रत्यक्ष ब्राउज़र सहमति (Consent) की आवश्यकता होती है।
* **2LO (Two-Legged / M2M):** इसमें केवल दो पक्ष होते हैं (सिस्टम-टू-सिस्टम)। इसमें यूजर के हस्तक्षेप के बिना दो मशीनें आपस में बात करती हैं।

### Q3. क्या AgentCore Identity का उपयोग करने के लिए AgentCore Runtime का होना ज़रूरी है?
**उत्तर:** **नहीं।** AgentCore Identity एक पूरी तरह से **Standalone** सेवा है। यदि आप अपना एजेंट लोकल कंप्यूटर, ECS, EKS या किसी दूसरे क्लाउड पर भी चला रहे हैं, तो भी आप API का उपयोग करके क्रेडेंशियल्स और टोकन्स को सुरक्षित रख सकते हैं।

### Q4. API Keys को LLM की मेमोरी या एजेंट कोड से बाहर रखने का मुख्य सुरक्षा लाभ क्या है?
**उत्तर:** LLM मॉडल्स कभी-कभी भड़क (hallucinate) सकते हैं या प्रॉम्ट इंजेक्शन (Prompt Injection) हमलों का शिकार हो सकते हैं। यदि सीक्रेट्स सीधे एजेंट कोड या LLM की मेमोरी में स्टोर होंगे, तो वे लीक हो सकते हैं। AgentCore **Token Vault** में सीक्रेट्स को सुरक्षित रखता है और एजेंट को केवल वही अस्थायी टोकन (Access Token) देता है जो आवश्यक हो। इससे मूल API Key कभी भी लीक नहीं होती।

