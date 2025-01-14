# Copyright Notice:
# Copyright 2017-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md

# Sensors API File

"""
Collection API:  GET
Singleton  API:  GET, POST, PATCH, DELETE
"""

import g
from g import INTERNAL_SERVER_ERROR as INTERNAL_ERROR

import sys, traceback, json
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

members = {}
BNAME = 'Sensors'
INDICES = [1,4]

# Sensors Singleton API
class SensorsAPI(Resource):

    # kwargs is used to pass in the wildcards values to be replaced
    # when an instance is created via get_<resource>_instance().
    #
    # The call to attach the API establishes the contents of kwargs.
    # All subsequent HTTP calls go through __init__.
    #
    # __init__ stores kwargs in wildcards, which is used to pass
    # values to the get_<resource>_instance() call.
    demo_schema = {
        "title": "DemoSchema",
        "type": "object",
        "properties": {
            "AssetTag": {
                "type": "string"
            },
            "SensorsType": {
                "enum": [
                    "Rack",
                    "Blade",
                    "Enclosure",
                    "StandAlone",
                    "RackMount",
                    "Card",
                    "Cartridge",
                    "Row",
                    "Pod",
                    "Expansion",
                    "Sidecar",
                    "Zone",
                    "Sled",
                    "Shelf",
                    "Drawer",
                    "Module",
                    "Component",
                    "IPBasedDrive",
                    "RackGroup",
                    "StorageEnclosure",
                    "ImmersionTank",
                    "HeatExchanger",
                    "PowerStrip",
                    "Other"
                ],
                "type": "string"
            },
        },
        "required": [""]
    }


    def __init__(self, **kwargs):
        logging.info('SensorsAPI init called')
        try:
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()

    # HTTP GET
    def get(self, ident):
        logging.info('SensorsAPI GET called')
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.get_value_from_bucket_hierarchy(bucket_hierarchy, INDICES)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self, ident):
        logging.info('SensorsAPI PUT called')
        return 'PUT is not a supported command for SensorsAPI', 405

    # HTTP POST
    # This is an emulator-only POST command that creates new resource
    # instances from a predefined template. The new instance is given
    # the identifier "ident", which is taken from the end of the URL.
    # PATCH commands can then be used to update the new instance.
    def post(self, ident):
        logging.info('SensorsAPI POST called')
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.post_value_to_bucket_hierarchy(bucket_hierarchy, INDICES, request.json)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info(self.__class__.__name__ + ' PATCH called')
        patch_data = request.get_json(force=True)
        logging.info(f"Payload = {patch_data}")
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.patch_bucket_value(bucket_hierarchy, INDICES, patch_data)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP DELETE
    def delete(self, ident):
        logging.info('SensorsAPI DELETE called')
        try:
            # Find the entry with the correct value for Id
            resp = 404
            if ident in members:
                del(members[ident])
                resp = 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# Sensors Collection API
class SensorsCollectionAPI(Resource):

    def __init__(self):
        logging.info('SensorsCollectionAPI init called')
        self.rb = g.rest_base
        bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            # get list of resources
        passed, output = g.get_collection_from_bucket_hierarchy(bucket_hierarchy)
        self.config = {
            "@odata.id": "/redfish/v1/Chassis/1/Sensors",
            "@odata.type": "#SensorCollection.SensorCollection",
            "@odata.context": "/redfish/v1/$metadata#SensorCollection.SensorCollection",
            "Description": "The collection of Sensor resource instances.",
            "Name": "The collection of Sensor resource instances.",
            "Members": [{'odata.id':x} for x in output],
            "Members@odata.count": len(output)
        }

    # HTTP GET
    def get(self,ident):
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

