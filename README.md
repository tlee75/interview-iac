# Personal Site IaC

This repo stores the IaC for the Personal Site Repo  

The IaC is split into separate stacks to isolate the deployment of OCI organizational resources (compartments, etc) which 
are likely to be managed by a shared Organizational team, from the website resources which gives the software team freedom 
to deploy and destroy as needed.  


Begin by creating a new Pulumi stack and configuring it with your OCI creds:

```shell
pulumi config set oci:tenancyOcid "ocid1.tenancy.oc1..<unique_ID>" --secret
pulumi config set oci:userOcid "ocid1.user.oc1..<unique_ID>" --secret
pulumi config set oci:fingerprint "<key_fingerprint>" --secret
pulumi config set oci:region "us-ashburn-1"
cat "~/.oci/oci_api_key.pem" | pulumi config set oci:privateKey --secret
```

Next create an OCI compartment to be used for the compute/network infrastructure and set add it to your pulumi config:  
`pulumi config set --secret compartment_ocid "ocid1.compartment.oc1..<unique_ID>`

Adjust the stack configs, specifically:  
`instance_node_operating_system_ocid`  The OCID of the image to use for the instance. A list is available [here](https://docs.oracle.com/en-us/iaas/images/image/741de11a-777e-4a12-a7b3-b66ea5a13419/).
`availability_domain_number` This will be the AD which has capacity and will be a number most likely between 1-3  
`ssh_pubkey_name`  Name of the SSH public key relative to the `~/.ssh/` directory that will be uploaded to the instance. 


# Github Environment:

The Github Actions depend on a few variables:  

Create a Github Variable named `SSH_PUBLIC_KEY` and `SSH_PUBLIC_KEY_NAME` and insert the SSH public key and the name of 
the public key which matches what you placed in the stack config as `ssh_pubkey_name`.  

Required Environment Variables:  
`SSH_PUBLIC_KEY`  SSH public key to be installed into the instance when ran from Github Actions  
`SSH_PUBLIC_KEY_NAME`  File name of the SSH public key for pulumi to look for  
`SSH_PRIVATE_KEY_NAME` File name of the SSH private key for Ansible to use  
`CF_ZONE_ID` Zone ID from your Cloudflare Site  
`SSH_RECORD_NAME` The SSH DNS record that will be pointed at CF Tunnel -- e.g. `ssh.mysite.com`  
`SITE_URL` The non-www apex domain of your website -- e.g. `mysite.com`  

Required Environment Secrets:  
`CF_TUNNEL_SECRET` Generate with a Password Manager and base64 encode for it to be used when creating the Cloudflare Tunnel.  
`SSH_PRIVATE_KEY`  SSH Private Key contents to be used by Ansible  
`SSH_USERNAME`  SSH Username to be used by Ansible  

Required Repository Secrets:  
`CF_API_KEY`  Cloudflare Account's Global API Key  
`CF_API_USER`  Cloudflare Account's Email Address  
`PULUMI_ACCESS_TOKEN` Access Token from Pulumi  

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
