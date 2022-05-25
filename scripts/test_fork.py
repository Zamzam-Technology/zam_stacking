import os, json
from brownie import AdminUpgradeableProxy, ZamStacking, Contract, accounts, convert, interface


def deploy_logic(main_acc):
    stacking = ZamStacking.deploy({'from': main_acc})

    return stacking




def main():
    main_acc = accounts.add(os.getenv('PRIVATE_KEY'))

    admin = '0x7B4c83146A2743bf9204a53BCe1e4DdD87cD1Ca0'
    token = '0xBbcF57177D8752B21d080bf30a06CE20aD6333F8'

    logic = deploy_logic(main_acc)

    # abi encoded initialize initialize(main_acc, main_acc, token, token)
    data = convert.to_bytes('f8c8765e000000000000000000000000a80bb6727bcb8116bbd7355384ed58b59c7b09a7000000000000000000000000a80bb6727bcb8116bbd7355384ed58b59c7b09a7000000000000000000000000bbcf57177d8752b21d080bf30a06ce20ad6333f8000000000000000000000000bbcf57177d8752b21d080bf30a06ce20ad6333f8', 'bytes')
    
    proxy = AdminUpgradeableProxy.deploy(logic.address, admin, data, {'from': main_acc})

    # proxy_address = "0xAB182786b854308638214dD15a78C1a9C4E42DA5"

    abi_stake = json.load(open("scripts/ZamStackingABI.json", 'r'))
    stacking = Contract.from_abi("Stacking", proxy.address, abi_stake)

    zam_token = interface.IBEP20(token)

    zam_token.approve(proxy.address, 10**60, {'from': main_acc})

    print("Percent 1", stacking.percent())

    stacking.updateStake(506036 * 10**18, 1639755901, False, {'from': main_acc})

    print("Percent 2", stacking.percent())
    print("S 2", stacking.s())
    print("Last 2", stacking.lastUpdateTimestamp())
    print("Stake 2", stacking.totalStake())

    stacking.deposit(8000000 * 10**18, {'from': main_acc})

    print("Percent 3", stacking.percent())
    print("S 3", stacking.s())
    print("Stake 3", stacking.totalStake())
    print("Last 3", stacking.lastUpdateTimestamp())

    stacking.deposit(6000000 * 10**18, {'from': main_acc})

    print("Percent 4", stacking.percent())
    print("S 4", stacking.s())
    print("Stake 4", stacking.totalStake())
    print("Last 4", stacking.lastUpdateTimestamp())