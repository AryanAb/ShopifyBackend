from flask import Flask, render_template, request

app = Flask(__name__)

inventory = {}
bin = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/item', methods=['POST', 'GET', 'PATCH', 'DELETE', 'PUT'])
def item():
    if request.method == 'POST':
        name = request.get_json()['name']
        price = request.get_json()['price']
        if name in inventory:
            return {"status": 400, "error": "An item with the same name already exists in the inventory."}

        inventory[name] = price
        return {"status": 200}

    elif request.method == 'GET':
        name = request.args.get('name')
        if name not in inventory:
            return {"status": 404, "error": "Item not found in inventory."}

        return {"status": 200, "item": {"name": name, "price": inventory[name]}}

    elif request.method == 'PATCH':
        name = request.get_json()['name']
        price = request.get_json()['price']
        if name not in inventory:
            return {"status": 400, "error": "Requested item to be modified does not exist in the inventory."}
        inventory[name] = price
        return {"status": 200, "item": {"name": name, "price": price}}

    elif request.method == 'DELETE':
        name = request.get_json()['name']
        comment = request.get_json()['comment']
        if name not in inventory:
            return {"status": 200, "item": {"name": name, "price": "NA"}}

        price = inventory.pop(name)
        bin[name] = {"price": price, "comment": comment}
        return {"status": 200, "item": {"name": name, "price": price}}

    elif request.method == 'PUT':
        name = request.args.get('name')
        if name not in bin:
            return {"status": 200, "item": {"name": name, "price": "NA", "comment": "NA"}}

        res = bin.pop(name)
        return {"status": 200, "item": {"name": name, "price": res['price'], "comment": res['comment']}}


if __name__ == '__main__':
    app.run(debug=True)
