# Personal Site IaC

This repo stores the IaC for the Personal Site Repo  

The IaC is split into separate stacks to isolate the OCI organizational resources which do not destroy quickly from the 
computational/network resources for the website which will be brought up and down more frequently.  


Begin by creating a new stack and configuring it with your OCI creds:

```shell
pulumi config set oci:tenancyOcid "ocid1.tenancy.oc1..<unique_ID>" --secret
pulumi config set oci:userOcid "ocid1.user.oc1..<unique_ID>" --secret
pulumi config set oci:fingerprint "<key_fingerprint>" --secret
pulumi config set oci:region "us-ashburn-1"
cat "~/.oci/oci_api_key.pem" | pulumi config set oci:privateKey --secret
```

Next create the compartment to be used for the compute/network infrastructure and set add it to your pulumi config:  
`pulumi config set --secret compartment_ocid "ocid1.compartment.oc1..<unique_ID>`

Adjust some of the stack configs, such as:  
`instance_node_operating_system_ocid`  The OCID to the image to use for the instance. A list is available [here](https://docs.oracle.com/en-us/iaas/images/image/741de11a-777e-4a12-a7b3-b66ea5a13419/).
`availability_domain_number` This will be the AD which has capacity and will be a number most likely between 1-3  
`ssh_pubkey_name`  Name of the SSH public key relative to the `~/.ssh/` directory that will be uploaded to the instance. 


The Github Actions depend on a few variables. Create a `prod` Github environment and create a secret named `PULUMI_ACCESS_TOKEN`
and store an access token from pulumi.com.

Create a Github Variable named `SSH_PUBLIC_KEY` and `SSH_PUBLIC_KEY_NAME` and insert the SSH public key and the name of 
the public key which matches what you placed in the stack config as `ssh_pubkey_name`.  
