// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    address[] private funders;
    mapping(address => uint256) private addressToAmount;
    uint256 private minimum_deposit = 1 * 10**18;

    address private owner = address(0x0);
    AggregatorV3Interface private priceFeed;

    constructor(address _priceFeedAddress) public {
        owner = address(msg.sender);
        funders = new address[](0);
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function fund() public payable {
        require(
            msg.value >= getMinimumDeposit(),
            "Your deposit is below the minimum amount required!"
        );

        addressToAmount[msg.sender] += 0;
        if (addressToAmount[msg.sender] == 0) {
            funders.push(msg.sender);
        }
        addressToAmount[msg.sender] += msg.value;
    }

    function getCurrentPrice() private view returns (uint256) {
        (, int256 _amount, , , ) = priceFeed.latestRoundData();
        return uint256(_amount * 10**10);
    }

    function convertUSDToWei(uint256 _amount) private view returns (uint256) {
        return ((_amount * 10**18 * 10**18) / getCurrentPrice());
    }

    function setMinimumDepositInUSD(uint256 _amount) public onlyOwner {
        minimum_deposit = convertUSDToWei(_amount);
    }

    function getMinimumDeposit() public view returns (uint256) {
        return minimum_deposit;
    }

    function getBalance(address _funder) public view returns (uint256) {
        return addressToAmount[_funder];
    }

    function withdraw() public payable {
        uint256 _amount = msg.value;
        uint256 funder_balance = addressToAmount[msg.sender];
        require(funder_balance > _amount, "You don't have enough balance!");
        addressToAmount[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
    }

    function withdrawAll() public onlyOwner {
        for (uint256 i = 0; i < funders.length; i++) {
            addressToAmount[funders[i]] = 0;
        }
        funders = new address[](0);
        payable(owner).transfer(address(this).balance);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You cannot call this function!");
        _;
    }
}
