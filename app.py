from flask import Flask, request, jsonify
from search_filter import search_data, filter_data, sort_data

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search_records():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request must contain JSON data"}), 400

    if "data" not in data:
        return jsonify({"error": "Missing required field: data"}), 400

    try:
        results = data["data"]

        # Search records if a search term was provided.
        results = search_data(results, data.get("search_term", ""))

        # Filter records if filters were provided.
        results = filter_data(results, data.get("filters", {}))

        # Sort records if a sort field was provided.
        sort_by = data.get("sort_by")
        if sort_by:
            order = data.get("order", "ascending")
            results = sort_data(results, sort_by, order)

        return jsonify({
            "results": results,
            "total": len(results)
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

if __name__ == "__main__":
    app.run(port=5001, debug=True)