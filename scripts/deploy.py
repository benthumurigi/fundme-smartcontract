from brownie import config, network, FundMe
from scripts.utils import get_account, get_price_feed


def deploy_fund_me():
    if len(FundMe) > 0:
        fund_me = FundMe[-1]
    else:
        fund_me = FundMe.deploy(
            get_price_feed(),
            {"from": get_account()},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )
    return fund_me


def main():
    deploy_fund_me()
