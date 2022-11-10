import logging
from flask import Flask, request, jsonify

logging.basicConfig(filename='record.log', level=logging.DEBUG)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route("/validate", methods=["POST"])
def validate():
    allowed = True
    request_info = request.get_json()
    try:
        f = open("request.txt", "a")
        f.write(request_info)
    except:
        pass
    try:
        app.logger.info(request_info)
        for each_image in request_info["request"]["object"]["spec"]["template"]["spec"]["containers"]:
            if "latest" not in each_image["image"]:
                allowed = False
    except KeyError:
        pass
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response":
                        {"allowed": allowed,
                         "uid": request_info["request"]["uid"],
                         "status": {"message": "image is not use latest tag"}
                         }
                    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    ca_crt = '/etc/ssl/ca.crt'
    ca_key = '/etc/ssl/ca.key'
    app.run(ssl_context=(ca_crt, ca_key), port=443, host='0.0.0.0', debug=True)
