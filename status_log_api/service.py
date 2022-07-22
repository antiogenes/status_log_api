#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
from kubernetes.client.rest import ApiException
from kubernetes import client, config
import logging

CONFIG_FILE = "./.kube/config"

config.load_kube_config()


def getStatusJobs(namespace, projeto):
    try:
        if projeto.__contains__('_'):
            projeto = projeto.replace("_", "-")
        pods_names = return_pods_running(namespace, projeto)
        if pods_names == 'Nenhum job do projeto em execução no momento':
            return 'Nenhum job do projeto em execução no momento'
        else:
            api_instance = client.CoreV1Api()
            dict_pods_and_status = {}
            dict_pods_and_status_all = []
            for pod in pods_names:
                api_response = api_instance.read_namespaced_pod_log(name=pod, namespace=namespace) # noqa
                lista = api_response.split(' ')
                for valor in lista:
                    if valor.__contains__('%|'):
                        ultimo_valor = valor
                valor_status = ultimo_valor.split("%")[0].lstrip()
                dict_pods_and_status = ({'nome': pod, 'status': valor_status})
                dict_pods_and_status_all.append(dict_pods_and_status)
            return dict_pods_and_status_all

    except ApiException as err:
        handle_error(err)


def return_pods_running(namespace, projeto):
    try:
        api_instance = client.CoreV1Api()
        api_response = api_instance.list_namespaced_pod(namespace=namespace)
        list_pods_running = []
        list_pods_running_2 = []
        for pods in api_response.items:
            if pods.status.phase == 'Running' and pods.metadata.name.__contains__(projeto): # noqa
                pods_running = pods.metadata.name
                list_pods_running.append(pods_running)
            elif pods.status.phase == 'Running' and pods.metadata.name.__contains__(projeto[:35]): # noqa
                pods_running = pods.metadata.name
                list_pods_running_2.append(pods_running)
        if list_pods_running == [] and list_pods_running_2 == []:
            return 'Nenhum job do projeto em execução no momento'
        else:
            if list_pods_running != []:
                result = re.findall('[eventual-]*'+projeto+'[-]?[0-9]{0,4}[-]?[0-9]{0,2}[-]?[0-9]{0,2}[-]?[0-9]{0,6}[-]?[a-z0-9]{5}', str(list_pods_running)) # noqa
                return result
            else:
                if list_pods_running_2 != []:
                    result = re.findall('[eventual-]*'+projeto[:35]+'[-]?[0-9]{0,4}[-]?[0-9]{0,2}[-]?[0-9]{0,2}[-]?[0-9]{0,6}[-]?[a-z0-9]{5}', str(list_pods_running_2)) # noqa
                    return result

    except ApiException as err:
        handle_error(err)


def handle_error(err):
    logger.error(err)
    os.system("exit(1)")
    raise Exception(0, 'Erro ".')


logger = logging.getLogger(__name__)
