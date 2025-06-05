from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables once for all scripts
load_dotenv()

# RPC endpoint and contract address used across all interactions
RPC_URL = "https://zkrpc.xsollazk.com"
CONTRACT_ADDRESS = "0xC43e8965367D53b83C97E65203EdaB272dFe98CE"

# Initialize Web3 and checksum address
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)


def get_private_key() -> str:
    """Return PRIVATE_KEY from environment or raise an error."""
    pk = os.getenv("PRIVATE_KEY")
    if not pk:
        raise ValueError("PRIVATE_KEY not set in environment")
    return pk


def get_account():
    """Return an Account object using PRIVATE_KEY."""
    return w3.eth.account.from_key(get_private_key())


def get_contract(abi):
    """Instantiate contract with provided ABI."""
    return w3.eth.contract(address=contract_address, abi=abi)


def sign_and_send(tx, private_key: str | None = None):
    """Sign transaction with given key and send to the network."""
    if private_key is None:
        private_key = get_private_key()
    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
    return w3.eth.send_raw_transaction(signed.raw_transaction)
