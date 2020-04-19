# AAR1 Firmware

## Deployment

1. Install [Ansible](https://www.ansible.com/).
2. Create an [inventory file](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) in `deployment/inventory` and addthe IP address of the Raspberry Pi to the `aar1` group.
3. Run `deploy.sh`