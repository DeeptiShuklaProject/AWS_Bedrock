

# Managing grants
<a name="managed-entitlements-managing"></a>

After creating grants, you may need to modify, deactivate, or delete them based on changing organizational needs.

## Editing grant names
<a name="managed-entitlements-editing-grants"></a>

### Console
<a name="managed-entitlements-editing-grants-console"></a>

You can change the name of a grant to add more detail or improve organization.

**To edit a grant name**

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. In the navigation pane, choose **Granted Licenses**.

1. Choose the license that contains the grant you want to edit.

1. In the **Grants** section, choose the radio button next to the grant.

1. Choose **Edit**.

1. Update the **Grant name** field.

1. Choose **Save changes**.

## Deactivating grants
<a name="managed-entitlements-deactivating-grants"></a>

You may want to temporarily revoke access to a third-party Bedrock model without permanently deleting the grant. Deactivating a grant moves it to a Disabled state.

### Console
<a name="managed-entitlements-deactivating-grants-console"></a>

**To deactivate a grant**

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. In the navigation pane, choose **Granted Licenses**.

1. Choose the license that contains the grant you want to deactivate.

1. In the **Grants** section, choose the grant name.

1. Choose **Deactivate**.

1. Type "deactivate" in the confirmation box.

1. Choose **Deactivate**.

**Important**  
Deactivating a grant does not impact any active workloads or model invocations that are currently running. However, new requests to invoke the model will be denied after deactivation.

## Deleting grants
<a name="managed-entitlements-deleting-grants"></a>

If you want to permanently revoke access to a third-party Bedrock model, you can delete the grant. This action is terminal and cannot be undone.

**To delete a grant**

1. Open the AWS License Manager console at [https://console.aws.amazon.com/license-manager/](https://console.aws.amazon.com/license-manager/).

1. In the navigation pane, choose **Granted Licenses**.

1. Choose the license that contains the grant you want to delete.

1. In the **Grants** section, choose the grant name.

1. Choose **Delete**.

1. Type "delete" in the confirmation box.

1. Choose **Delete**.

Once deleted, the recipient account will no longer be able to activate new instances or invoke the third-party Bedrock model using that grant. Active model invocations will continue to run until completion.

**Note**  
If you delete a grant in error, you can create a new grant to the same account. The new grant will be independent of the deleted grant.

## API
<a name="managed-entitlements-managing-api"></a>

You can deactivate grants using the [CreateGrantVersion API](https://docs.aws.amazon.com/license-manager/latest/APIReference/API_CreateGrantVersion.html) with status set to DISABLED, and delete grants using the [DeleteGrant API.](https://docs.aws.amazon.com/license-manager/latest/APIReference/API_DeleteGrant.html)