

# Deleting a Library
<a name="bda-library-deleting"></a>

Use the [DeleteDataAutomationLibrary](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation_DeleteDataAutomationLibrary.html) api to delete library with its entities.

## AWS CLI Example:
<a name="bda-library-deleting-cli"></a>

**Request**

```
aws bedrock-data-automation delete-data-automation-library \
    --library-arn "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary"
```

**Response:**

```
{
  "libraryArn": "arn:aws:bedrock:us-east-1:123456789012:data-automation-library/healthcare-vocabulary",
  "status": "DELETING"
}
```

## AWS Console Example:
<a name="bda-library-deleting-console"></a>

1. Navigate to "Manage libraries" page in BDA Console

1. Choose the desired library from the list of libraries

1. Choose "Delete library"

![Custom vocabulary library details showing Library ID, ARN, status as Active, and creation date.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/library-delete-console.png)


## Important:
<a name="bda-library-deleting-notes"></a>

1. To delete the library, first dissociate the library from the project and then delete the library.

1. You cannot delete a library with an active ingestion job

1. Deletion removes all entities and search indices

1. The operation may take several minutes for large libraries