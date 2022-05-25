import brownie

def test_multiple(stacking_multiple_v2, accounts, chain):
    stackingSmart = stacking_multiple_v2[0]
    token = stacking_multiple_v2[1]

    stakingEnd = chain.time() + 5 * 365 * 24 * 3600

    token.approve(stackingSmart.address, 10**60, {'from': accounts[0]})

    stackingSmart.updateStake(506036 * 10**18, stakingEnd, False, {'from': accounts[0]})

    for i in range(100):
        token.approve(stackingSmart.address, 10**60, {'from': accounts[i + 1]})
        stackingSmart.deposit((100 + i) * 10**18, {'from': accounts[i + 1]})

    chain.sleep(6 * 365 * 24 * 3600)
    chain.mine()

    for i in range(100):
        assert stackingSmart.userInfo(accounts[i + 1])[0] == (100 + i) * 10**18
        stackingSmart.withdraw((100 + i) * 10**18, {'from': accounts[i + 1]})
        # print(token.balanceOf(accounts[i + 1]) - (100 + i) * 10**18)

    assert token.balanceOf(stackingSmart.address) > 0 # should be ==