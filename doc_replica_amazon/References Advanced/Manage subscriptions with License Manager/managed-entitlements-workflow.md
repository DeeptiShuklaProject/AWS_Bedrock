

# Workflow overview
<a name="managed-entitlements-workflow"></a>

**Step 1 - Subscribe**: Subscribe to a third-party Bedrock serverless model through AWS Marketplace (either via auto-enablement or private offer).

**Step 2 - License creation**: A license is automatically generated in us-east-1, representing your entitlement. You can view this license in the License Manager console under Granted Licenses.

**Steps 3 - Create and distribute grants**: Create grants to distribute the license. Grants can target individual AWS account IDs, your entire organization ID, or specific organizational units (OUs).
+ Individual AWS account IDs - grant appears in recipient's License Manager console
+ Organization ID - grants automatically distributed to all member accounts
+ Organizational units (OUs) - grants distributed to all accounts in the OU

**Step 4 - Activate**: Grants must be activated before the model can be used:
+ Individual grants: Recipient accepts and activates their own grant
+ Organization/OU grants: Management account can bulk-activate all grants, or recipients activate individually

**Step 5 - Use the model**: Once activated, users in the entitled accounts can invoke the model using the Amazon Bedrock console, AWS CLI, or AWS SDKs.