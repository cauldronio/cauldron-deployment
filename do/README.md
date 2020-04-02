# Setting up DigitalOcean account

We will be working with this thing DigitalOcean calls [Droplets](https://www.digitalocean.com/products/droplets/).
Things you need to do:
* [Add your SSH key to your account](https://www.digitalocean.com/docs/droplets/how-to/add-ssh-keys/)
* [Create a DigitalOcean Personal Token](https://www.digitalocean.com/docs/api/create-personal-access-token/)

# Setting your local environment and getting remote machinery ready

1. Change your working directory to `cauldron-deployment/do`:
```
cd cauldron-deployment/do
```

2. Export your Personal Token to an environment variable called `DIGITALOCEAN_TOKEN`:
```
export DIGITALOCEAN_TOKEN=<DIGITAL_OCEAN_PERSONAL_TOKEN>
```

3. Export the name given to your SSH key in DigitalOcean to an environment variable called `TF_VAR_default_ssh` ***(Optional)***:
```
export TF_VAR_default_ssh=<DO_SSH_KEY_NAME>
```
**NOTE**: If you want to add more than one SSH key to the provisioning of the machine, you must modify the `cauldron.tf` file to include as many datasources as keys you want to add. These datasources should be added to the `ssh_keys` field of the droplet resource. You must also add as many variables as SSH keys you want to enter, and create the corresponding environment variables.

4. Initialize Terraform:
```
terraform init
```

5. Let's create the droplet:
```
terraform apply
```
During the process, Terraform might ask for confirmation to apply the changes you
have requested. If you want to say `yes` to everything, just run:
```
terraform apply -auto-approve
```
At the end of the process, Terraform outputs the public IP to access to the machine you have created. Something like:
```
digitalocean_droplet.cauldron: Creation complete after 2m2s [id=160048525]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
Outputs:
public_ip = 157.245.85.159
```

6. You are ready for [next steps](../README.md#clone-and-configure).

# Import an existing state

If you use Terraform with already deployed resources, you must first load the status of these resources.

1. Find the ID of your Cauldron droplet:
```
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" "https://api.digitalocean.com/v2/droplets" | json_pp
```

2. Import the droplet state:
```
terraform import digitalocean_droplet.cauldron <DROPLET_ID>
```
If everything goes well, the following message should appear on the terminal:
```
Import successful!
The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
```

# Destroying remote machinery and checking status

1. Change your working directory to `cauldron-deployment/do`:
```
cd cauldron-deployment/do
```

2. Destroy architecture at DigitalOcean:
```
terraform destroy
```

3. If everything goes well, the following message should appear on the terminal:
```
Destroy complete! Resources: 1 destroyed.
```

4. You can also check that the droplet has been deleted by logging into DigitalOcean or through the [API](https://developers.digitalocean.com/documentation/v2/#list-all-droplets):
```
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" "https://api.digitalocean.com/v2/droplets"
```
