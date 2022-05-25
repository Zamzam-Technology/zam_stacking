import os, json
from brownie import AdminUpgradeableProxy, ZamStacking, Contract, accounts, convert, interface


def deploy_logic(main_acc):
    stacking = ZamStacking.deploy({'from': main_acc})

    return stacking




def main():
    main_acc = accounts.add(os.getenv('PRIVATE_KEY'))

    admin = '0x7B4c83146A2743bf9204a53BCe1e4DdD87cD1Ca0'
    token = '0xd373576a9e738f37dc6882328358ff69c4caf4c6'

    # logic = deploy_logic(main_acc)
    logic = "0xC883d1F1f0F4656e8966b517aAE6402994590364"
    # abi encoded initialize initialize(main_acc, main_acc, token, token)
    # data = convert.to_bytes('f8c8765e000000000000000000000000a80bb6727bcb8116bbd7355384ed58b59c7b09a70000000000000000000000009633813343e61a70024c266dd8376e2764641711000000000000000000000000bbcf57177d8752b21d080bf30a06ce20ad6333f8000000000000000000000000bbcf57177d8752b21d080bf30a06ce20ad6333f8', 'bytes')
    
    # proxy = AdminUpgradeableProxy.deploy(logic, admin, data, {'from': main_acc})

    proxy_address = "0xDAdB4a98597323C1a33058D6A17f23720ffcC740"

    abi_stake = json.load(open("scripts/ZamStackingABI.json", 'r'))
    stacking = Contract.from_abi("Stacking", proxy_address, abi_stake)
    
    # zam_token = interface.IBEP20(token)

    # zam_token.approve(proxy.address, 10**60, {'from': main_acc})
    

    # stacking.updateStake(506036 * 10**18, 1640109600, False, {'from': main_acc})

    print(stacking.vault())

    # print("Percent 2", stacking.percent())
    # print("S 2", stacking.s())
    # print("Last 2", stacking.lastUpdateTimestamp())
    # print("Stake 2", stacking.totalStake())

    # stacking.deposit(8000000 * 10**18, {'from': main_acc})

    # print("Percent 3", stacking.percent())
    # print("S 3", stacking.s())
    # print("Stake 3", stacking.totalStake())
    # print("Last 3", stacking.lastUpdateTimestamp())

    # stacking.deposit(8000000 * 10**18, {'from': main_acc})
    
    # stacking.deposit(6000000 * 10**18, {'from': main_acc})
    
    # stacking.withdraw(12000000 * 10**18, {'from': main_acc, 'allow_revert': True})

    # print("Percent 5", stacking.percent())
    # print("S 5", stacking.s())
    # print("Stake 5", stacking.totalStake())
    # print("Last 5", stacking.lastUpdateTimestamp())
    # print(stacking.totalStake())
    # print(stacking.lastUpdateTimestamp())

    # print("User", stacking.userInfo(main_acc))