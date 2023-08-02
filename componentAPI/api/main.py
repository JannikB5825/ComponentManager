"""
This is a FastAPI module to interface with a json file which stores electrical components
"""
import json
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

FILENAME = "comps.json"
data = {}

try:
    jsonFile = open(FILENAME, encoding="utf-8")
    data = json.load(jsonFile)
    jsonFile.close()
except (FileNotFoundError, json.decoder.JSONDecodeError):
    f = open(FILENAME, "w", encoding="utf-8")
    f.write("{}")
    f.close()


class Component(BaseModel):
    """
    Component
    """

    cNumber: str = "Na"
    name: str = "Na"
    catagory: str = "Na"
    catagoryID: int = 0
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
                "catagoryID": self.catagoryID,
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
    if response_json["result"] is None:
        comp.name = "Fail"
        return comp
    comp.name = response_json["result"]["productModel"]
    comp.catagory = response_json["result"]["catalogName"]
    comp.catagoryID = response_json["result"]["catalogId"]
    comp.price = response_json["result"]["productPriceList"][0]["productPrice"]
    try:
        comp.image = response_json["result"]["productImages"][0]
    except IndexError:
        comp.image = "https://placehold.co/400"
    param_list = response_json["result"]["paramVOList"]
    if param_list is not None:
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


async def get_catagory_comps(comp: Component):
    """
    The function `get_catagory_comps` retrieves components from a specific category using an API
    endpoint and returns them as a dictionary.
    
    :param comp: The parameter `comp` is of type `Component`. It represents a specific component for
    which we want to retrieve the category components
    :type comp: Component
    :return: a dictionary containing components that belong to the same category as the input
    component.
    """
    respone = requests.get(
        "https://wmsc.lcsc.com/wmsc/product/catalog/menu/onelevel?catalogId="
        + str(comp.catagoryID),
        timeout=5,
    )
    response_json = json.loads(respone.text)
    if response_json["result"] is None:
        return JSONResponse(status_code=404, content={"message": "Catagory not found"})
    return_dict = {}
    for component in data:
        if data[component]["catagoryID"] == comp.catagoryID:
            return_dict[component] = data[component]["name"]
    return return_dict



async def get_all_catagorys():
    """
    The function `get_all_catagorys` returns a dictionary with the count of each category ID in the
    `data` variable.
    :return: a dictionary that contains the count of each category ID in the "data" variable.
    """
    return_dict = {}
    for comp in data:
        if data[comp]["catagory"] not in return_dict:
            return_dict[data[comp]["catagory"]] = 1
        else:
            return_dict[data[comp]["catagory"]] += 1
    return return_dict


app = FastAPI()


@app.get("/allComps")
async def all_comps():
    """
    The function `all_comps` returns the variable `data`.
    :return: The function `all_comps()` is returning the variable `data`.
    """
    return data

@app.post("/getComp")
async def get_comp(comp: Component):
    """
    The function `get_comp` retrieves information about a component and returns it, or returns a 404
    error if the component is not found.
    
    :param comp: The parameter `comp` is of type `Component`
    :type comp: Component
    :return: a JSONResponse object.
    """
    temp_comp = await get_component_info(comp)
    if temp_comp.name == "Fail":
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return temp_comp


@app.post("/addComp")
async def add_comp(comp: Component):
    """
    The function `add_comp` adds a component to a file after checking if it exists and returning an
    error message if it doesn't.
    
    :param comp: The parameter `comp` is of type `Component`
    :type comp: Component
    :return: If the query_comp.name is "Fail", then a JSONResponse with a status code of 404 and a
    content message of "Item not found" is returned. Otherwise, the result of the
    query_comp.add_to_file() function is returned.
    """
    query_comp = await get_component_info(comp)
    if query_comp.name == "Fail":
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return await query_comp.add_to_file()


@app.post("/deleteComp")
async def delete_comp(comp: Component):
    """
    The function `delete_comp` deletes a component asynchronously.
    
    :param comp: The parameter `comp` is of type `Component`
    :type comp: Component
    :return: the result of the `delete_component` function, which is awaited using the `await`
    keyword.
    """
    return await delete_component(comp)


@app.post("/modifyInv")
async def modify_inv(comp: Component):
    """
    The `get_comps_catagory` function takes a `Component` object as input and returns the category
    of components it belongs to by calling the `get_catagory_comps` function asynchronously.
    
    :param comp: The `comp` parameter is of type `Component`
    :type comp: Component
    :return: The function `get_comps_catagory` is returning the result of the
    `get_catagory_comps(comp)` function call, which is awaited using the `await` keyword.
    """
    return await modify_inventory(comp)


@app.post("/getCompsCatagory")
async def get_comps_catagory(comp: Component):
    """
    The function `get_comps_catagory` takes a `Component` object as input and returns the category
    of components it belongs to by calling the `get_catagory_comps` function asynchronously.
    
    :param comp: The parameter `comp` is of type `Component`
    :type comp: Component
    :return: the result of the `get_catagory_comps(comp)` function call, which is awaited using the
    `await` keyword.
    """
    return await get_catagory_comps(comp)


@app.get("/getCatagorys")
async def get_catagorys():
    """
    The function `get_catagorys` is an asynchronous function that returns all categories.
    :return: The function `get_catagorys` is returning the result of the `get_all_catagorys`
    function.
    """
    return await get_all_catagorys()
