from brownie import accounts, config, network, MockV3Aggregator

LOCAL_DEV_NETWORKS = ["development", "ganache-local"]

DECIMALS = 8
ETH_TO_USD = 1893.59 * 10 ** DECIMALS


def get_account():
    if network.show_active() not in LOCAL_DEV_NETWORKS:
        account = config["wallets"]["from_key"]
    else:
        account = accounts[0]
    return account


def get_account_2():
    account = accounts[1]
    return account


def get_account_3():
    account = accounts[2]
    return account


def get_price_feed():
    if network.show_active() in LOCAL_DEV_NETWORKS:
        if len(MockV3Aggregator) < 1:
            MockV3Aggregator.deploy(
                DECIMALS,
                ETH_TO_USD,
                {"from": get_account()},
                publish_source=config["networks"][network.show_active()].get("verify"),
            )
        return MockV3Aggregator[-1]
    return config["networks"][network.show_active()].get("eth_to_usd_price_feed")
