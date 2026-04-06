const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.use((req, res, next) => {
    console.log("Request:", req.method, req.url);
    next();
});

let devices = {};

app.post("/data", (req, res) => {
    console.log("BODY:", req.body);

    devices[req.body.address] = req.body;

    res.send("OK");
});

app.get("/devices", (req, res) => {
    console.log("Sending devices:", devices);
    res.json(Object.values(devices));
});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});