import os, json
from brownie import AdminUpgradeableProxy, ZamStacking, ZamStackingV2, Contract, accounts

def deploy_logic(main_acc):
    logic = ZamStackingV2.deploy({'from': main_acc})
    return logic

def main():
    admin_acc = accounts.add(os.getenv('ADMIN_KEY'))
    main_acc = accounts.add(os.getenv('MAIN_KEY'))
    proxy_address = '0xDAdB4a98597323C1a33058D6A17f23720ffcC740'

    logic = deploy_logic(main_acc)

    abi_stake = json.load(open("scripts/ZamStackingABI.json", 'r'))
    stacking = Contract.from_abi("Stacking", proxy_address, abi_stake)

    print("Vault before", stacking.vault())
    print("Percent before", stacking.percent())
    print("S before", stacking.s())
    print("Last before", stacking.lastUpdateTimestamp())
    print("Stake before", stacking.totalStake())
    print("Reward period before", stacking.rewardPeriod())
    print("Duration before", stacking.periodDuration())
    print("Reward claimed before", stacking.rewardClaimed())
    print("User 1 before", stacking.userInfo('0xd50eA49BA6F59496Aa8EB00262AD945b0715d454'))
    print("User 2 before", stacking.userInfo('0x678d47100185b0B879Fa93370591253abC592DA3'))

    proxy = AdminUpgradeableProxy.at(proxy_address)

    proxy.upgradeTo(logic.address, {'from': admin_acc})

    print("Upgraded")

    abi_stake = json.load(open("scripts/ZamStackingV2ABI.json", 'r'))
    stacking = Contract.from_abi("StackingV2", proxy_address, abi_stake)
    stacking.setFeeReceiver('0x4f9C760E30fD99d90E135dd363418aCbC9fE0641', {'from': main_acc})

    print("Vault after", stacking.vault())
    print("Percent after", stacking.percent())
    print("S after", stacking.s())
    print("Last after", stacking.lastUpdateTimestamp())
    print("Stake after", stacking.totalStake())
    print("Reward period after", stacking.rewardPeriod())
    print("Duration after", stacking.periodDuration())
    print("Reward claimed after", stacking.rewardClaimed())
    print("User 1 after", stacking.userInfo('0xd50eA49BA6F59496Aa8EB00262AD945b0715d454'))
    print("User 2 after", stacking.userInfo('0x678d47100185b0B879Fa93370591253abC592DA3'))

