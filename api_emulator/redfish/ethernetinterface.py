# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md

# Redfish Memorys and Memory Resources. Based on version 1.0.0
import g

import sys, traceback
from flask_restful import Resource
import logging
from .templates.ethernetinterface import format_nic_template
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from g import INTERNAL_SERVER_ERROR
members = {}
INTERNAL_ERROR = 500
INDICES=[1,4]

class EthernetInterface(Resource):
    """
    EthernetInterface.v1_3_0.EthernetInterface
    """
    def __init__(self, **kwargs):
        logging.info('EthernetInterfaceAPI init called')
        try:
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()

       # HTTP GET
    def get(self, ident1, ident2):
        logging.info('EthernetInterfaceAPI GET called')
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.get_value_from_bucket_hierarchy(bucket_hierarchy, INDICES)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_SERVER_ERROR
        return resp

    # HTTP PUT
    def put(self,ident1 , ident2):
        logging.info('EthernetInterfaceAPI PUT called')
        return 'PUT is not a supported command for EthernetInterfaceAPI', 405

    # HTTP POST
    def post(self, ident1, ident2):
        logging.info('EthernetInterfaceAPI POST called')
        try:
            bucket_hierarchy = request.path.lstrip(g.rest_base).split('/')
            resp = g.post_value_to_bucket_hierarchy(bucket_hierarchy, INDICES, request.json)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_SERVER_ERROR
        return resp

    # HTTP PATCH
    def patch(self, ident1, ident2):
        logging.info('EthernetInterfaceAPI PATCH called')
        return 'PATCH is not a supported command for EthernetInterfaceAPI', 405

    # HTTP DELETE
    def delete(self, ident1, ident2):
        logging.info('EthernetInterfaceAPI DELETE called')
        return 'DELETE is not a supported command for EthernetInterfaceAPI', 405
    # def __init__(self, **kwargs):
    #     pass

    # def get(self, ident1, ident2):
    #     resp = 404
    #     if ident1 not in members:
    #         return 'not found',404
    #     if ident2 not in members[ident1]:
    #         return 'not found',404
    #     return members[ident1][ident2], 200


class EthernetInterfaceCollection(Resource):
    """
    EthernetInterface.v1_3_0.EthernetInterfaceCollection
    """

    def __init__(self, rb, suffix):
        """
        EthernetInterfaceCollection Constructor
        """
        self.config = {u'@odata.context': '{rb}$metadata#EthernetInterfaceCollection.EthernetInterfaceCollection'.format(rb=rb),
                       u'@odata.id': '{rb}{suffix}'.format(rb=rb, suffix=suffix),
                       u'@odata.type': u'#EthernetInterfaceCollection.EthernetInterfaceCollection'}

    def get(self, ident):
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({'@odata.id': p['@odata.id']})
            self.config['@odata.id']='{prefix}/{ident}/EthernetInterfaces'.format(prefix=self.config['@odata.id'],ident=ident)
            self.config['Members'] = procs
            self.config['Members@odata.count'] = len(procs)
            resp = self.config, 200
        except Exception as e:
            logging.error(e)
            resp = 'internal error', INTERNAL_ERROR
        return resp


def CreateEthernetInterface(**kwargs):
    suffix_id = kwargs['suffix_id']
    nic_id = kwargs['nic_id']
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][nic_id] = format_nic_template(**kwargs)
