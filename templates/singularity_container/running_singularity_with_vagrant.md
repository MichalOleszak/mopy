# Running Singularity with Vagrant

Unlike Docker, Singularity containers share the OS kernel with the host, which makes it necessary to build them on a virtual machine when using MacOS. The recommended VM supported by Singularity is Vagrant. [Here are some resources](https://sylabs.io/guides/3.6/admin-guide/installation.html#installation-on-windows-or-mac) on how to install Singularity and Vagrant on MacOS.

1. To initialize the VM and connect to it via SSH, run (from project rootdir):
    ```bash
    mkdir vm-singularity && cd vm-singularity
    vagrant init sylabs/singularity-3.6-ubuntu-bionic64
    vagrant up && vagrant ssh
    ```
2. To build the container on the VM, you will need to copy all the necessary files there. Just run (from the `vm-singularity` dir on host):
    ```bash
    vagrant scp ../pyproject.toml /home/vagrant/
    ```
3. Next, you need to allocate more disk space to the VM (the default 20GB is not enough for the container to build).
   * Edit `vm-singularity/Vagrantfile` on the host to include the following config (memory and cpus are optional, they only impact speed; disksize is required):
       ```bash
     config.vm.provider "virtualbox" do |vb|
          vb.memory = "4096"
          vb.cpus = 8
     end
     config.disksize.size = '50GB'
       ```
   * Run `vagrant halt && vagrant up` to apply the changes.
   * On the guest (inside VM), run `sudo cfdisk /dev/sda`. Use arrows to select sda1. Select 'resize' using arrow keys and accept the suggested disk size. Select write and then quit.
   * Run:
       ```bash
       sudo pvs
       sudo pvresize /dev/sda1
       sudo lvextend -r -l +100%FREE /dev/mapper/vagrant--vg-root
       ```
   * Run `df -h` and verify whether the disk has been resized. It should have ~44GB of free space.

4. To build the container, run (in the VM):
    ```bash
    sudo singularity build pipeline.sif lineage/pipeline/pipeline.def
    ```
5. To copy the Singularity image file from the VM back to the host, run (from host):
    ```bash
    scp -P 2200 vagrant@127.0.0.1:/home/vagrant/pipeline.sif path_on_host
    ```
   If prompted to enter a passoword, type `vagrant`.