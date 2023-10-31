"""Import predefined public networks"""

import os
from django.conf import settings
from django.core.management.base import BaseCommand
from utilities.file import load_json
from api.models import Network


class Command(BaseCommand):
    help = 'Import predefined public networks'

    def handle(self, *args, **kwargs):
        data = load_json(os.path.join(settings.BASE_DIR, 'data', 'networks', 'networks.json'))

        networks = Network.objects.all()

        for n in data:
            found = False
            for network in networks:
                if network.name == n['name']:
                    found = True
                    break
            
            if not found:
                Network.objects.create(name=n['name'], network_id=n['network_id'], chain_id=n['chain_id'], url=n['url'])
                print(f'Created network {n["name"]}')
        print('Done !')