import * as http from "http";
import * as fs from "fs";

//server settings
const host = "localhost";
const port = 3001;

async function sendRequest(methode, data, apiRequest){
  try {
    if (methode === "GET") {
      const response = await fetch("http://127.0.0.1:8000/" + apiRequest, {
        method: methode,
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response;
    }
    else {
      const response = await fetch("http://127.0.0.1:8000/" + apiRequest, {
        method: methode,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      return response;
    }
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
        res.writeHead(response.status, {
          "Content-Type": "application/json",
        });
        res.end(await response.text());

      });

    } else {
      try {
        let data = {};
        const response = await sendRequest("GET", data, apiRequest);
        res.writeHead(response.status, {
          "Content-Type": "application/json",
        });
        res.end(await response.text());
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
  }
  else if (req.url == "/addComp") {
    fs.readFile("addComp/index.html", function (err, data) {
      res.writeHead(200, {
        "Content-Type": "text/html",
      });
      res.write(data);
      res.end();
    });
  }
  else if (req.url == "/add-comp-script.js") {
    fs.readFile("addComp/script.js", function (err, data) {
      res.writeHead(200, {
        "Content-Type": "text/html",
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
