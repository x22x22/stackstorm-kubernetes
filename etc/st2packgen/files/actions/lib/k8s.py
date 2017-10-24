import base64
import json
import requests

from st2actions.runners.pythonrunner import Action


class K8sClient(Action):

    def __init__(self, config=None):

        # args
        # - method
        # - url
        # - headers
        # - body
        # - config_override

        # stuff to be added
        # - auth
        # - config

        super(K8sClient, self).__init__(config=config)

        self.clientcert = 0

        self.myconfig = self.config
        self.req = {'method': '', 'url': '', 'headers': {}, 'data': {}}

    def addArgs(self, **args):

        if "config_override" in args:
            self.overwriteConfig(args['config_override'])
            del(args['config_override'])

        self.req['url'] = self.myconfig['kubernetes_api_url'] + '/' + args['url']
        self.req['method'] = args['method']
        self.req['headers'] = args['headers']
        if 'data' in args:
            self.req['data'] = args['data']
        else:
            self.req['data'] = ''

        for entry in self.myconfig:
            if self.myconfig[entry] == 'None':
                self.myconfig[entry] = None

        if self.myconfig['user'] is not None and self.myconfig['password'] is not None:
            self.addauth()
        elif self.myconfig['cert_path'] is not None:
            self.clientcert = 1
            return True
        else:
            return (False,
                    "Failed finding authentication method\n \
                     Please specify either username and password or clientcert location")

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.myconfig[key] = newconf[key]

    def addauth(self):

        auth = base64.b64encode(self.myconfig['user'] + ":" + self.myconfig['password'])
        self.req['headers'].update({"authorization": "Basic " + auth})
        return True

    def makeRequest(self):

        s = requests.Session()

        if self.clientcert:
            if self.myconfig['cert_key_path'] is not None:
                s.cert = (self.myconfig['cert_path'], self.myconfig['cert_key_path'])
            else:
                s.cert = self.myconfig['cert_path']

        kwargs = {}
        kwargs['url'] = self.req['url']
        kwargs['json'] = self.req['data']
        kwargs['headers'] = self.req['headers']
        kwargs['verify'] = self.myconfig['verify']
        self.resp = getattr(s, self.req['method'])(**kwargs)

if __name__ == "__main__":

    config = {'kubernetes_api_url': "https://master-a.andy.kube",
              'user': 'admin', 'password': 'andypass',
              'template_path': '/opt/stackstorm/packs/kubernetes'}

    body = {
        "kind": "Namespace",
        "apiVersion": "v1",
        "metadata": {"labels": {"project": "andy"}, "name": "new-stg"}
    }

    url = "/api/v1/namespaces"

    header = {'Accept': u'application/json', 'Content-Type': 'application/json'}

    request = {
        "method": "GET",
        "url": url,
        "params": "",
        "data": body,
        "headers": header
    }

    k8s = k8scli(config, request)
    print json.dumps(k8s.makeRequest(), sort_keys=True, indent=2)
