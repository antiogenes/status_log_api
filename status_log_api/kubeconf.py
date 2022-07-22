import os


def create_kube_config(app):
    try:
        certificate = os.environ["certificate_authority_data"]
        server = os.environ["server"]
        namespace = os.environ["current_context"]
        cluster = os.environ["contexts"]
        token = os.environ["k8s_token"]
        user = os.environ["k8s_user"]

        f = open(os.environ["CONFIG_FILE"], "w+")

        conf = """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {0}
    server: {1}
  name: {2}
contexts:
- context:
    cluster: {2}
    namespace: {3}
    user: {4}
  name:  {2}
current-context:  {2}
kind: Config
preferences:
users:
- name:  {4}
  user:
    token: {5}
        """.format(
            certificate, server, cluster, namespace, user, token
        )
        f.write(conf)
        f.close()

    except Exception as identifier:
        print("[ERRO] Erro ao gravar as configuracoes {}", identifier)


def init_app(app):
    create_kube_config(app)
