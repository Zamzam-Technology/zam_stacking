import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # выполнять откат цепи после завершения каждого теста, чтобы обеспечить надлежащую изоляцию
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def zam(BEP20, accounts):
    zam = BEP20.deploy(100000000 * 10**18, 'Zamzam', 18, 'Zam', {'from': accounts[0]})
    zam.transfer(accounts[1], 20000000 * 10**18, {'from': accounts[0]})
    zam.transfer(accounts[2], 20000000 * 10**18, {'from': accounts[0]})
    return zam


@pytest.fixture(scope="module")
def stacking(ZamStacking, zam, accounts):
    stacking = ZamStacking.deploy({'from': accounts[0]})
    stacking.initialize(accounts[0], accounts[0], zam.address, zam.address, {'from': accounts[0]})
    return (stacking, zam)


@pytest.fixture(scope="module")
def zam_long(BEP20, accounts):
    zam = BEP20.deploy(223401000 * 10**18, 'Zamzam', 18, 'Zam', {'from': accounts[0]})
    zam.transfer(accounts[1], 5000000 * 10**18, {'from': accounts[0]})
    zam.transfer(accounts[2], 14000000 * 10**18, {'from': accounts[0]})
    zam.transfer(accounts[3], 1000 * 10**18, {'from': accounts[0]})
    return zam


@pytest.fixture(scope="module")
def stacking_long(ZamStacking, zam_long, accounts):
    stacking = ZamStacking.deploy({'from': accounts[0]})
    stacking.initialize(accounts[0], accounts[0], zam_long.address, zam_long.address, {'from': accounts[0]})
    return (stacking, zam_long)


@pytest.fixture(scope="module")
def zam_multiple(BEP20, accounts):
    zam = BEP20.deploy(204415000 * 10**18, 'Zamzam', 18, 'Zam', {'from': accounts[0]})

    for i in range(100):
        if ( i + 1 ) > 9:
            accounts.add()
        zam.transfer(accounts[i + 1], (100 + i) * 10**18, {'from': accounts[0]})
        accounts[0].transfer(accounts[i + 1], '0.5 ether')
    return zam


@pytest.fixture(scope="module")
def stacking_multiple(ZamStacking, zam_multiple, accounts):
    stacking = ZamStacking.deploy({'from': accounts[0]})
    stacking.initialize(accounts[0], accounts[0], zam_multiple.address, zam_multiple.address, {'from': accounts[0]})
    return (stacking, zam_multiple)


@pytest.fixture(scope="module")
def stacking_v2(ZamStackingV2, zam, accounts):
    stacking = ZamStackingV2.deploy({'from': accounts[0]})
    stacking.initialize(accounts[0], accounts[0], zam.address, zam.address, {'from': accounts[0]})
    stacking.setFeeReceiver(accounts[3])
    return (stacking, zam)


@pytest.fixture(scope="module")
def stacking_long_v2(ZamStackingV2, zam_long, accounts):
    stacking = ZamStackingV2.deploy({'from': accounts[0]})
    stacking.initialize(accounts[0], accounts[0], zam_long.address, zam_long.address, {'from': accounts[0]})
    stacking.setFeeReceiver(accounts[4])
    return (stacking, zam_long)


@pytest.fixture(scope="module")
def stacking_multiple_v2(ZamStackingV2, zam_multiple, accounts):
    stacking = ZamStackingV2.deploy({'from': accounts[0]})
    stacking.initialize(accounts[0], accounts[0], zam_multiple.address, zam_multiple.address, {'from': accounts[0]})
    stacking.setFeeReceiver(accounts[0])
    return (stacking, zam_multiple)