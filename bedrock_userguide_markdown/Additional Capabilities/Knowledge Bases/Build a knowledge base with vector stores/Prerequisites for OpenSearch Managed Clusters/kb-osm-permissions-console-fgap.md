

# Configuring OpenSearch permissions with fine-grained access control
<a name="kb-osm-permissions-console-fgap"></a>

While optional, we strongly recommend that you enable fine-grained access control for your OpenSearch domain. Using fine-grained access control, you can use role-based access control, which enables you to create an OpenSearch role with specific permissions and map it to the Knowledge Base service role. The mapping grants your knowledge base the minimum required permissions that allows it to access and perform operations on the OpenSearch domain and index.

To configure and use fine-access control:

1. Make sure that the OpenSearch domain that you're using has fine-grained access control enabled.

1. For your domain that uses fine-grained access control, configure permissions with scoped-down policies in the form of an OpenSearch role.

1. For the domain that you create a role for, add a role mapping to the Knowledge Base Service role.

The following steps show how how to configure your OpenSearch role and ensure the correct mapping between the OpenSearch role and the Knowledge Base service role.

**To create an OpenSearch role and configure permissions**  
After you have enabled fine-grained access control and configured Amazon Bedrock to connect to the OpenSearch Service, you can configure permissions using the OpenSearch Dashboards link for each OpenSearch domain.

**To configure permissions for a domain to allow access to Amazon Bedrock:**

1. Open the OpenSearch Dashboard for the OpenSearch domain that you want to work with. To find the link to Dashboards, go to the domain that you created in the OpenSearch Service console. For domains running OpenSearch, the URL is of the format, `{{domain-endpoint}}/_dashboards/`. For more information, see [Dashboards](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/dashboards.html) in the *Amazon OpenSearch Service developer guide*.

1. In the OpenSearch Dashboard, choose **Security** and then choose **Roles**.

1. Choose **Create role**.

1. Provide any name for the role, for example, **kb\_opensearch\_role**.

1. Under **Cluster permissions**, add the following permissions.
   + `indices:data/read/msearch`
   + `indices:data/write/bulk*`
   + `indices:data/read/mget*`

1. Under **Index permissions**, provide a name for the vector index. Choose **Create new permission group**, and then choose **Create new action group**. Add the following permissions to an action group, such as `KnowledgeBasesActionGroup`. Add the following permissions to an action group.
   + `indices:admin/get`
   + `indices:data/read/msearch`
   + `indices:data/read/search`
   + `indices:data/write/index`
   + `indices:data/write/update`
   + `indices:data/write/delete`
   + `indices:data/write/delete/byquery`
   + `indices:data/write/bulk*`
   + `indices:admin/mapping/put`
   + `indices:data/read/mget*`  
![Action groups to create in OpenSearch Dashboards for cluster and index permissions.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/kb-test-os-action-groups.png)

1. Choose **Create** to create the OpenSearch role.

The following shows a sample OpenSearch role with the permissions added.

![A sample OpenSearch role in OpenSearch Dashboards with the permissions added.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/kb/kb-test-os-dashboards-permissions.png)


**To create a role mapping to your Knowledge Base service role**

1. Identify the IAM role that will need to be mapped.
   + If you created your own custom IAM role, you can copy the role ARN for this role from the IAM console.
   + If you are allowing Knowledge Bases to create the role for you, you can make note of the role ARN when creating your knowledge base, and then copy this role ARN.

1. Open the OpenSearch Dashboard for the OpenSearch domain that you want to work with. The URL is of the format, `{{domain-endpoint}}/_dashboards/`.

1. Choose **Security** from the navigation pane.

1. Search for the role that you just created from the list, for example, **kb\_opensearch\_role**, and open it.

1. On the **Mapped Users** tab, choose **Manage mapping**

1. In the **Backend roles** section, enter the ARN of the AWS managed IAM role for Knowledge Bases. Depending on whether you created your own custom role or let Knowledge Bases create the role for you, copy the role ARN information from the IAM console or the Amazon Bedrock console, and then enter that information for the **Backend roles** in the OpenSearch console. Following is an example.

   ```
   arn:aws:iam::{{<accountId>}}:role/service-role/{{<knowledge-base-service-role>}}
   ```

1. Choose **Map**.

   The Knowledge Base Service role can now connect to the OpenSearch role and perform the required operations on the domain and index.