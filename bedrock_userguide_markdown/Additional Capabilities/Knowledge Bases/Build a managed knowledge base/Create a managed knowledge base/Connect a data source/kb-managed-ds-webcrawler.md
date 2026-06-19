

# Web Crawler
<a name="kb-managed-ds-webcrawler"></a>

The Web Crawler connects to and crawls URLs you specify for use in your managed knowledge base. The Web Crawler traverses HTML pages starting from your seed URLs, following child links according to your crawl scope and limits. You can also provide sitemap URLs as starting points. The Web Crawler respects robots.txt in accordance with [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html).

**Important**  
When you select websites to crawl, you must adhere to the [Amazon Acceptable Use Policy](https://aws.amazon.com/aup/) and all other Amazon terms. Use the Web Crawler only to index your own web pages, or web pages that you have authorization to crawl.

**Note**  
The Web Crawler does not support document-level access control (ACLs). All indexed content is accessible to any user who has access to the knowledge base. If you need ACL filtering, use a connector that supports it (for example, Amazon S3, SharePoint, or OneDrive).

## Supported features
<a name="kb-managed-supported-features-webcrawler"></a>
+ Crawl multiple seed URLs and sitemap URLs
+ Configurable crawl depth, rate limit, and links-per-URL limit
+ Crawl scope control: same host and path, host only, or host and subdomains
+ URL pattern filters (inclusion and exclusion regular expressions)
+ Crawl attachments linked from web pages (PDFs, documents, and so on)
+ Authentication for protected sites: basic, form-based, or SAML
+ Incremental content syncs for added, updated, and deleted content

## Authentication methods
<a name="kb-managed-webcrawler-auth-methods"></a>

The Web Crawler supports four authentication methods. Choose the method that matches how the target site authenticates users. For public sites with no sign-in, use `NO_AUTH`.


**Web Crawler authentication methods**  

| Method | How it authenticates | When to use | 
| --- | --- | --- | 
| No authentication (NO\_AUTH) | The crawler sends requests without credentials. | Public websites that do not require sign-in. | 
| Basic authentication (BASIC\_AUTH) | The crawler sends an HTTP Authorization: Basic header with a user name and password from your secret. | Sites protected by HTTP Basic Authentication (the browser-style user name and password dialog). | 
| Form authentication (FORM) | The crawler signs in by submitting an HTML form. You provide the login URL, credentials, and XPath expressions that locate the form fields. | Sites that use an HTML form for sign-in. | 
| SAML authentication (SAML) | The crawler signs in through a SAML identity provider's login form. You provide the IdP login URL, credentials, and XPath expressions that locate the form fields. | Sites that use SAML-based single sign-on. | 

## Prerequisites
<a name="kb-managed-prereqs-webcrawler"></a>

**For the website you want to crawl, make sure you**:
+ Have permission to crawl the website and its content.
+ Confirm that `robots.txt` for the site does not disallow the URLs you want to crawl. The Web Crawler defaults to disallow if a `robots.txt` file is not found.
+ If the site requires sign-in, identify the authentication method (basic, form, or SAML). For form and SAML, locate the XPath expressions for the user name field, password field, and submit button on the login page. To find an XPath, right-click the form element in your browser and choose **Inspect**, then copy the XPath from the developer tools.

**In your AWS account, make sure you**:
+ If your site requires authentication, store your credentials in an [AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and note its Amazon Resource Name (ARN). For the exact key-value pairs, see [Authentication credentials](#kb-managed-webcrawler-credentials).
+ Include the necessary permissions to connect to your data source in your AWS Identity and Access Management (IAM) role/permissions policy for your knowledge base. For information on the required permissions, see [Permissions to access your data sources](kb-permissions.md#kb-permissions-access-ds).

## How to set up a Web Crawler data source
<a name="kb-managed-webcrawler-workflow"></a>

Setting up a Web Crawler data source involves the following steps:

1. **(If your site requires sign-in) Prepare credentials.** Store the credentials for your authentication method in an AWS Secrets Manager secret. See [Authentication credentials](#kb-managed-webcrawler-credentials).

1. **Connect the data source.** Create the Web Crawler data source in the knowledge base using the AWS Management Console or the API. See [Create the data source](#kb-managed-ds-webcrawler-create).

## Create the data source
<a name="kb-managed-ds-webcrawler-create"></a>

------
#### [ Console ]

**To connect the Web Crawler to your managed knowledge base**

1. Under **Data source**, provide a name for your data source.

1. Select **Web Crawler** from the data source dropdown.

1. Under **Source**, choose **Source URLs** (up to 10 starting-point URLs) or **Source sitemaps** (up to 3 sitemap URLs).

1. Enter your URLs in the **Add URLs** text area, one per line.

1. Under **Authentication**, select **No authentication**, **Basic authentication**, **Form authentication**, or **SAML authentication**. For any method other than **No authentication**, select or create an AWS Secrets Manager secret to store your credentials.

1. (Optional) Expand **Sync scope** to set the crawl depth (0–10), maximum links per URL (1–1000), maximum URLs crawled per minute (1–300), and the crawl scope: **Default** (same host and same initial URL path as the seed URL), **Host only** (same host, any path), or **Subdomains** (same primary domain, including subdomains).

1. (Optional) Expand **URL filter patterns** to add regular expressions that include or exclude specific URLs.

------
#### [ API ]

To create a Web Crawler data source, send a [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) request with an Agents for Amazon Bedrock build-time endpoint. The following AWS Command Line Interface example creates a data source that crawls a public site without authentication. For a description of each field, see the connector parameters reference that follows.

```
aws bedrock-agent create-data-source \
 --name "{{WebCrawler-connector}}" \
 --knowledge-base-id "{{your-knowledge-base-id}}" \
 --data-source-configuration file://webcrawler-managed-connector.json
```

The `webcrawler-managed-connector.json` file contains the following:

```
{
    "type": "MANAGED_KNOWLEDGE_BASE_CONNECTOR",
    "managedKnowledgeBaseConnectorConfiguration": {
        "connectorParameters": {
            "type": "WEB",
            "version": "1",
            "connectionConfiguration": {
                "seedUrls": [
                    "{{https://docs.example.com}}"
                ],
                "authType": "NO_AUTH"
            },
            "crawlConfiguration": {
                "crawlDepth": 3,
                "maxLinksPerUrl": 100,
                "maxCrawledUrlsPerMinute": 50,
                "syncScope": "SUB_DOMAINS",
                "crawlAttachments": true
            },
            "filterConfiguration": {
                "exclusionPatterns": [
                    "{{https://docs.example.com/private/.*}}"
                ]
            }
        }
    }
}
```

For an authenticated site, set `authType` to `BASIC_AUTH`, `FORM`, or `SAML`, and add a `secretArn` to `connectionConfiguration`.

For managed knowledge bases, `CreateDataSource` is asynchronous: the data source status transitions from `CREATING` to `AVAILABLE` when the operation completes.

------

## Connector parameters
<a name="kb-managed-config-webcrawler"></a>

The data source configuration uses the following connector parameters. To use the Web Crawler, specify `WEB` as the connector type in `connectorParameters`. For the fields that wrap `connectorParameters` (such as `deletionProtectionConfiguration` and `mediaExtractionConfiguration`), see [Connect a data source](kb-managed-connect-ds.md).


**connectionConfiguration**  

| Field | Required | Description | 
| --- | --- | --- | 
| seedUrls | Conditional | List of seed URLs to start crawling from. Maximum of 10. Required unless you provide siteMapUrls. | 
| siteMapUrls | Conditional | List of sitemap URLs. Maximum of 3. Required unless you provide seedUrls. | 
| authType | Yes | The authentication type: NO\_AUTH, BASIC\_AUTH, FORM, or SAML. See [Authentication methods](#kb-managed-webcrawler-auth-methods). | 
| secretArn | Conditional | The ARN of the AWS Secrets Manager secret containing your credentials. Required when authType is not NO\_AUTH. | 


**crawlConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| crawlDepth | No | Maximum crawl depth. Range 0–10. 0 crawls only the specified URLs; higher values follow links deeper into the site. Defaults to 2. | 
| maxLinksPerUrl | No | Maximum links to follow per URL. Range 1–1000. Defaults to 100. | 
| maxCrawledUrlsPerMinute | No | Maximum URLs crawled per minute (rate limit). Range 1–300. | 
| implicitWaitInSeconds | No | Wait time, in seconds, after a page reaches a ready state before the crawler reads it. Increase this for pages with dynamic JavaScript content that loads after the main template. | 
| syncScope | No | The scope of links to follow. One of PATH\_SPECIFIC (same host and same initial URL path as the seed URL), DOMAINS\_ONLY (same host as the seed URL, any path), or SUB\_DOMAINS (same primary domain, including subdomains). When omitted, the crawler crawls only the same host and the same initial URL path as the seed URL. | 
| crawlAttachments | No | Whether to crawl files and attachments linked from web pages (such as PDFs and other documents). | 


**filterConfiguration (optional)**  

| Field | Required | Description | 
| --- | --- | --- | 
| inclusionPatterns | No | List of regular expressions. Only URLs that match at least one pattern are crawled and indexed. | 
| exclusionPatterns | No | List of regular expressions. URLs that match any pattern are not crawled or indexed. | 
| maxFileSizeInMegaBytes | No | Maximum size, in megabytes, of any single file the crawler ingests. Provide as a numeric string (for example, "500"). Defaults to "500". | 

## Authentication credentials
<a name="kb-managed-webcrawler-credentials"></a>

If your website requires authentication, store your credentials in an AWS Secrets Manager secret. The secret format depends on the authentication type you choose.

**Basic authentication (`BASIC_AUTH`)**

```
{
    "userName": "{{your-username}}",
    "password": "{{your-password}}",
    "authentication": "BASIC_AUTH"
}
```

**Form authentication (`FORM`)**

For form-based authentication, provide XPath expressions that identify the user name field, password field, and submit button on the login page.

```
{
    "authentication": "FORM",
    "loginPageUrl": "{{https://example.com/login}}",
    "userName": "{{your-username}}",
    "password": "{{your-password}}",
    "userNameFieldXpath": "{{//input[@name='username']}}",
    "passwordFieldXpath": "{{//input[@name='password']}}",
    "userNameButtonXpath": "{{//button[@type='submit']}}",
    "passwordButtonXpath": "{{//button[@type='submit']}}"
}
```

**SAML authentication (`SAML`)**

For SAML authentication, provide the SAML identity provider's login page URL and XPath expressions for the form fields.

```
{
    "authentication": "SAML",
    "loginPageUrl": "{{https://your-idp.example.com/login}}",
    "userName": "{{your-username}}",
    "password": "{{your-password}}",
    "userNameFieldXpath": "{{//input[@name='username']}}",
    "passwordFieldXpath": "{{//input[@name='password']}}",
    "userNameButtonXpath": "{{//button[@type='submit']}}",
    "passwordButtonXpath": "{{//button[@type='submit']}}"
}
```

**Note**  
To find an XPath in your browser, right-click the form element on the login page and choose **Inspect**. In the developer tools, right-click the highlighted HTML, choose **Copy**, and then choose **Copy XPath**.

## Troubleshooting
<a name="kb-managed-ds-webcrawler-troubleshooting"></a>


**Common Web Crawler issues, causes, and fixes**  

| Symptom | Likely cause | Fix | 
| --- | --- | --- | 
| Sync completes successfully but only the seed URL is indexed. | Site navigation links are wired through JavaScript event handlers (click, scroll, dynamic menus) instead of standard <a href="..."> elements. The crawler renders JavaScript but does not simulate user interactions, so it cannot discover those links. | Provide additional seed URLs for the pages you want to crawl, or provide a sitemap URL that lists every URL to crawl. If content can be exported as files, consider using the Amazon S3 connector instead. | 
| Sync returns no content or fewer pages than expected. | The site's robots.txt file disallows the URLs you want to crawl, or pages have a noindex meta tag. | Update robots.txt for the host so it allows the paths you want crawled, or remove the noindex meta tag from pages you want indexed. Do not block the page in robots.txt if you also want meta tag detection, because the crawler must access the page to read meta tags. | 
| Authentication fails (HTTP 401 or 403, login redirect loop, or session timeout). | Credentials are incorrect or expired, or the XPath expressions do not match the login page elements. | Verify the credentials in your secret. For FORM or SAML auth, validate each XPath in your browser's developer tools, and verify loginPageUrl. | 
| Sync fails with rate limiting (HTTP 429) or incomplete content. | The crawler is fetching pages faster than the site allows. | Lower maxCrawledUrlsPerMinute, or increase implicitWaitInSeconds for sites with dynamic content that loads after the page becomes ready. | 
| Pages are missing because they are larger than expected. | The page or attachment exceeds maxFileSizeInMegaBytes. | Increase maxFileSizeInMegaBytes, or accept that files larger than the limit are not ingested. | 