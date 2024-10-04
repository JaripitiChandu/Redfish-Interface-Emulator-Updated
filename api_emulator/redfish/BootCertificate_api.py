import g
from g import INTERNAL_SERVER_ERROR as INTERNAL_ERROR

import sys, traceback, json
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

members = {}
INDICES = [1]

class BootCertificateCollectionAPI(Resource):

    def __init__(self):
        logging.info('ChassisCollectionAPI init called')
        self.rb = g.rest_base
        bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
        # get list of resources
        passed, output = g.get_collection_from_bucket_hierarchy(bucket_hierarchy)
        self.config = {
            "@odata.id": "/redfish/v1/Systems/WZP27430FB7/Boot/Certificates",
            "@odata.type": "#CertificateCollection.CertificateCollection",
            "@odata.context": "/redfish/v1/$metadata#CertificateCollection.CertificateCollection",
            "Description": "A Collection of Certificate resource instances.",
            "Name": "Certificate Collection",
            "Members": [0],
            "Members@odata.count": 0
        }

    # HTTP GET
    def get(self):
        logging.info('ChassisCollectionAPI GET called')
        try:
            # define the bucket hierarchy for collection
            # bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            # # get list of resources
            # passed, output = g.get_collection_from_bucket_hierarchy(bucket_hierarchy)
            # if not passed:
            #     return output, 404
            # # update the value of config using obtained values
            # self.config["Members"] = [{'@odata.id': x} for x in output]
            # self.config["Members@odata.count"] = len(output)
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        logging.info('ChassisCollectionAPI PUT called')
        return 'PUT is not a supported command for ChassisCollectionAPI', 405

    def verify(self, config):
        #TODO: Implement a method to verify that the POST body is valid
        return True,{}

    # HTTP POST
    def post(self):
        logging.info('ChassisCollectionAPI POST called')
        return 'POST is not a supported command for ChassisCollectionAPI', 405
 
    # HTTP PATCH
    def patch(self):
        logging.info('ChassisCollectionAPI PATCH called')
        return 'PATCH is not a supported command for ChassisCollectionAPI', 405

    # HTTP DELETE
    def delete(self):
        logging.info('ChassisCollectionAPI DELETE called')
        return 'DELETE is not a supported command for ChassisCollectionAPI', 405