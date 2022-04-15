from adapters.cli import create_cli
from composites import loader
from composites.book_api import MessageBus

cli = create_cli(loader, MessageBus.publisher)