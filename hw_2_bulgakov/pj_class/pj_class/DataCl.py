from dataclasses import dataclass


@dataclass
class Probe:
    action: str


@dataclass
class Authenticate:
    account_name: str
    password: str


@dataclass
class AnwClient:
    account_name: str
    status: str


@dataclass
class Responce:
    response: str
    alert: str


@dataclass
class ResponceError:
    response: str
    error: str


@dataclass
class AnwQuit:
    action: str


@dataclass
class Presence:
    account_name: str
    status: str
