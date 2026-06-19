

# Create Blueprints for Classification
<a name="idp-cases-classification"></a>

With BDA, you can classify documents by assigning a document class and providing a description when you create a blueprint. The document class serves as a high-level categorization of the document type, while the description provides more granular details about the expected content and elements within that class of documents. We recommend that your description specifies the typical type of data found in the documents along with other relevant information such as purpose of the document and entities expected. 

Examples of document class and their descriptions are:


| Document Class | Description | 
| --- | --- | 
| Invoice | An invoice is a document that contains the list of service rendered or items purchased from a company by a person or another company. It contains details such as when the payment is due and how much is owed. | 
| Payslip | This document issued by an employer to an employee contains wages received by an employee for a given period. It usually contains the breakdown of each of the income and tax deductions items. | 
| Receipts | A document acknowledging that a person has received money or property in payment following a sale or other transfer of goods or provision of a service. All receipts must have the date of purchase on them. | 
| W2 | This is a tax form to file personal income received from an employer in a fiscal year | 

After creating your blueprint fields, follow these steps:

1. On the Create Blueprint page, choose **Save and exit blueprint prompt**.

1. For Blueprint name, enter a name for your blueprint.

1. For Document class, enter a class name that represents the type of document you want to classify.

1. In the Description field, provide a detailed description of the document type. Include information about the type of data and elements commonly found in these documents, such as person, company, addresses, product details, or any other relevant information.

1. Choose Publish blueprint.

After you create the blueprint, you can use it to classify documents during inference by providing one or more blueprint IDs in the InvokeDataAutomationAsync API request.

BDA uses the document class and description provided in each of the blueprints to accurately categorize and process the documents. When you submit a document for processing, BDA analyzes its content and matches it against the list of blueprints provided. The document is then classified and processed based on the blueprint field instructions to produce the output in the desired structure.