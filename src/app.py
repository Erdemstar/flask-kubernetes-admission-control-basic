import base64, logging, json
from flask import Flask, request, jsonify

logging.basicConfig(filename="admission_controller.log", level=logging.DEBUG)
app = Flask(__name__)

#Deployment's image tag control
@app.route("/validate", methods=["POST"])
def validate():
    allowed = True
    request_info = request.get_json()

    log(request_info)

    try:
        app.logger.info(request_info)
        for each_image in request_info["request"]["object"]["spec"]["template"]["spec"]["containers"]:
            if "latest" not in each_image["image"]:
                allowed = False
    except KeyError:
        pass
    return jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": allowed,
                "uid": request_info["request"]["uid"],
                "status": {"message": "image is not use latest tag"}
            }
        })

#Deployment name change
@app.route("/mutate", methods=["POST"])
def mutate():
    request_info = request.get_json()
    name = request_info["request"]["object"]["metadata"]["name"]
    operation = [{
        'op': 'replace',
        'path': '/metadata/name',
        'value': 'dummy-prefix' + name
    }]

    patch = base64.b64encode(json.dumps(operation).encode()).decode()

    result = jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": True,
                    "uid": request_info["request"]["uid"],
                    "patch": patch,
                    "patchType": "JSONPatch",
                    "status": {"message": "Namespace is default so it's changed from default to valiation"}
            }
        }
    )

    return result

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

def log(data):
    logging.info("\n")
    logging.info(data)
    logging.info("\n")

if __name__ == "__main__":
    ca_crt = '/etc/ssl/ca.crt'
    ca_key = '/etc/ssl/ca.key'
    app.run(ssl_context=(ca_crt, ca_key), port=443, host='0.0.0.0', debug=True)
