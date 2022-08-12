from brownie import exceptions, network
from scripts.deploy import deploy_fund_me
from scripts.utils import get_account, get_account_2, get_account_3
import pytest
from web3 import Web3


def test_minimum_deposit():
    fund_me = deploy_fund_me()
    expected_value = 1 * 10 ** 18
    actual_value = fund_me.getMinimumDeposit()
    assert expected_value == actual_value


def test_change_minimum_deposit():
    fund_me = deploy_fund_me()
    fund_me.setMinimumDepositInUSD(50, {"from": get_account()})
    expected_value = 26404871170633558
    actual_value = fund_me.getMinimumDeposit()
    assert expected_value == actual_value


def test_only_owner_can_change_minimum_deposit():
    fund_me = deploy_fund_me()
    if network.show_active() == "development":
        with pytest.raises(exceptions.VirtualMachineError):
            fund_me.setMinimumDepositInUSD(100, {"from": get_account_2()})
    if network.show_active() == "ganache-local":
        with pytest.raises(exceptions.ValueError):
            fund_me.setMinimumDepositInUSD(100, {"from": get_account_2()})
    expected_value = 26404871170633558
    actual_value = fund_me.getMinimumDeposit()
    assert expected_value == actual_value


def test_fund_with_less_amount():
    fund_me = deploy_fund_me()
    fund_me.setMinimumDepositInUSD(50, {"from": get_account()})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.fund({"from": get_account_2(), "value": 26404871170633557})
    expected_value = 0
    actual_value = fund_me.getBalance(get_account_2())
    assert expected_value == actual_value


def test_fund():
    fund_me = deploy_fund_me()
    fund_me.fund({"from": get_account_2(), "value": Web3.toWei(1, "ether")})
    expected_value = 1 * 10 ** 18
    actual_value = fund_me.getBalance(get_account_2())
    assert expected_value == actual_value


def test_only_owner_can_withdraw_all():
    fund_me = deploy_fund_me()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdrawAll({"from": get_account_2()})


def test_get_balance_of_non_funder():
    fund_me = deploy_fund_me()
    expected_value = 0
    actual_value = fund_me.getBalance(get_account_3())
    assert expected_value == actual_value


def test_withdraw():
    fund_me = deploy_fund_me()
    fund_me.fund({"from": get_account_3(), "value": Web3.toWei(1, "ether")})
    fund_me.withdraw({"from": get_account_3(), "value": Web3.toWei(0.5, "ether")})
    expected_value = (1 * 10 ** 18) / 2
    actual_value = fund_me.getBalance(get_account_3())
    assert expected_value == actual_value


def test_withdraw_more_than_account_balance():
    fund_me = deploy_fund_me()
    fund_me.fund({"from": get_account_2(), "value": Web3.toWei(1, "ether")})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": get_account_2(), "value": Web3.toWei(3, "ether")})
    expected_value = 2 * 10 ** 18
    actual_value = fund_me.getBalance(get_account_2())
    assert expected_value == actual_value
