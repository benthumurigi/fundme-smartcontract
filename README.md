# FundMe smart-contract

## Functionalities
1. Users can deposit funds. The minimum amount to be deposited is determined by the address that deployed the smart contract. This may be an admin(Which is not generally a good idea since it doesn't make the application centralised enough) or a DAO

2. People can check what an individual account address has

3. Users, in this case funders (People who have made at least one deposit), can make withdrawals. As long as those withdrawals are below the total amount they have deposited.

4. The holder of the address that deployed this smart contract can withdraw all the money. This is here because there may be a case where the owner, in this case, the address that deployed this smart contract, is a DAO and they may need to use this money for something.

5. The owner can change the minimum deposit amount in USD. This makes it easy instead of trying to figure out how much Eth you'll be asking people to deposit.

More features may be added soon but this was not meant to be serious project.

## How to run it
You need to have brownie and python installed.

Once installed, clone this repository into a folder in your local machine and run

- brownie compile

This compiles the smart-contracts

Then

-brownie test

To run the tests

-brownie run scripts/deploy.py

Deploys the application.

To run the application on a test-net like Rinkeby

make sure you create a .env file and enter your wallet private key into it. Example:

export PRIVATE_KEY=0x123456789123456789123

type everything as is except the part after 0x, that's where you paste your private key.

If you are using Infura or Alchemy, add

export WEB3_INFURA_PROJECT_ID=123

        OR

export WEB3_ALCHEMY_PROJECT_ID=123

respectively

I hope I have covered the important stuff but feel free to ask any questions should you get stuck...of cause after you've googled and tried a couple of solutions first...Have fun.

This project was made using solidity version 0.6.0 and above and python version 3.10.1