# Before we start

We will create a DNS record using [Gandi](https://www.gandi.net) and its [API](https://api.gandi.net/docs/).
Things you need to do:
* Create an API Key
* Obtain an organizational sharing ID

# Setting your local environment and getting remote machinery ready

1. Change your working directory to `cauldron-deployment/terraform/gandi`:
    ```
    cd cauldron-deployment/terraform/gandi
    ```

2. Export your API Key and your organization sharing ID to two environment variables called `GANDI_KEY` and `GANDI_SHARING_ID`:
    ```
    export GANDI_KEY=<GANDI_API_KEY>
    export GANDI_SHARING_ID=<GANDI_ORGANIZATION_SHARING_ID>
    ```

3. Initialize Terraform:
    ```
    terraform init
    ```

4. Create the record:
    ```
    terraform apply
    ```
    During the process, Terraform might ask for confirmation to apply the changes you
    have requested. If you want to say `yes` to everything, just run:
    ```
    terraform apply -auto-approve
    ```
    At the end of the process, Terraform outputs the record ID of the record you just have created. Something like:
    ```
    record_id = "cauldron.io/botergia/A"
    ```

# Import an existing state

If you use Terraform with already created records, you must first load the status of these resources.

1. Find the ID of your record:
    ```
    curl -X GET https://api.gandi.net/v5/livedns/domains/cauldron.io/records -H "Authorization: Apikey $GANDI_KEY" | json_pp
    ```

2. Import the record state:
    ```
    terraform import gandi_livedns_record.cauldron cauldron.io/<rrset_name>/<rrset_type>
    ```
    If everything goes well, the following message should appear on the terminal:
    ```
    Import successful!

    The resources that were imported are shown above. These resources are now in
    your Terraform state and will henceforth be managed by Terraform.
    ```

# Destroying remote machinery and checking status

1. Change your working directory to `cauldron-deployment/terraform/gandi`:
    ```
    cd cauldron-deployment/terraform/gandi
    ```

2. Destroy record at Gandi:
    ```
    terraform destroy
    ```

3. If everything goes well, the following message should appear on the terminal:
    ```
    Destroy complete! Resources: 1 destroyed.
    ```

4. You can also check that the record has been deleted the [API](https://api.gandi.net/docs/livedns/#v5-livedns-domains-fqdn-records):
    ```
    curl -X GET https://api.gandi.net/v5/livedns/domains/cauldron.io/records -H "Authorization: Apikey $GANDI_KEY" | json_pp
    ```
