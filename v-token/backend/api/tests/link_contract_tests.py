from django.test import TestCase
from rest_framework import status

# Create your tests here.
from api.models import FTContract, TokenSmartContract
from django.urls import reverse

class LinkContractTestCase(TestCase):
    def setUp(self):
        self.token = 'Bearer'

    def test_link_ft_contract(self):
        contract_1 = FTContract.objects.create(
            token_name='1',
            token_symbol='1',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
        )

        contract_2 = FTContract.objects.create(
            token_name='2',
            token_symbol='2',
            token_standard=TokenSmartContract.FT_STANDARDS.ERC_20,
        )

        url = reverse('token-contract-link-contract', args=[contract_1.id])

        data = {
            'token_type': 'fungible',
            'contracts': [contract_2.id]
        }

        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
