import brownie


def test_long_period(stacking_long, accounts, chain):
    stackingSmart = stacking_long[0]
    token = stacking_long[1]

    stackingEnd = chain.time() + 5 * 365 * 24 * 3600

    token.approve(stackingSmart, 10**60, {'from': accounts[0]})
    token.approve(stackingSmart, 10**60, {'from': accounts[1]})
    token.approve(stackingSmart, 10**60, {'from': accounts[2]})
    token.approve(stackingSmart, 10**60, {'from': accounts[3]})

    stackingSmart.updateStake(204400000 * 10**18, stackingEnd, False, {'from': accounts[0]})

    stackingSmart.deposit(5000000 * 10**18, {'from': accounts[1]})
    stackingSmart.deposit(14000000 * 10**18, {'from': accounts[2]})
    stackingSmart.deposit(1000 * 10**18, {'from': accounts[3]})

    assert stackingSmart.percent() == 89000

    chain.sleep(6 * 365 * 24 * 3600)
    chain.mine()

    stackingSmart.withdraw(5000000 * 10**18, {'from': accounts[1]})
    stackingSmart.withdraw(14000000 * 10**18, {'from': accounts[2]})
    stackingSmart.withdraw(1000 * 10**18, {'from': accounts[3]})

    reward_1 = token.balanceOf(accounts[1]) - 5000000 * 10**18
    reward_2 = token.balanceOf(accounts[2]) - 14000000 * 10**18
    reward_3 = token.balanceOf(accounts[3]) - 1000 * 10**18

    assert reward_1 > 0
    assert reward_2 > 0
    assert reward_3 > 0
    assert token.balanceOf(accounts[0]) > 0
    assert token.balanceOf(stackingSmart.address) == 0