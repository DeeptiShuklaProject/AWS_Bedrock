

# Key concepts
<a name="managed-entitlements-key-concepts"></a>

## Account roles
<a name="managed-entitlements-account-roles"></a>

**Grantor or Administrator**: The user who creates the subscription to the third-party Bedrock serverless model through AWS Marketplace. This user receives a license from that subscription and can subsequently grant entitlements to that license to other members of their AWS Organization. For organizations with all features enabled, we highly recommend that you subscribe to the third-party Bedrock model licenses through your management account to take advantage of additional governance mechanisms including auto-acceptance of granted entitlements in linked accounts and the ability to distribute to your AWS Organization ID.

**Grantee or End User**: Accounts that receive the entitlements granted from the Grantor or Administrator. Once granted, licenses can be accepted and activated by end users without them having to explicitly subscribe through AWS Marketplace again.

**Delegated Administrator**: A member account in your organization that has been designated to perform administrative tasks like distributing entitlements. Only one delegated administrator per AWS organization is supported. This account can manage licenses independently from the management account. If you opt to use delegated admin, then you will need the delegated admin to subscribe to the offer initially during Step 1.

## License and grant states
<a name="managed-entitlements-license-grant-states"></a>

Understanding license and grant states helps you track the lifecycle of entitlements in your organization.

### License states
<a name="managed-entitlements-license-states"></a>

**Available**: License is available for use according to the terms of the AWS Marketplace agreement.

**Deleted**: The AWS Marketplace agreement has been cancelled or terminated and the customer no longer has access to that licensed model.

### Grant states
<a name="managed-entitlements-grant-states"></a>

**Pending Acceptance**: Grant has been created and the grantee or end user has not yet accepted it. This state only applies to organizations that do not have all features enabled.

**Disabled**: Grant has been accepted by the end user but not activated for immediate use. Grants in this state cannot be used to invoke third-party Bedrock models.

**Active**: Grant has been accepted and activated successfully. End users can now invoke the third-party Bedrock model.

**Rejected**: End user has rejected the license that was granted to them. This is a terminal state for that grant. The grantor can create a new grant for the end user on the same license.

**Deleted**: Grantor or administrator has deleted the grant. This is a terminal state for that grant. The grantor can create a new grant for the end user on the same license.