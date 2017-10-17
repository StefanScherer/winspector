import dateutil.parser
import json
import re
import requests
import sys
from requests.exceptions import HTTPError, ConnectTimeout
from os import environ

knownWindowsLayers = {
    "sha256:5847a47b8593f7c39aa5e3db09e50b76d42aa8898c0440c70cc9c69747d4c479": "microsoft/windowsservercore:1709 base",
    "sha256:768182d8a1bb181439f7406a92cfa3d10f2751395fdd954c862ab100f8cde774": "microsoft/windowsservercore:1709_KB4043961",

    "sha256:8df8e568af76c1c311a1251f6f7402e2a09d14629840c97091beb9ba55419464": "microsoft/windowsservercore:10.0.14393.1770 update",
    "sha256:da87b55a9b6358a65462540faeaa97505b0a12e1a2c14f08893589181d32d00d": "microsoft/windowsservercore:10.0.14393.1715 update",
    "sha256:9f5eeabe6154feaf01ca3bf333d9936a1e0803a4998279a74f27e5012605eff4": "microsoft/windowsservercore:10.0.14393.1593 update",
    "sha256:e29afd68a947fc566b71a432a6df352eea9e59eb221c3cb9f6bf5a4df206571e": "microsoft/windowsservercore:10.0.14393.1480 update",
    "sha256:423d66441981dd92835b658b5f8f6e300d5af455e5de3d824889c732b9ea03b5": "microsoft/windowsservercore:10.0.14393.1358 update",
    "sha256:1a106d48ef90b8891090e7d056144d20cfb6672acff25a4d3e27ecb53e04afbc": "microsoft/windowsservercore:10.0.14393.1198 update",
    "sha256:6d4d50238ed13902c153bc3efc3a22f8a96bca4168ea03624d01da1063728dc2": "microsoft/windowsservercore:10.0.14393.1066 update",
    "sha256:503d87f3196a164f17f7b7c68b76271330e21a7e4fbefd1a578b327ed102258e": "microsoft/windowsservercore:10.0.14393.953 update",
    "sha256:3430754e4d171ead00cf6766797a28abf3caf236f6c92c5c346ea2ad3955a129": "microsoft/windowsservercore:10.0.14393.693 update",
    "sha256:04ee5d718c7adc0144556d740900f778129e41be806c95191710d1d92051a7b3": "microsoft/windowsservercore:10.0.14393.576 update",
    "sha256:3889bb8d808bbae6fa5a33e07093e65c31371bcf9e4c38c21be6b9af52ad1548": "microsoft/windowsservercore:10.0.14393.447 full",
    "sha256:d33fff6043a134da85e10360f9932543f1dfc0c3a22e1edd062aa9b088a86c5b": "microsoft/windowsservercore:10.0.14393.447 update",
    "sha256:de5064718b3f2749727c8b5ffddf2da7698189277afe0df6fc0a57ad573bca0f": "microsoft/windowsservercore:10.0.14393.321 update",
    "sha256:9c7f9c7d9bc2915388ecc5d08e89a7583658285469d7325281f95d8ee279cc60": "microsoft/windowsservercore:10.0.14393.206 full",
    "sha256:1239394e5a8ab79fbd3b751dc5d98decf5886f14339958fdf5c1f96c89da58a7": "microsoft/windowsservercore:10.0.14300.1030",

    "sha256:407ada6e90de9752a53cb9f52b7947a0e38a9b21a349970ace15c68890d72511": "microsoft/nanoserver:1709 base",
    "sha256:ad09b0550b6c41c96a80f476f16b2ad5160d9c10545a05a73b8eece84b5d9d49": "microsoft/nanoserver:1709_KB4043961",

    "sha256:b0b5e40cb939a7befa4e01212d6f65f30022bbd04b5f15985b45ce9cfd3fcabc": "microsoft/nanoserver:10.0.14393.1770 update",
    "sha256:5cd49617cf500abea7b9f47d82b70455d816ae6b497cabc1fc86a9522d19a828": "microsoft/nanoserver:10.0.14393.1715 update",
    "sha256:38cc73423ca1d089e2e2374a8baf65d25d3792b22a22263c702f22f85bea6d4c": "microsoft/nanoserver:10.0.14393.1593 update",
    "sha256:baa0507b781fcbf25230671393ddd64a7028872f57c375e758e9d11335cdc4ab": "microsoft/nanoserver:10.0.14393.1480 update",
    "sha256:6330793656b1565cd8b5d5c1e2a736a351dec39f7250daf31eb91e3a76cc872b": "microsoft/nanoserver:10.0.14393.1358 update",
    "sha256:4a8c367fd46d2e2da2a8b0fa02158540e13b3a9015daf9f17d1af354a591492f": "microsoft/nanoserver:10.0.14393.1198 update",
    "sha256:6a43ac69611f40511708beba10dfe6fbe3e266ca933b6fd49c87a9f31f46f46c": "microsoft/nanoserver:10.0.14393.1066 update",
    "sha256:58f68fa0ceda734a980c12dedf782342f892e218bba3c74ded58bfabed652ba1": "microsoft/nanoserver:10.0.14393.953 update",
    "sha256:3ac17e2e6106d09a44642a437c318092eddd284afea0b4e707e89f6cec7a18ef": "microsoft/nanoserver:10.0.14393.693 update",
    "sha256:10bf725c5388a1909f7184467b5ec75dbad3ece68508aa5fa4074baa0b20cc6f": "microsoft/nanoserver:10.0.14393.576 update",
    "sha256:bce2fbc256ea437a87dadac2f69aabd25bed4f56255549090056c1131fad0277": "microsoft/nanoserver:10.0.14393.447 full",
    "sha256:482ab31872a23b32cbdeca13edb7a0b97290714c0b5edcce96fbb3e34221ea91": "microsoft/nanoserver:10.0.14393.447 update",
    "sha256:94b4ce7ac4c7c7d4ed75ac2bd9359a87204ad2d5a909759d8e77953874d8e7c2": "microsoft/nanoserver:10.0.14393.321 update",
    "sha256:5496abde368a3dd39999745bf998c877ddc6a390a943bc3fd99ffaabf728ed88": "microsoft/nanoserver:10.0.14393.206 full",
    "sha256:cf62dbf6d334601f3e026a976218e4d73641ab8c3e66a842a4e4dbdc72768b18": "microsoft/nanoserver:10.0.14300.1030",

    "sha256:3631e6c91d014ec27c8f4911389c8fabe66dd62b2df0d9ceb33388f321e1f061": "microsoft/nanoserver-insider:10.0.16237.1001",
    "sha256:bd0ebd30a0d509ccf4d7ef54855f9468a7207bd63d4350b588ea39ae7402bea5": "microsoft/nanoserver-insider:10.0.16257.1000",
    "sha256:3cda982da924f03f7f053877b8623b1875e156b2e4367b67c97a2d46faf1d31c": "microsoft/nanoserver-insider:10.0.16278.1000",

    "sha256:279070587260c8f3629decdd22e5e8d2cc43456e9a9a15cf40e5ee27ee61de01": "microsoft/nanoserver-insider-powershell:10.0.16237.1001",

    "sha256:dfb9b801c3addce50d23b0bf3c153e604992f9a881097b2bfbb9f9d69fdc23bb": "microsoft/windowsservercore-insider:10.0.16237.1001",
    "sha256:89e73aabab6c8b5247bb20c406c1316cef3fc07445dcd569cfb0d101760f256c": "microsoft/windowsservercore-insider:10.0.16257.1000",
    "sha256:a60e32cc1c9f69e1c3bb5ef1bfdcd5d69ee257cee4b07be2f5815e802444f0c2": "microsoft/windowsservercore-insider:10.0.16278.1000",
}

