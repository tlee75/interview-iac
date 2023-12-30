# Personal Site IaC

This repo stores the IaC for the Personal Site Repo  

The IaC is split into separate stacks to isolate the OCI organizational resources which do not destroy quickly from the 
computational/network resources for the website which will be brought up and down more frequently.  


First create the compartment to be used for the compute/network infrastructure and set it as an environment variable: `TF_VAR_compartment_ocid`  

Adjust some of the stack configs, such as:  
`instance_node_operating_system_ocid`  The OCID to the image to use for the instance. A list is available [here](https://docs.oracle.com/en-us/iaas/images/image/741de11a-777e-4a12-a7b3-b66ea5a13419/).   
`path_ssh_pubkey` A Local path to a public key to be installed on the instance  
`availability_domain_number` This will be the AD which has capacity and will be a number most likely between 1-3  



The Github Actions depend on a few variables. Create a `prod` Github environment and create a secret named `PULUMI_ACCESS_TOKEN`
and store an access token from pulumi.com.

