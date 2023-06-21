"""
This is a FastAPI module to interface with a json file which stores electrical components
"""
import json
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

FILENAME = "comps.json"

jsonFile = open(FILENAME, encoding="utf-8")
data = json.load(jsonFile)
jsonFile.close()


class Component(BaseModel):
    """
    Component
    """

    cNumber: str
    name: str = "Na"
    catagory: str = "Na"
    price: float = 0.00
    inventory: int = 0
    image: str = "Na"
    parameters: list = []

    async def add_to_file(self):
        """
        This function adds a temp_dictionary containing computer component information to a JSON
        file.
        :return: the instance of the class that called it, which is represented by the `self`
        keyword.
        """
        temp_dict = {
            self.cNumber: {
                "name": self.name,
                "catagory": self.catagory,
                "price": self.price,
                "inventory": self.inventory,
                "image": self.image,
                "parameters": self.parameters,
            }
        }
        write_file = open(FILENAME, mode="w", encoding="utf-8")
        data.update(temp_dict)
        json.dump(data, write_file)
        write_file.close()
        return self


async def get_component_info(comp: Component):
    """
    The `get_component_info` function retrieves information about a component from a website and
    updates a `Component` object with the retrieved data.

    :param comp: A `Component` object that contains information about an electronic component,
    such as its part number, name, category, price, image, and parameters
    :type comp: Component
    :return: The function `get_component_info` returns a `Component` object with updated
    information obtained from a web API.
    """
    respone = requests.get(
        "https://wmsc.lcsc.com/wmsc/product/detail?productCode=" + comp.cNumber,
        timeout=5,
    )
    response_json = json.loads(respone.text)
    comp.name = response_json["result"]["productModel"]
    comp.catagory = response_json["result"]["catalogName"]
    comp.price = response_json["result"]["productPriceList"][0]["productPrice"]
    comp.image = response_json["result"]["productImages"][0]
    param_list = response_json["result"]["paramVOList"]
    for param in param_list:
        comp.parameters.append([param["paramNameEn"], param["paramValueEn"]])
    return comp


async def delete_component(comp: Component):
    """
    This is an asynchronous Python function that deletes a component from a JSON file and returns a
    JSON response with a success or error message.

    :param comp: The parameter `comp` is an object representing a component, which is used to
    identify the component to be deleted from the `data` temp_dictionary. The `cNumber` attribute
    of the `comp` object is used as the key to locate the component in the `data` temp_dictionary
    :return: a JSONResponse object with a status code and a message indicating whether the item was
    successfully deleted or not. If the item is not found, a 404 status code and a "Item not found"
    message are returned. If the item is successfully deleted, a 200 status code and a
    "Item deleted" message are returned.
    """
    if comp.cNumber not in data:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    write_file = open(FILENAME, mode="w", encoding="utf-8")
    del data[comp.cNumber]
    json.dump(data, write_file)
    write_file.close()
    return JSONResponse(status_code=200, content={"message": "Item deleted"})


async def modify_inventory(comp: Component):
    """
    This is an asynchronous Python function that modifies the inventory of a component in a global
    data temp_dictionary and returns a JSON response with the updated component data.

    :param comp: The parameter `comp` is of type `Component`, which is likely a custom class defined
    elsewhere in the code. It is being used to update the inventory of an item in a global
    temp_dictionary called `data`. If the item is not found in the temp_dictionary, a 404 error
    response is returned
    :type comp: Component
    :return: This function returns a JSONResponse object. If the component number is not found in
    the data temp_dictionary, it returns a 404 status code with a message indicating that the item
    was not found. If the component number is found, it updates the inventory value for that
    component and returns a 200 status code with the updated component data.
    """
    if comp.cNumber not in data:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    data[comp.cNumber]["inventory"] = comp.inventory
    return JSONResponse(status_code=200, content=data[comp.cNumber])


app = FastAPI()


@app.get("/allComps")
async def all_comps():
    return data


@app.post("/addComp")
async def add_comp(comp: Component):
    temp = await get_component_info(comp)
    return await temp.add_to_file()


@app.post("/deleteComp")
async def delete_comp(comp: Component):
    return await delete_component(comp)


@app.post("/modifyInv")
async def modify_inv(comp: Component):
    return await modify_inventory(comp)
