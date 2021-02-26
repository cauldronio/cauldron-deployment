# Setting up the AWS account

We are going to use [AWS Lightsail](https://aws.amazon.com/lightsail/) instances for this template.
Things you need to do:
* [Add your SSH key to your account](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-how-to-set-up-ssh)
* [Generate the access keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)

# Setting your local environment and getting remote machinery ready

1. Change your working directory to `cauldron-deployment/terraform/aws`:
    ```
    cd cauldron-deployment/terraform/aws
    ```

2. Export your Access Keys and your AWS region to three environment variables:
    ```
    export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
    export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
    export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>
    ```

3. Export the key pair name of the SSH key already uploaded to your AWS account to an environment variable called `TF_VAR_ssh_id`:
    ```
    export TF_VAR_ssh_id=<KEY_PAIR_NAME>
    ```

4. Initialize Terraform:
    ```
    terraform init
    ```

5. Let's create the instances:
    ```
    terraform apply
    ```
    During the process, Terraform might ask for confirmation to apply the changes you
    have requested. If you want to say `yes` to everything, just run:
    ```
    terraform apply -auto-approve
    ```
    At the end of the process, Terraform outputs the public IP to access to the machines you have created. Something like:
    ```
    cauldron_public_ip = 157.245.85.159
    ...
    ```

6. You are ready for [next steps](../../README.md#requirements).

# Import an existing state

If you use Terraform with already deployed resources, you must first load the status of these resources. **Note**: AWS Lightsail only supports to import existing states of instances, not static IPs.

1. Find the name of your Cauldron instances:
    ```
    aws lightsail get-instances
    ```

2. Import the instances state:
    ```
    terraform import aws_lightsail_instance.cauldron <INSTANCE_NAME>
    ...
    ```
    If everything goes well, the following message should appear on the terminal:
    ```
    Import successful!

    The resources that were imported are shown above. These resources are now in
    your Terraform state and will henceforth be managed by Terraform.
    ```

# Destroying remote machinery and checking status

1. Change your working directory to `cauldron-deployment/terraform/aws`:
    ```
    cd cauldron-deployment/terraform/aws
    ```

2. Destroy architecture at AWS Lightsail:
    ```
    terraform destroy
    ```

3. If everything goes well, the following message should appear on the terminal:
    ```
    Destroy complete! Resources: 1 destroyed.
    ```

4. You can also check that the instance has been deleted by logging into AWS or through the AWS CLI:
    ```
    aws lightsail get-instances
    ```
