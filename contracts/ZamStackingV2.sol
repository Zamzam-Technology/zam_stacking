pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "../interfaces/IBEP20.sol";
import "./TransferHelper.sol";

contract ZamStackingV2 is ReentrancyGuard, Initializable{
    
    event Deposit(address indexed user, uint256 amount);
    event Withdraw(address indexed user, uint256 amount);

    struct UserInfo {
        uint256 amount;
        uint256 rewardDebt; // calculated as amount * s at update moment
    }

    uint256 public s;
    uint256 public percent;
    uint256 public rewardPeriod;
    uint256 public periodDuration;
    uint256 public totalPassedTime;
    uint256 public lastUpdateTimestamp;
    uint256 public totalStake;
    uint256 public rewardClaimed; 
    IBEP20 public stakedToken;
    IBEP20 public rewardToken;

    mapping(address => UserInfo) public userInfo;

    address public owner;

    address public feeReceiver;
    uint256 public fee;

    address public vault;

    uint public PERCENT_DIVISOR;
    uint public S_DIVISOR;
    uint public FEE_DIVISOR;
    uint public SECONDS_IN_YEAR;
    uint public PERCENT_LIMIT;

    mapping(address => uint256) public lastDepositTime;

    modifier onlyOwner() {
        require(owner == msg.sender, "Ownable: caller is not the owner");
        _ ;
    }

    function renounceOwnership() external onlyOwner {
        owner = address(0);
    }

    function transferOwnership(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "Ownable: new owner is the zero address");
        owner = _newOwner;
    }

    function initialize(address _owner, address _vault, 
                            address _stakedToken, address _rewardToken) external initializer {
        owner = _owner;
        s = 0;
        percent = 0;
        rewardPeriod = 0;
        lastUpdateTimestamp = 0;
        totalStake = 0;
        vault = _vault;
        stakedToken = IBEP20(_stakedToken);
        rewardToken = IBEP20(_rewardToken);

        PERCENT_DIVISOR = 10**5;
        S_DIVISOR = 10**24;
        FEE_DIVISOR = 100;
        SECONDS_IN_YEAR = 31536000;
        PERCENT_LIMIT = 89000;
    }

    function pendingReward(address _user) external view returns (uint256) {
        UserInfo memory user = userInfo[_user];

        uint timestamp = min(periodDuration, block.timestamp);
        uint passedTime = timestamp - lastUpdateTimestamp;

        uint temp_s = s + ((percent * passedTime * S_DIVISOR) / PERCENT_DIVISOR) / SECONDS_IN_YEAR;

        return ((user.amount * temp_s) / S_DIVISOR) - user.rewardDebt;
    }


    // _periodDuration - till what time stacking will end (based on unix timestamp)
    function updateStake(uint256 _rewardPeriod, uint256 _periodDuration, bool _beforeSwitch) external onlyOwner {
        if (_beforeSwitch) {
            updatePoolState(totalStake); // do this for right calculation between switching vestings period
        }
        rewardPeriod = rewardPeriod +_rewardPeriod;
        periodDuration = _periodDuration;
        updatePoolState(totalStake);
    }

    
    function updatePoolState(uint _updateStake) internal {
        uint timestamp = min(periodDuration, block.timestamp);
        uint passedTime = timestamp - lastUpdateTimestamp; // passed time from previoud period
        totalPassedTime = block.timestamp; // passed time 

        uint passedReward = 0;

        s += ((percent * passedTime * S_DIVISOR) / PERCENT_DIVISOR) / SECONDS_IN_YEAR;
        passedReward = ((totalStake * percent * passedTime) / PERCENT_DIVISOR) / SECONDS_IN_YEAR;
        rewardPeriod -= passedReward;
        if (_updateStake > 0 && periodDuration > totalPassedTime) {
            percent = ((rewardPeriod * SECONDS_IN_YEAR * PERCENT_DIVISOR) / (periodDuration - totalPassedTime)) / _updateStake;
        } else {
            percent = 0;
        }
        
        if (passedReward > 0) {
            TransferHelper.safeTransferFrom(address(rewardToken), vault, address(this), passedReward);
        }

        if (percent > PERCENT_LIMIT) {
            percent = PERCENT_LIMIT;
        }

        lastUpdateTimestamp = timestamp;
        totalStake = _updateStake;
    }

    function deposit(uint256 _amount) external nonReentrant {
        updatePoolState(totalStake + _amount);

        UserInfo storage user = userInfo[msg.sender];
        if (user.amount > 0) {
            uint256 pending = (user.amount * s) / S_DIVISOR - user.rewardDebt;
            if (pending > 0) {
                transferReward(address(rewardToken), msg.sender, pending, false);
            }
        }
        if (_amount > 0) {
            TransferHelper.safeTransferFrom(address(stakedToken), msg.sender, address(this), _amount);
            user.amount += _amount;
            lastDepositTime[msg.sender] = block.timestamp;
        }

        user.rewardDebt = (user.amount * s) / S_DIVISOR;

        emit Deposit(msg.sender, _amount);
    }

    function withdraw(uint256 _amount) external nonReentrant {
        UserInfo storage user = userInfo[msg.sender];

        require(user.amount >= _amount, "Withdraw: not enough deposit");

        updatePoolState(totalStake - _amount);
        uint256 pending = user.amount * s / S_DIVISOR - user.rewardDebt;
        if (pending > 0) {
            transferReward(address(rewardToken), msg.sender, pending, true);
        }

        if (_amount > 0) {
            user.amount -= _amount;
            TransferHelper.safeTransfer(address(stakedToken), msg.sender, _amount);
        }

        user.rewardDebt = user.amount * s / S_DIVISOR;

        emit Withdraw(msg.sender, _amount);
    }

    function min(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a > b) {
            return b;
        }
            return a;
    }

    function setFeeReceiver(address _feeReceiver) external onlyOwner {
        require(_feeReceiver != address(0), "Fee: receiver can not be zero address");
        feeReceiver = _feeReceiver;
    }

    function setVaultAddress(address _vault) external onlyOwner {
        require(_vault != address(0), "Vault: vault can not be zero address");
        vault = _vault;
    }

    function transferReward(address _token, address _to, uint _amount, bool _checkTime) internal {
        uint fee_transfer = 0;
        if (_checkTime) {
            fee_transfer = _amount * calculateFee(lastDepositTime[_to]) / FEE_DIVISOR;
            if (fee_transfer > 0) {
                TransferHelper.safeTransfer(_token, feeReceiver, fee_transfer);
            }
        }
        TransferHelper.safeTransfer(_token, _to, _amount - fee_transfer);
        rewardClaimed += (_amount - fee_transfer);
    }

    function calculateFee(uint timestamp) view public returns (uint256 _fee) {
        if (timestamp + (2 * 7 * 24 * 3600) > block.timestamp) {
            _fee = 25;
        } else if (timestamp + (4 * 7 * 24 * 3600) > block.timestamp) {
            _fee = 15;
        } else if (timestamp + (6 * 7 * 24 * 3600) > block.timestamp) {
            _fee = 10;
        } else if (timestamp + (8 * 7 * 24 * 3600) > block.timestamp) {
            _fee = 5;
        } else {
            _fee = 0;
        }
    }
}
