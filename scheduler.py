#!/usr/bin/env python3

import time
import random
import json
import os
import yaml
import re

from kubernetes import client, config, watch

# Monkey Patch 
from kubernetes.client.models.v1_container_image import V1ContainerImage

def names(self, names):
    self._names = names

V1ContainerImage.names = V1ContainerImage.names.setter(names)
# End Monkey Patch

scheduler_name = os.environ.get('SCHEDULER_NAME','map-scheduler')
namespace = os.environ.get('NAMESPACE','default')

with open('map-scheduler.yaml') as map_scheduler_file:
    mapping = yaml.safe_load(map_scheduler_file)

config.load_incluster_config()
v1 = client.CoreV1Api()

def available_nodes():

    ready_nodes = []

    for n in v1.list_node().items:
        for status in n.status.conditions:
            if status.status == "True" and status.type == "Ready":
                ready_nodes.append(n.metadata.name)

    return ready_nodes


def scheduler(name, node, namespace="default"):
        
    target=client.V1ObjectReference()
    target.kind="Node"
    target.apiVersion="v1"
    target.name=node
    
    meta=client.V1ObjectMeta()
    meta.name=name
    
    body=client.V1Binding(target=target)
    body.metadata=meta
    
    return v1.create_namespaced_binding(namespace, body, _preload_content=False)


def main():

    w = watch.Watch()

    for event in w.stream(v1.list_namespaced_pod, namespace):

        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:

            try:

                for key in mapping:
                    _key = '^'+key+'$'
                    print('Key: ', _key)
                    if re.match(_key, event['object'].metadata.name): break

                preferred_node = mapping.get(key, '')

                if not preferred_node:
                    raise(f"Value {event['object'].metadata.name} is not mapped.")

                if preferred_node not in available_nodes():
                    raise(f'Node {preferred_node} is not available.')

                res = scheduler(event['object'].metadata.name, preferred_node, namespace)

                print(f'Pod {event["object"].metadata.name} was scheduled to node {preferred_nome}')

            except client.rest.ApiException as e:
                print(json.loads(e.body)['message'])

            except Exception as e:
                print(e)
                    
if __name__ == '__main__':
    main()
