import * as http from "http";
import * as fs from "fs";

//server settings
const host = "localhost";
const port = 3001;

async function sendRequest(methode, data, apiRequest) {
  try {
    const response = await fetch("http://127.0.0.1:8000/" + apiRequest, {
      method: methode,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const json = await response.text();
    console.log(json)
    return json;
  } catch (error) {
    console.log(error.stack);
  }
}

async function getData(req, res) {
  if (String(req.url).startsWith("/api/")) {
    const apiRequest = String(req.url).slice(5);
    if (req.method === "POST") {
      let data = "";

      // Accumulate the data chunks
      req.on("data", (chunk) => {
        data += chunk;
      });
      req.on("end", async () => {
        data = JSON.parse(data);

        const response = await sendRequest("POST", data, apiRequest);
        res.writeHead(200, {
          "Content-Type": "application/json",
        });
        res.end(response);

      });

    } else {
      try {
        data = {};
        const response = await sendRequest("GET", data, apiRequest);
        res.writeHead(200, {
          "Content-Type": "application/json",
        });
        res.end(response);
      } catch (error) {
        console.log(error.stack);
      }
    }
  } else if (req.url == "/script.js") {
    fs.readFile("script.js", function (err, data) {
      res.writeHead(200, {
        "Content-Type": "text/html",
      });
      res.write(data);
      res.end();
    });
  } else if (req.url == "/style.css") {
    fs.readFile("style.css", function (err, data) {
      res.writeHead(200, {
        "Content-Type": "text/css",
      });
      res.write(data);
      res.end();
    });
  } else {
    fs.readFile("index.html", function (err, data) {
      res.writeHead(200, {
        "Content-Type": "text/html",
      });
      res.write(data);
      res.end();
    });
  }
}

const server = http.createServer(getData);

server.listen(port, host);
