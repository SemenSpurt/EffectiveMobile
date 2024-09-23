import sys
import json
import requests

import unittest
import logging

logger = logging.getLogger()
logger.level = logging.INFO

from dotenv import dotenv_values


config = dotenv_values(".env")

stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class CheckOneProduct(unittest.TestCase):

    def setUp(self):

        data = {'name': config["REPONAME"], 'auto_init': 'true'}

        self.create = requests.post(
            'https://api.github.com/' + 'user/repos', 
            auth=(config["USERNAME"], config["APITOKEN"]), 
            data=json.dumps(data)
        )

        logger.info(self.create)


    def test_check_one_product(self):

        headers={
            "Authorization" : f'token {config["APITOKEN"]}',
            "Accept" : "application/vnd.github+json",
            "X-GitHub-Api-Version" : "2022-11-28"
        }
        
        self.repos = requests.get(
            f'https://api.github.com/users/{config["USERNAME"]}/repos',
            headers=headers
        )

        logger.info(self.repos)

        self.assertTrue(config["REPONAME"] in [each["name"] for each in self.repos.json()], \
            "Name is not in User Repository List")


    def tearDown(self):

        headers = {
            'Authorization': "token " + config["APITOKEN"],
            "X-GitHub-Api-Version" : "2022-11-28"
        }

        self.delete = requests.delete(
            f'https://api.github.com/repos/{config["USERNAME"]}/{config["REPONAME"]}', 
            headers=headers
        )

        logger.info(self.delete)



if __name__ == "__main__":
    unittest.main()