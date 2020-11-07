# S.O.I.A.
## Server Orientato all'Integrazione Assistita

S.O.I.A. allows our developers to instantly create a local test instance of the team's LDAP server, complete with fictitious data, in order to test changes to our server infrastructure without breaking production services.

### Test data

The repository already comes with a set of fictitious identities, with five members for every group and five of them being administrators (one for each group). If however you need to generate a fresh dataset, you can do so with `make identities`. This requires:

- `make` - for the command itself
- `Python` - for the scripts that generates the data
- `requests` - for querying [NameFake.com's API](https://namefake.com)
- `PyYAML` - for generating `identities.yml`

The identities are generated from data gathered from [namefake.com](https://namefake.com)

### How to run

Make sure to have Vagrant and Ansible installed and run `make` or `make vm`  
To destroy the VM and remove all unnecessary files (`.vagrant`, downloaded Ansible roles and OpenSSL files) run `make clean`  
To destroy the current VM and recreate it from scratch run `make reinstall`

### Important notes

For various reasons the list of groups in the instant server does not match exactly the list of groups in the real deal. If you notice strange errors that seem to suggest that entire groups or parts of the database are missing, double check that the group you are working with is defined in `ldap_groups` inside `provisioning/elements.yml`. If not, follow these steps to create it:

- add the group to the `ldap_groups` list within `provisioning/elements.yml`
- if you added a thematic group, add it to the `thematic_groups` list at the top of `provisioning/idgen.py`
- if you renamed a group, also rename it within the three variables listed at the top of `provisioning/idgen.py`
- run `make identities` to regenerate the identity list also including the new/changed groups
- run `make reinstall` to recreate the database with the new identities and groups

Please, if you commit to the repository, remember to not commit changes to the group list in the repo unless you know what you're doing.