from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

filename = "comps.json"

jsonFile = open(filename)
data = json.load(jsonFile)
jsonFile.close()


class Component(BaseModel):
    cNumber: str
    name: str = "Na"
    catagory: str = "Na"
    price: float = 0.00
    inventory: int = 0
    image: str = "Na"
    parameters: list = []

    async def addToFile(self):
        global data, filename
        dict = {
            self.cNumber: {
                "name": self.name,
                "catagory": self.catagory,
                "price": self.price,
                "inventory": self.inventory,
                "image": self.image,
                "parameters": self.parameters,
            }
        }
        jsonFile = open("comps.json", mode="w")
        data.update(dict)
        json.dump(data, jsonFile)
        jsonFile.close()
        return self


async def getComponentInfo(comp: Component):
    """
    The `getComponentInfo` function retrieves information about a component from a website and updates a
    `Component` object with the retrieved data.

    :param comp: A `Component` object that contains information about an electronic component, such as
    its part number, name, category, price, image, and parameters
    :type comp: Component
    :return: The function `getComponentInfo` returns a `Component` object with updated information
    obtained from a web API.
    """
    re = requests.get(
        "https://wmsc.lcsc.com/wmsc/product/detail?productCode=" + comp.cNumber
    )
    responseJson = json.loads(re.text)
    comp.name = responseJson["result"]["productModel"]
    comp.catagory = responseJson["result"]["catalogName"]
    comp.price = responseJson["result"]["productPriceList"][0]["productPrice"]
    comp.image = responseJson["result"]["productImages"][0]
    paramList = responseJson["result"]["paramVOList"]
    for param in paramList:
        comp.parameters.append([param["paramNameEn"], param["paramValueEn"]])
    return comp


app = FastAPI()


@app.get("/allCopms")
async def allCopms():
    return data


@app.post("/addComp")
async def addComp(comp: Component):
    temp = await getComponentInfo(comp)
    return await temp.addToFile()
