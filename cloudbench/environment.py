import ssh

from env.configs.xml_config import EnvXmlConfig
from env.clouds.azure import AzureCloud

class Env(object):
    def config(self):
        pass

    def __init__(self, cloud, f):
        self._cloud = cloud
        self._file  = f
        self._config = None
        self._manager = None
        self._uuid = 'deadbeef' #str(uuid.uuid4())

    def namify(self, obj):
        if obj is None: return None
        return self._uuid + '' + str(obj)


    def config(self):
        if self._config: return self._config
        if '.xml' in self._file:
            self._config = EnvXmlConfig(self._file, self._cloud, self)

        return self._config

    def manager(self):
        if self._manager: return self._manager

        if self._cloud == 'azure':
            self._manager = AzureCloud(self)

        return self._manager

    def address_vm(self, vm):
        return self.manager().address_vm(vm)

    def delete_vm(self, vm):
        return self.manager().delete_vm(vm)

    def delete_vnet(self, vnet):
        return self.manager().delete_vnet(vnet)

    def delete_group(self, group):
        return self.manager().delete_group(group)

    def create_vm(self, vm):
        return self.manager().create_vm(vm)

    def create_vnet(self, vnet):
        return self.manager().create_vnet(vnet)

    def create_group(self, group):
        return self.manager().create_group(group)

    def virtual_machines(self):
        return self.config().virtual_machines().values()

    def virtual_networks(self):
        return self.config().virtual_networks().values()

    def groups(self):
        return self.config().groups().values()

    def vm(self, name):
        vms = self.config().virtual_machines()
        if name in vms:
            return vms[name]
        return None

    def network(self, name):
        vns = self.config().virtual_networks()
        if name in vns:
            return vns[name]
        return None

    def group(self, name):
        groups = self.config().groups()
        if name in groups:
            return groups[name]
        return None

    def setup(self):
        for vm in self.virtual_machines(): vm.create()

    def teardown(self):
        for vm in self.virtual_machines(): vm.delete()
        for vnet in self.virtual_networks(): vnet.delete()
        for group in self.groups(): group.delete()

if __name__ == "__main__":
    from test import run
    import sys

    env = Env('azure', "./benchmarks/fio/config.xml")
    if '-c' in sys.argv: env.setup()
    if '-e' in sys.argv: run(env)
    if '-d' in sys.argv: env.teardown()
