# AAR1 Firmware

## Development

### General

Some notes about the structure of this repository:

- Python source code should be placed in the directory `src`.
- Documentation should be placed in the directory `docs`.
- Tests should be placed into the directory `test`.
- The `deployment` folder contains an [Ansible](https://www.ansible.com/) playbook which we'll later use to deploy the firmware to the Raspberry Pi.

### Local development

1. Install [VSCode](https://code.visualstudio.com/).
2. Install [Docker](https://docs.docker.com/get-docker/).
3. Install the [VSCode Remote Development Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).
4. Clone this repository to your local machine. `git clone`
5. Open the repository in [the devcontainer](https://code.visualstudio.com/docs/remote/containers).

### Developing on the Raspberry Pi

1. Install [VSCode](https://code.visualstudio.com/).
2. Install the [VSCode Remote Development Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).
3. [Connect to the Raspberry Pi with VSCode Remote](https://code.visualstudio.com/docs/remote/ssh).
4. Clone this repository to the Raspberry Pi. `git clone`
5. Install the [official Python VSCode extension](https://code.visualstudio.com/docs/python/python-tutorial) and start developing!

## Deployment

1. Install [Ansible](https://www.ansible.com/).
2. Create an [inventory file](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) in `deployment/inventory` and addthe IP address of the Raspberry Pi to the `aar1` group.
3. Run `deploy.sh`

> Ansible is pre-installed in the development container!
