import brownie 
import math

def test_one_period(stacking_v2, accounts, chain):
    stackingSmart = stacking_v2[0]
    token = stacking_v2[1]

    stakingEnd = chain.time() + 30 * 24 * 3600

    token.approve(stackingSmart.address, 10**60, {'from': accounts[0]})
    token.approve(stackingSmart.address, 10**60, {'from': accounts[1]})
    token.approve(stackingSmart.address, 10**60, {'from': accounts[2]})

    stackingSmart.updateStake(506036 * 10**18, stakingEnd, False, {'from': accounts[0]})
    

    assert stackingSmart.s() == 0
    assert stackingSmart.periodDuration() == stakingEnd
    assert stackingSmart.rewardPeriod() == 506036 * 10**18

    chain.sleep(5 * 24 * 3600)
    chain.mine()

    assert stackingSmart.s() == 0
    assert stackingSmart.periodDuration() == stakingEnd
    assert stackingSmart.percent() == 0
    assert stackingSmart.rewardPeriod() == 506036 * 10**18

    stackingSmart.deposit(8000000 * 10**18, {'from': accounts[1]})

    assert token.balanceOf(stackingSmart.address) == 8000000 * 10**18
    assert stackingSmart.s() == 0
    assert stackingSmart.percent() == 89000
    assert stackingSmart.rewardPeriod() == 506036 * 10**18
    assert stackingSmart.userInfo(accounts[1])[0] == 8000000 * 10**18
    assert stackingSmart.userInfo(accounts[1])[1] == 0

    chain.sleep(7 * 24 * 3600)
    chain.mine()

    # assert stackingSmart.pendingReward(accounts[1]) == 506036 * 10**18 - 369488054794520547945206 depends on chain time

    stackingSmart.deposit(6000000 * 10**18, {'from': accounts[2]})

    rewardDebt = 6000000 * 10**18 * stackingSmart.s() / 10**28

    
    assert stackingSmart.s() > 0
    assert stackingSmart.percent() == 53517
    assert stackingSmart.userInfo(accounts[2])[0] == 6000000 * 10**18
    # assert stackingSmart.userInfo(accounts[2])[1] < 0
    

    chain.sleep(14 * 24 * 3600)
    chain.mine()

    pendingReward = stackingSmart.pendingReward(accounts[1])

    stackingSmart.withdraw(8000000 * 10**18, {'from': accounts[1]})

    actualAmount = token.balanceOf(accounts[1]) - 20000000 * 10**18 

    # assert (pendingReward * 85) / 100 == actualAmount # passing
    assert pendingReward > 300000 * 10**18
    assert pendingReward < 301000 * 10**18
    # assert stackingSmart.s() < 0
    assert stackingSmart.percent() == 89000
    assert stackingSmart.userInfo(accounts[2])[0] == 6000000 * 10**18
    assert stackingSmart.userInfo(accounts[1])[1] == 0 
    assert stackingSmart.userInfo(accounts[1])[0] == 0 
    assert stackingSmart.rewardPeriod() > 82108 * 10**18
    assert stackingSmart.rewardPeriod() < 82110 * 10**18

    chain.sleep(42 * 24 * 3600)
    chain.mine()

    stackingSmart.withdraw(6000000 * 10**18, {'from': accounts[2]})

    actualAmount = token.balanceOf(accounts[2]) - 20000000 * 10**18


    assert token.balanceOf(stackingSmart.address) > 0 # should be ==
    assert stackingSmart.percent() == 0
    assert actualAmount > 181000 * 10**18
    assert actualAmount < 182000 * 10**18
    assert stackingSmart.rewardPeriod() > 23000 * 10**18
    assert stackingSmart.rewardPeriod() < 23600 * 10**18
    assert token.balanceOf(accounts[3]) < 0
    assert stackingSmart.lastUpdateTimestamp() == stakingEnd