class DockerImageInspector(object):

    def __init__(self, registry_hostname, repository_name, tag="latest"):
        self.base_url = "https://%s" % registry_hostname
        self.repository_name = repository_name
        self.token = None
        self.tag = tag
        self.create_date = None
        self.create_os = None
        self.create_docker_version = None
        self.create_os_version = ""
        self.layers = []
        self.tags = []
        self.manifest = None
        self.get_tags()
        self.get_manifest()

    def get_tags(self):
        url = "{base_url}/v2/{name}/tags/list".format(
                base_url=self.base_url,
                name=self.repository_name)
        headers = {}
        if self.token is not None:
            headers["Authorization"] = "Bearer %s" % self.token
        r = requests.get(url, headers=headers, timeout=(3.05,10))
        r.raise_for_status()
        self.tags = r.json()["tags"]

    def get_manifest(self):
        url = "{base_url}/v2/{name}/manifests/{reference}".format(
                base_url=self.base_url,
                name=self.repository_name,
                reference=self.tag)
        headers = {}
        if self.token is not None:
            headers["Authorization"] = "Bearer %s" % self.token
        try:
            r = requests.get(url, headers=headers, timeout=(3.05,10))
            r.raise_for_status()
            self.manifest = r.json()
            if environ.get('DEBUG') is not None:
                print(self.manifest)
            if "history" in self.manifest:
                if "v1Compatibility" in self.manifest["history"][0]:
                    hist = json.loads(self.manifest["history"][0]["v1Compatibility"])
                    self.create_date = dateutil.parser.parse(hist["created"])
                    self.create_os = hist["os"]
                    if "os.version" in hist:
                        self.create_os_version = hist["os.version"]
                    self.create_docker_version = hist["docker_version"]
            self.manifest_content_type = r.headers["content-type"]
        except:
            # seems we directly check a Windows base image
            self.manifest = {}
            self.create_os = "windows"
        headers["Accept"] = "application/vnd.docker.distribution.manifest.v2+json"
        r = requests.get(url, headers=headers, timeout=(3.05,10))
        r.raise_for_status()
        manifest = r.json()
        self.manifest["layers"] = manifest["layers"]
        for l in self.manifest["layers"]:
            self.layers.append(l)


