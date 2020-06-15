"""
    This python file will act as mediator or controller for python graphs.
"""
# pylint: disable=E0211
# pylint: disable=E0213
import os
from flask import Flask, request, render_template, jsonify, send_file

from utilities.config import GRAPH_FOLDER
from utilities.covidgraphs import COVIDGraphs
from utilities.datacollection import DataCollection

APP = Flask(__name__, template_folder="frontend")

class COVID:
    """
        This class contains all the methods for plotting the graphs.
    """
    @APP.route("/", methods=["GET"])
    def show_index():
        """
            This will show index page.
        """
        return render_template("index.html")

    @staticmethod
    @APP.after_request
    def add_header(response):
        """
            Add response headers.
        """
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @APP.route("/anuvrat/covid/<filename>", methods=["GET"])
    def send_graph(filename):
        """
            This will return graph file of specified of filename.
        """
        return send_file(os.path.join(GRAPH_FOLDER, filename), as_attachment=True, cache_timeout=0)

    @APP.route("/anuvrat/covid/getstats", methods=["POST"])
    def show_graphs():
        """
            This is entrypoint of API which will send all the graphs.
        """
        data = request.json
        confirm, recover, death = DataCollection().get_data(data)
        files = COVIDGraphs().run_covidgraphs(data, confirm, recover, death)
        return jsonify(files)

if __name__ == "__main__":
    APP.config["CACHE_TYPE"] = "null"
    APP.jinja_env.cache = {}
    APP.run(host="127.0.0.1", port=65000, debug=True)
