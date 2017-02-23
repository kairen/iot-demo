Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.network "public_network", bridge: "en0"
  config.vm.define "tb" do |subconfig|
    subconfig.vm.hostname = "thingsboard.io"
    subconfig.vm.network "private_network", ip: "172.16.35.30",  auto_config: true
    subconfig.vm.provider "virtualbox" do |vm|
        vm.name = "thingsboard.io"
        vm.memory = 2048
        vm.cpus = 1
      end
  end
end