class DockerHubImageInspector(DockerImageInspector):

    def __init__(self, repository_name, tag="latest"):
        self.base_url = "https://registry.hub.docker.com"
        self.repository_name = repository_name
        self.__get_token()
        self.tag = tag
        self.layers = []
        self.tags = []
        self.manifest = None
        self.create_os_version = ""
        self.get_tags()
        self.get_manifest()

    def __get_token(self):
        url = "https://auth.docker.io/token"
        params = {
            "service": "registry.docker.io",
            "scope": "repository:{name}:pull".format(
                name=self.repository_name)
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        self.token = r.json()["token"]



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Inspect an image from DockerHub')
    parser.add_argument('image', metavar='IMAGE',
                        help='The image to look for, e.g. "library/redis"')

    args = parser.parse_args()
    if ":" in args.image:
        (image, tag) = args.image.split(":")
    else:
        image = args.image
        tag = "latest"

    image_parts = image.split("/")
    registry = None
    namespace = None
    repository = None
    if len(image_parts) == 3:
        registry = image_parts[-3]
    else:
        registry = "index.docker.io"
    if len(image_parts) >= 2:
        namespace = image_parts[-2]
    else:
        namespace = "library"
    repository = image_parts[-1]

    image = "/".join([registry, namespace, repository])

    try:
        if registry == "index.docker.io":
            dii = DockerHubImageInspector(namespace + "/" + repository, tag)
        else:
            dii = DockerImageInspector(registry, namespace + "/" + repository, tag)
    except HTTPError as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)
    except ConnectTimeout as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write("Unknown error: " + str(e) + "\n")
        sys.exit(3)

    print("Image name: %s" % dii.repository_name)
    print("Tag: %s" % dii.tag)
    print("Number of layers: %d" % len(dii.layers))
    if "schemaVersion" in dii.manifest:
        print("Schema version: %s" % dii.manifest["schemaVersion"])
        print("Architecture: %s" % dii.manifest["architecture"])
        print("Created: %s with Docker %s on %s %s" % (dii.create_date.strftime("%Y-%m-%d %H:%M:%S"), dii.create_docker_version, dii.create_os, dii.create_os_version))
    totalSize=0
    appSize=0
    print("Sizes of layers:")
    for l in dii.layers:
        print("  %s - %s byte" % (l["digest"], l["size"]))
        totalSize += l["size"]
        if l["mediaType"] != "application/vnd.docker.image.rootfs.foreign.diff.tar.gzip":
            appSize += l["size"]
    print("Total size (including Windows base layers): %s byte" % totalSize)
    print("Application size (w/o Windows base layers): %s byte" % appSize)
    print("Windows base image used:")
    if dii.create_os != "windows":
        print("  It does not seem to be a Windows image")
    for l in dii.layers:
        if l["mediaType"] == "application/vnd.docker.image.rootfs.foreign.diff.tar.gzip":
            if l["digest"] in knownWindowsLayers:
                print("  %s" % knownWindowsLayers[l["digest"]])
            else:
                print("  %s - unknown Windows layer" % l["digest"])
    if "history" in dii.manifest:
        print("History:")
        for h in reversed(dii.manifest["history"]):
            hist = json.loads(h["v1Compatibility"])["container_config"]
            if "(nop)" in json.dumps(hist["Cmd"]):
                cmd = hist["Cmd"][-1]
                cmd = re.sub(r".*\(nop\)\s*", "", cmd)
                if "(nop)" in hist["Cmd"][-1]:
                    print("  %s" % cmd)
                else:
                    print("  %s" % cmd)
            else:
                print("  RUN %s" % json.dumps(hist["Cmd"]))
