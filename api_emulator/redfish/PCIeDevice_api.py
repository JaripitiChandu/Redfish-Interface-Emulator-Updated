# Copyright Notice:
# Copyright 2017-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md

# ComputerSystem API File

"""
Collection API:  GET, POST
Singleton  API:  GET, POST, PATCH, DELETE
"""

import sys, traceback
from pprint import pprint
import logging, json
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource
from .ResetActionInfo_api import ResetActionInfo_API
from .ResetAction_api import ResetAction_API

import g
from g import INTERNAL_SERVER_ERROR

members = {}
BNAME = b"PCIeDevices"
INDICES = [1,3]

INTERNAL_ERROR = 500


# Storage Singleton API
class PCIeDeviceAPI(Resource):

    # kwargs is used to pass in the wildcards values to be replaced
    # when an instance is created via get_<resource>_instance().
    #
    # The call to attach the API establishes the contents of kwargs.
    # All subsequent HTTP calls go through __init__.
    #
    # __init__ stores kwargs in wildcards, which is used to pass
    # values to the get_<resource>_instance() call.
    def __init__(self, **kwargs):
        logging.info(f'{self.__class__.__name__} init called')
        try:
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()


    # HTTP GET
    def get(self, ident1, ident2):
        logging.info(self.__class__.__name__ +' GET called')
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.get_value_from_bucket_hierarchy(bucket_hierarchy, INDICES)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_SERVER_ERROR
        return resp


    # HTTP PUT
    def put(self, ident):
        logging.info(self.__class__.__name__ + ' PUT called')
        return f'PUT is not a supported command for {self.__class__.__name__}', 405

    # HTTP POST
    # This is an emulator-only POST command that creates new resource
    # instances from a predefined template. The new instance is given
    # the identifier "ident", which is taken from the end of the URL.
    # PATCH commands can then be used to update the new instance.
    def post(self, ident1, ident2):
        logging.info(self.__class__.__name__ + ' POST called')
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.post_value_to_bucket_hierarchy(bucket_hierarchy, INDICES, request.json)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_SERVER_ERROR
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info(self.__class__.__name__ + ' PATCH called')
        raw_dict = request.get_json(force=True)
        try:
            # Update specific portions of the identified object
            for key, value in raw_dict.items():
                members[ident][key] = value
            resp = members[ident], 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP DELETE
    def delete(self, ident):
        logging.info(self.__class__.__name__ + ' DELETE called')
        try:
            if ident in members:
                del(members[ident])
                resp = 200
            else:
                resp = "Storage" + ident + " not found", 404
        except Exception:
            traceback.print_exc()
            resp = "Internal Server Error", INTERNAL_ERROR
        return resp
class PCIeDeviceCollectionAPI(Resource):
    def __init__(self):
        logging.info('PCIeCollectionAPI init called')
        self.rb = g.rest_base
        bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            # get list of resources
        passed, output = g.get_collection_from_bucket_hierarchy(bucket_hierarchy)
        self.config = {
            "@odata.id": "/redfish/v1/Chassis/1/PCIeDevices",
            "@odata.type": "#PCIeDeviceCollection.PCIeDeviceCollection",
            "@odata.context": "/redfish/v1/$metadata#PCIeDeviceCollection.PCIeDeviceCollection",
            "Description": "Collection of PCIeDevice resource instances for this system",
            "Name": "PCIeDevice Collection",
            "Members": [{'odata.id':x} for x in output],
            "Members@odata.count": len(output)
        }

    # HTTP GET
    def get(self):
        logging.info('SensorsCollectionAPI GET called')
        try:
            # define the bucket hierarchy for collection
            # bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            # # get list of resources
            # passed, output = g.get_collection_from_bucket_hierarchy(bucket_hierarchy)
            # if not passed:
            #     return output, 404
            # update the value of config using obtained values
            # self.config["Members"] = [{'@odata.id': x} for x in output]
            # self.config["Members@odata.count"] = len(output)
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        logging.info('SensorsCollectionAPI PUT called')
        return 'PUT is not a supported command for SensorsCollectionAPI', 405

    def verify(self, config):
        #TODO: Implement a method to verify that the POST body is valid
        return True,{}

    # HTTP POST
    def post(self):
        logging.info('SensorsCollectionAPI POST called')
        return 'POST is not a supported command for SensorsCollectionAPI', 405
 
    # HTTP PATCH
    def patch(self):
        logging.info('SensorsCollectionAPI PATCH called')
        return 'PATCH is not a supported command for SensorsCollectionAPI', 405

    # HTTP DELETE
    def delete(self):
        logging.info('SensorsCollectionAPI DELETE called')
        return 'DELETE is not a supported command for SensorsCollectionAPI', 405