class SmartContract:
    max_compute_gaz = 10_000_000
    max_storage_gas = 20_000
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SmartContract, cls).__new__(cls)
            cls.instance._initialize()
        return cls.instance

    @classmethod
    def get_instance(cls):
        return cls.instance

    def _initialize(self):
        self.storage = dict()
        self.gasStorage = []
        self.gasCompute = []

if __name__ == "__main__":
    sc = SmartContract()
    sc.storage["key"] = "value"
    sc2 = SmartContract.get_instance()
    print(sc.storage["key"])
    print(sc2.storage["key"])
    print(sc == sc2)