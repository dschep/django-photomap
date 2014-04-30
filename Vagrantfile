# vi: set ft=ruby

$script = <<SCRIPT
apt-get update
apt-get install -y \
    python-virtualenv \
    python-dev \
    postgresql \
    libpq-dev \
    libjpeg-dev \
    libgeos-c1 \
    libgdal-dev \
    postgis \
    postgresql-9.3-postgis-2.1-scripts

sudo -u postgres createdb -O vagrant dcbikelanegraffiti
sudo -u postgres psql dcbikelanegraffiti -c 'create extension postgis;'
sudo -u postgres psql dcbikelanegraffiti -c 'create extension postgis_topology;'

if ! [ -d ~vagrant/venv ] ; then
    sudo -u vagrant virtualenv ~vagrant/venv
fi
sudo -u vagrant ~vagrant/venv/bin/pip install -r /vagrant/requirements.txt

SCRIPT

Vagrant.configure("2") do |config|
    config.vm.box = "trusty64"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    config.vm.network :forwarded_port, guest: 8000, host: 8000

    config.vm.provision :shell, :inline => $script
end
