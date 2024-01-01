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


# Github Environment:

The Github Actions depend on a few variables. Create a `prod` Github environment and create a secret named `PULUMI_ACCESS_TOKEN`
and store an access token from pulumi.com.

Create a Github Variable named `SSH_PUBLIC_KEY` and `SSH_PUBLIC_KEY_NAME` and insert the SSH public key and the name of 
the public key which matches what you placed in the stack config as `ssh_pubkey_name`.

Required Environment Variables:  
`SSH_PUBLIC_KEY`  SSH public key to be installed into the instance when ran from Github Actions  
`SSH_PUBLIC_KEY_NAME`  File name of the SSH public key for pulumi to look for  
`CF_ZONE_ID` Zone ID from your Cloudflare Site  
`SSH_RECORD_NAME` The SSH DNS record that will be pointed at CF Tunnel -- e.g. `ssh.mysite.com`  
`TUNNEL_NAME` The display name for the cloudflare tunnel  

Required Environment Secrets:  
`CF_TUNNEL_SECRET` A random secret which has been base64 encoded and will be used to create the Cloudflare Tunnel. 

Required Repository Secrets:  
`CF_API_KEY`  Cloudflare Account's Global API Key  
`CF_API_USER`  Cloudflare Account's Email Address  

Required Repository Variables:  
`CF_ACCOUNT_ID` Cloudflare Account ID  

# To run Instance Configuration playbook locally:

Ensure the public IP address has a trailing comma:  

```shell
ansible-playbook ./ansible/playbooks/configure.yml \
--inventory <public_ip>, \
--user <SSH_USERNAME> \
--key-file ~/.ssh/<SSH_PRIVATE_KEY_NAME> \
--verbose \
--extra-vars "CF_TUNNEL_JSON_ENCODED=<CF_TUNNEL_JSON_ENCODED>"
```